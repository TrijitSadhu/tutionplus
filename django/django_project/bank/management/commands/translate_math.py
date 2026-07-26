"""
Management command: translate_math
Batch-translates math questions using Groq API and stores in math_translation table.

Usage:
  python manage.py translate_math --language hi
  python manage.py translate_math --language bn --chapter profit_n_loss
  python manage.py translate_math --language ta --limit 20
  python manage.py translate_math --language hi --force   (re-translate even if exists)
"""

import json
import time

from django.core.management.base import BaseCommand, CommandError
from bank.models import math as Math, math_translation


LANG_NAMES = {
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
}


def _extract_json(text):
    """Strip markdown code fences and return the JSON string."""
    text = text.strip()
    if '```' in text:
        parts = text.split('```')
        for part in parts:
            part = part.strip()
            if part.startswith('json'):
                part = part[4:].strip()
            if part.startswith('{'):
                return part
    return text


class Command(BaseCommand):
    help = 'Batch-translate math questions to a target language using Groq API.'

    def add_arguments(self, parser):
        parser.add_argument('--language', required=True,
                            help='Target language code: hi, bn, ta, te, mr')
        parser.add_argument('--chapter', default='all',
                            help='Chapter slug (default: all chapters)')
        parser.add_argument('--limit', type=int, default=None,
                            help='Max number of questions to translate (default: all)')
        parser.add_argument('--force', action='store_true',
                            help='Re-translate even if translation already exists')
        parser.add_argument('--delay', type=float, default=0.5,
                            help='Seconds to wait between API calls (default: 0.5)')

    def handle(self, *args, **options):
        lang = options['language']
        chapter = options['chapter']
        limit = options['limit']
        force = options['force']
        delay = options['delay']

        if lang not in LANG_NAMES:
            raise CommandError(
                f'Unknown language: "{lang}". Valid codes: {", ".join(LANG_NAMES)}'
            )

        # Build queryset
        qs = Math.objects.all().order_by('id')
        if chapter != 'all':
            qs = qs.filter(chapter=chapter)
            self.stdout.write(f'Chapter filter: {chapter}')

        if not force:
            already_done = set(
                math_translation.objects.filter(language=lang)
                .values_list('math_id', flat=True)
            )
            qs = qs.exclude(id__in=already_done)
            self.stdout.write(f'Skipping {len(already_done)} already-translated questions.')

        if limit:
            qs = qs[:limit]

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS('Nothing to translate.'))
            return

        self.stdout.write(f'Translating {total} questions to {LANG_NAMES[lang]}...\n')

        # Initialize Groq client
        try:
            from genai.config import GROQ_API_KEY, GROQ_MODEL
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            model = GROQ_MODEL
        except Exception as e:
            raise CommandError(f'Failed to init Groq client: {e}')

        ok_count = 0
        err_count = 0

        for i, q in enumerate(qs, 1):
            payload = {
                'question': q.question or '',
                'a': q.a or '',
                'b': q.b or '',
                'c': q.c or '',
                'd': q.d or '',
                'e': q.e or '',
                'solution': q.solution or '',
                'shortcut': q.shortcut or '',
            }

            prompt = (
                f'Translate the following math question fields to {LANG_NAMES[lang]}.\n'
                'STRICT RULES:\n'
                '- Translate ONLY human-readable text words.\n'
                '- Do NOT change, remove, or add any HTML tags (e.g. <b>, <br>, <p>, <div>, <img>).\n'
                '- Do NOT change any numbers, mathematical symbols, or unit labels (Rs, kg, km, %, litres, etc.).\n'
                '- Return ONLY valid JSON with the exact same 8 keys. No explanation, no code fences.\n\n'
                f'Input JSON:\n{json.dumps(payload, ensure_ascii=False)}'
            )

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=0.3,
                    max_tokens=3000,
                )
                raw = response.choices[0].message.content
                clean = _extract_json(raw)
                result = json.loads(clean)

                math_translation.objects.update_or_create(
                    math=q,
                    language=lang,
                    defaults={
                        'question': result.get('question', ''),
                        'a': result.get('a', ''),
                        'b': result.get('b', ''),
                        'c': result.get('c', ''),
                        'd': result.get('d', ''),
                        'e': result.get('e', ''),
                        'solution': result.get('solution', ''),
                        'shortcut': result.get('shortcut', ''),
                    }
                )
                ok_count += 1
                self.stdout.write(f'  [{i}/{total}] OK  id={q.id} chapter={q.chapter}')

            except Exception as ex:
                err_count += 1
                self.stderr.write(f'  [{i}/{total}] ERR id={q.id}: {ex}')
                time.sleep(1)
                continue

            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. Translated: {ok_count}, Errors: {err_count}'
        ))
