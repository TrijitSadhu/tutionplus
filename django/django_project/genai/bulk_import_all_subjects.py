"""
Comprehensive Bulk Import System for ALL Subjects
Supports: Polity, History, Geography, Economics, Physics, Biology, Chemistry, 
Reasoning, Error, MCQ, and Current Affairs
"""

import json
import logging
from datetime import datetime, date, time
from django.apps import apps
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class SubjectBulkImporter:
    """
    Bulk importer for all subject models (MCQ-based subjects)
    
    Supported subjects:
    - polity, history, geography, economics
    - physics, biology, chemistry
    - reasoning, error, mcq
    - currentaffairs_mcq, currentaffairs_descriptive
    """

    # Subject configuration mapping
    SUBJECT_CONFIG = {
        'polity': {
            'model_name': 'polity',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'history': {
            'model_name': 'history',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'geography': {
            'model_name': 'geography',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'economics': {
            'model_name': 'economics',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'physics': {
            'model_name': 'physics',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'biology': {
            'model_name': 'biology',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'chemistry': {
            'model_name': 'chemistry',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'reasoning': {
            'model_name': 'reasoning',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'error': {
            'model_name': 'error',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'mcq': {
            'model_name': 'mcq',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4', 'option_5'],
            'answer_field': 'ans',
            'has_chapters': True,
            'max_chapters': 41,
            'has_difficulty': True,
            'processor_method': 'process_standard_mcq'
        },
        'currentaffairs_mcq': {
            'model_name': 'currentaffairs_mcq',
            'app_label': 'bank',
            'question_field': 'question',
            'option_fields': ['option_1', 'option_2', 'option_3', 'option_4'],
            'answer_field': 'ans',
            'has_chapters': False,
            'has_difficulty': False,
            'has_categories': True,
            'processor_method': 'process_currentaffairs_mcq'
        },
        'currentaffairs_descriptive': {
            'model_name': 'currentaffairs_descriptive',
            'app_label': 'bank',
            'processor_method': 'process_currentaffairs_descriptive'
        }
    }

    # Category mapping for current affairs
    CATEGORY_FIELDS = [
        'Science_Techonlogy',
        'National',
        'State',
        'International',
        'Business_Economy_Banking',
        'Environment',
        'Defence',
        'Persons_in_News',
        'Awards_Honours',
        'Sports',
        'Art_Culture',
        'Government_Schemes',
        'appointment',
        'obituary',
        'important_day',
        'rank',
        'mythology',
        'agreement',
        'medical',
        'static_gk'
    ]

    def __init__(self, subject: str, json_data: str, form_date: date = None):
        """
        Initialize bulk importer for a subject
        
        Args:
            subject: Subject name (e.g., 'polity', 'history', 'physics')
            json_data: JSON string with records
            form_date: Date to use if not in JSON
        """
        self.subject = subject
        self.json_data = json_data
        self.form_date = form_date or date.today()
        self.config = self.SUBJECT_CONFIG.get(subject)
        
        if not self.config:
            raise ValueError(f"Subject '{subject}' not supported. Supported: {list(self.SUBJECT_CONFIG.keys())}")
        
        self.model = None
        self.records = []
        self.errors = []
        self.created_count = 0
        self.updated_count = 0

    def parse_json(self) -> bool:
        """Parse and validate JSON data"""
        try:
            data = json.loads(self.json_data)
            
            if isinstance(data, list):
                self.records = data
            elif isinstance(data, dict) and 'records' in data:
                self.records = data['records']
            else:
                raise ValueError("JSON must be array or object with 'records' key")
            
            logger.info(f"✅ Parsed {len(self.records)} records for {self.subject}")
            return True
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False

    def get_model_class(self):
        """Get Django model class"""
        try:
            self.model = apps.get_model(
                self.config['app_label'],
                self.config['model_name']
            )
            logger.info(f"✅ Got model class: {self.model}")
            return self.model
        except Exception as e:
            error_msg = f"Failed to get model: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return None

    def extract_date_from_record(self, record: Dict) -> Tuple[str, str, date]:
        """
        Extract date from record with fallback logic:
        1. Use JSON date fields (year_now, month, day)
        2. Use form_date if JSON doesn't have dates
        3. Fallback to today
        
        Returns: (year_now, month, day_date)
        """
        # Priority 1: Check for date in JSON
        if all(key in record for key in ['year_now', 'month', 'day']):
            year_now = str(record['year_now'])
            month = str(record['month'])
            try:
                # Parse day - could be string or date object
                day_str = record['day']
                if isinstance(day_str, str):
                    day_date = datetime.strptime(day_str, '%Y-%m-%d').date()
                else:
                    day_date = day_str
                return year_now, month, day_date
            except (ValueError, TypeError):
                pass

        # Priority 2: Use form_date
        year_now = str(self.form_date.year)
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        month = month_names.get(self.form_date.month, "January")
        day_date = self.form_date

        return year_now, month, day_date

    def process_standard_mcq(self, record: Dict) -> Dict[str, Any]:
        """
        Process standard MCQ record (Polity, History, Geography, etc.)
        """
        try:
            year_now, month, day_date = self.extract_date_from_record(record)

            # Extract answer - handle both 1-5 and A-E formats
            ans_raw = record.get('ans', record.get('answer', record.get('correct_answer', 1)))
            if isinstance(ans_raw, str):
                ans_raw = ans_raw.strip().upper()
                ans_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'OPTION_1': 1, 'OPTION_2': 2, 'OPTION_3': 3, 'OPTION_4': 4, 'OPTION_5': 5}
                ans = ans_map.get(ans_raw, 1)
            else:
                ans = int(ans_raw) if ans_raw else 1

            # Extract options - handle various formats
            options = {}
            option_fields = self.config['option_fields']
            for i, field in enumerate(option_fields, 1):
                # Try: option_1, option_a, optiona, a, etc.
                option_value = (
                    record.get(field) or 
                    record.get(f'option_{chr(96+i)}') or  # option_a, option_b...
                    record.get(chr(96+i)) or  # a, b, c...
                    ''
                )
                options[field] = str(option_value)[:600]  # Truncate to max_length

            processed = {
                'question': str(record.get('question', ''))[:1000],
                'chapter': str(record.get('chapter', '1')),
                'topic': record.get('topic', 'question-answare'),
                'subtopic': record.get('subtopic', 'mcq'),
                'subtopic_2': record.get('subtopic_2', 'more'),
                'ans': ans,
                'year_exam': record.get('year_exam', ''),
                'extra': record.get('extra', record.get('explanation', '')),
                'difficulty': record.get('difficulty', 'easy'),
                'home': record.get('home', False),
                'mocktest': record.get('mocktest', False),
                'year_now': year_now,
                'month': month,
                'day': day_date,
                'creation_time': datetime.now().time(),
            }
            processed.update(options)

            return processed

        except Exception as e:
            logger.error(f"Error processing MCQ record: {str(e)}")
            self.errors.append(f"Record processing error: {str(e)}")
            return None

    def process_currentaffairs_mcq(self, record: Dict) -> Dict[str, Any]:
        """Process Current Affairs MCQ"""
        try:
            year_now, month, day_date = self.extract_date_from_record(record)

            ans_raw = record.get('ans', record.get('correct_answer', 1))
            if isinstance(ans_raw, str):
                ans_raw = ans_raw.strip().upper()
                ans_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'OPTION_1': 1, 'OPTION_2': 2, 'OPTION_3': 3, 'OPTION_4': 4}
                ans = ans_map.get(ans_raw, 1)
            else:
                ans = int(ans_raw) if ans_raw else 1

            processed = {
                'question': str(record.get('question', ''))[:1000],
                'option_1': str(record.get('option_1', record.get('option_a', '')))[:600],
                'option_2': str(record.get('option_2', record.get('option_b', '')))[:600],
                'option_3': str(record.get('option_3', record.get('option_c', '')))[:600],
                'option_4': str(record.get('option_4', record.get('option_d', '')))[:600],
                'ans': ans,
                'extra': record.get('extra', record.get('explanation', '')),
                'year_now': year_now,
                'month': month,
                'day': day_date,
                'creation_time': datetime.now().time(),
            }

            # Handle categories
            categories = record.get('categories', [])
            if categories:
                if isinstance(categories, str):
                    categories = [categories]
                for category in categories:
                    if category.strip() in self.CATEGORY_FIELDS:
                        processed[category.strip()] = True

            return processed

        except Exception as e:
            logger.error(f"Error processing Current Affairs MCQ: {str(e)}")
            self.errors.append(f"CA MCQ processing error: {str(e)}")
            return None

    def process_currentaffairs_descriptive(self, record: Dict) -> Dict[str, Any]:
        """Process Current Affairs Descriptive"""
        try:
            year_now, month, day_date = self.extract_date_from_record(record)

            processed = {
                'upper_heading': str(record.get('upper_heading', record.get('title', '')))[:250],
                'yellow_heading': str(record.get('yellow_heading', record.get('summary', '')))[:250],
                'key_1': str(record.get('key_1', record.get('key_point_1', '')))[:200],
                'key_2': str(record.get('key_2', record.get('key_point_2', '')))[:200],
                'key_3': str(record.get('key_3', record.get('key_point_3', '')))[:200],
                'key_4': str(record.get('key_4', record.get('key_point_4', '')))[:200],
                'all_key_points': record.get('all_key_points', record.get('key_points', '')),
                'paragraph': record.get('paragraph', ''),
                'year_now': year_now,
                'month': month,
                'day': day_date,
                'creation_time': datetime.now().time(),
            }

            # Handle categories
            categories = record.get('categories', [])
            if categories:
                if isinstance(categories, str):
                    categories = [categories]
                for category in categories:
                    if category.strip() in self.CATEGORY_FIELDS:
                        processed[category.strip()] = True

            return processed

        except Exception as e:
            logger.error(f"Error processing descriptive: {str(e)}")
            self.errors.append(f"Descriptive processing error: {str(e)}")
            return None

    def import_data(self) -> Dict[str, Any]:
        """
        Main import method: Parse, Process, Save
        """
        print(f"\n{'='*70}")
        print(f"📥 BULK IMPORT: {self.subject.upper()}")
        print(f"{'='*70}")
        logger.info(f"Starting bulk import for {self.subject}")

        # Step 1: Parse JSON
        print(f"\n[STEP 1] Parsing JSON...")
        if not self.parse_json():
            return {
                'success': False,
                'subject': self.subject,
                'created': 0,
                'updated': 0,
                'errors': self.errors,
                'message': f'❌ JSON parsing failed: {self.errors[0] if self.errors else "Unknown error"}'
            }

        # Step 2: Get model
        print(f"[STEP 2] Getting model...")
        if not self.get_model_class():
            return {
                'success': False,
                'subject': self.subject,
                'created': 0,
                'updated': 0,
                'errors': self.errors,
                'message': f'❌ Model not found: {self.errors[0] if self.errors else "Unknown error"}'
            }

        # Step 3: Process and save records
        print(f"[STEP 3] Processing {len(self.records)} records...")
        processor_method_name = self.config.get('processor_method', 'process_standard_mcq')
        processor_method = getattr(self, processor_method_name)

        for idx, record in enumerate(self.records, 1):
            try:
                processed = processor_method(record)
                if not processed:
                    continue

                # Check if record exists (duplicate prevention)
                question_text = processed.get('question', '')[:100]
                day = processed.get('day', date.today())
                
                existing = self.model.objects.filter(
                    question__startswith=question_text,
                    day=day
                ).first()

                if existing:
                    # Update existing record
                    for key, value in processed.items():
                        if key != 'creation_time':  # Don't update creation_time
                            setattr(existing, key, value)
                    existing.save()
                    self.updated_count += 1
                    status = "✏️  Updated"
                else:
                    # Create new record
                    obj = self.model.objects.create(**processed)
                    self.created_count += 1
                    status = "✅ Created"

                if idx % 10 == 0 or idx == len(self.records):
                    print(f"  [{idx}/{len(self.records)}] {status}")

            except Exception as e:
                error_msg = f"Record {idx}: {str(e)}"
                logger.error(error_msg)
                self.errors.append(error_msg)
                print(f"  [{idx}] ❌ Error: {str(e)}")

        # Step 4: Return results
        print(f"\n{'='*70}")
        print(f"✅ IMPORT COMPLETE")
        print(f"  Created: {self.created_count}")
        print(f"  Updated: {self.updated_count}")
        print(f"  Errors: {len(self.errors)}")
        print(f"{'='*70}\n")

        return {
            'success': True,
            'subject': self.subject,
            'created': self.created_count,
            'updated': self.updated_count,
            'errors': self.errors,
            'message': f'✅ Bulk import complete: {self.created_count} created, {self.updated_count} updated'
        }


def bulk_import_subject(subject: str, json_data: str, form_date: date = None) -> Dict[str, Any]:
    """
    Convenient function to bulk import any subject
    
    Args:
        subject: Subject name
        json_data: JSON string with records
        form_date: Optional date for records without dates
    
    Returns:
        Import result dictionary
    """
    try:
        importer = SubjectBulkImporter(subject, json_data, form_date)
        return importer.import_data()
    except Exception as e:
        logger.error(f"Bulk import error: {str(e)}")
        return {
            'success': False,
            'subject': subject,
            'created': 0,
            'updated': 0,
            'errors': [str(e)],
            'message': f'❌ Error: {str(e)}'
        }
