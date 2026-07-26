from django.contrib import admin
from .models import current_affairs_slide
from .models import currentaffairs_descriptive
from .models import the_hindu_word_Header1
from .models import the_hindu_word_list1
from .models import the_hindu_word_Header2
from .models import the_hindu_word_list2
from .models import the_economy_word_Header1
from .models import the_economy_word_list1
from .models import the_economy_word_Header2
from .models import the_economy_word_list2
from .models import total
from .models import total_english

from .models import job
from .models import total_job
from .models import total_job_category
from .models import total_job_state
from .models import home
from .models import user_save
from .models import reasoning
from .models import total_reasoning
from .models import topic
from .models import total_error
from .models import error
from .models import total_close
from .models import close

from .models import total_math
from .models import math
from .models import rule_math
from .models import math_translation
from .models import currentaffairs_mcq
from .models import currentaffairs_mcq_info_2018
from .models import currentaffairs_mcq_info_2019
from .models import currentaffairs_mcq_info_2020
from .models import currentaffairs_mcq_info_2025
from .models import currentaffairs_mcq_info_2026
from .models import currentaffairs_mcq_info_2027
from .models import currentaffairs_mcq_info_2028
from .models import currentaffairs_descriptive_info_2020
from .models import currentaffairs_descriptive_info_2018
from .models import currentaffairs_descriptive_info_2019
from .models import currentaffairs_descriptive_info_2025
from .models import currentaffairs_descriptive_info_2026
from .models import currentaffairs_descriptive_info_2027
from .models import currentaffairs_descriptive_info_2028

from .models import total_mcq
from .models import polity
from .models import total_polity
from .models import history
from .models import total_history
from .models import geography
from .models import total_geography
from .models import economics
from .models import total_economics
from .models import physics
from .models import total_physics
from .models import chemistry
from .models import total_chemistry
from .models import biology
from .models import total_biology



from django import forms
from django.db import models
from django.forms import TextInput, Textarea
from django.contrib.admin import AdminSite
from django.urls import reverse




class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = currentaffairs_descriptive
        description = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100})) 
        fields = '__all__'
        exclude = ()

class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
  

# Register your models here (using custom admin_site)
# Info table admin groupings for clearer separation
class CurrentAffairsMCQInfoAdmin(admin.ModelAdmin):
    list_display = ('total_mcq', 'total_mcq_page')
    list_filter = ('id',)
    readonly_fields = ('id',)


class CurrentAffairsDescriptiveInfoAdmin(admin.ModelAdmin):
    list_display = ('total_current_affairs', 'total_current_affairs_page')
    list_filter = ('id',)
    readonly_fields = ('id',)


class SubjectMetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'sub_chapter', 'section')
    search_fields = ('subject_name', 'sub_chapter', 'section')


class RuleMathAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'rule_name')
    list_filter = ('chapter',)
    search_fields = ('chapter', 'rule_name')
    ordering = ('chapter', 'rule_name')


from bank.admin_math_actions import (
    action_modify_language, action_validation_check,
    action_validate_math, action_modify_and_validate,
)


def translate_questions_action(modeladmin, request, queryset):
    """Single action: redirect to language-select + progress page."""
    from django.http import HttpResponseRedirect
    ids = ','.join(str(q.id) for q in queryset)
    request.session['translate_math_ids'] = ids
    return HttpResponseRedirect('translate-select/')

translate_questions_action.short_description = 'Translate selected questions'


from django.utils.html import format_html


class HasVariantsFilter(admin.SimpleListFilter):
    title = 'Has variants'
    parameter_name = 'has_variants'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes — has variants'),
            ('no',  'No variants'),
        )

    def queryset(self, request, queryset):
        from django.db.models import Count
        qs = queryset.annotate(_vc=Count('variants'))
        if self.value() == 'yes':
            return qs.filter(_vc__gt=0)
        if self.value() == 'no':
            return qs.filter(_vc=0)
        return queryset


class IsVariantFilter(admin.SimpleListFilter):
    title = 'Is a variant'
    parameter_name = 'is_variant'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes — copied from another'),
            ('no',  'No — original'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(source_math__isnull=False)
        if self.value() == 'no':
            return queryset.filter(source_math__isnull=True)
        return queryset


class MathAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_preview', 'chapter', 'subject_name', 'sub_chapter', 'section',
                    'validation_status', 'translated_language', 'source_info', 'variants_link', 'llm_used')
    list_filter = ('validation_status', 'chapter', HasVariantsFilter, IsVariantFilter)
    search_fields = ('question', 'subject_name', 'sub_chapter', 'section')
    list_editable = ('validation_status', 'llm_used')
    actions = [
        translate_questions_action,
        action_modify_language,
        action_validation_check,
        action_validate_math,
        action_modify_and_validate,
    ]

    def get_urls(self):
        from django.urls import path
        from bank.admin_translate_views import (
            translate_select_view, translate_start_view,
            translate_progress_view, translate_progress_poll,
        )
        from bank.admin_math_actions import (
            action_progress_view, action_progress_poll,
            action_save_preview, action_save_as_new, math_variants_view,
        )
        custom = [
            path('translate-select/',    translate_select_view,   name='math_translate_select'),
            path('translate-start/',     translate_start_view,    name='math_translate_start'),
            path('translate-progress/',  translate_progress_view, name='math_translate_progress'),
            path('translate-poll/',      translate_progress_poll, name='math_translate_poll'),
            path('action-progress/',     action_progress_view,    name='math_action_progress'),
            path('action-poll/',         action_progress_poll,    name='math_action_poll'),
            path('action-save-preview/', action_save_preview,     name='math_action_save_preview'),
            path('action-save-as-new/',  action_save_as_new,      name='math_action_save_as_new'),
            path('<int:math_id>/variants/', math_variants_view,   name='math_variants'),
        ]
        return custom + super().get_urls()

    def get_changelist_form(self, request, **kwargs):
        class MathListForm(forms.ModelForm):
            llm_used = forms.CharField(required=False, widget=TextInput(attrs={'size': '20'}))
        return MathListForm

    def question_preview(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_preview.short_description = 'Question'

    def source_info(self, obj):
        if obj.source_math_id:
            url = reverse('admin:bank_math_change', args=[obj.source_math_id])
            return format_html('<a href="{}">&#128279; orig&nbsp;id={}</a>', url, obj.source_math_id)
        return ''
    source_info.short_description = 'Source'

    def variants_link(self, obj):
        count = obj.variants.count()
        if count == 0:
            return ''
        url = reverse('admin:math_variants', args=[obj.id])
        return format_html('<a href="{}">&#128441; {}&nbsp;variant{}</a>',
                           url, count, 's' if count != 1 else '')
    variants_link.short_description = 'Variants'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.chapter:
            form.base_fields['rule'].queryset = rule_math.objects.filter(chapter=obj.chapter)
        else:
            form.base_fields['rule'].queryset = rule_math.objects.all()
        return form


class ReasoningAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_preview', 'validation_status', 'llm_used', 'chapter')
    list_filter = ('validation_status', 'chapter')
    search_fields = ('question',)
    list_editable = ('validation_status', 'llm_used')

    def get_changelist_form(self, request, **kwargs):
        class ReasoningListForm(forms.ModelForm):
            llm_used = forms.CharField(required=False, widget=TextInput(attrs={'size': '20'}))
        return ReasoningListForm

    def question_preview(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_preview.short_description = 'Question'

# Lists of models for grouping on admin index
mcq_info_tables = [
    currentaffairs_mcq_info_2018,
    currentaffairs_mcq_info_2019,
    currentaffairs_mcq_info_2020,
    currentaffairs_mcq_info_2025,
    currentaffairs_mcq_info_2026,
    currentaffairs_mcq_info_2027,
    currentaffairs_mcq_info_2028,
]

descriptive_info_tables = [
    currentaffairs_descriptive_info_2018,
    currentaffairs_descriptive_info_2019,
    currentaffairs_descriptive_info_2020,
    currentaffairs_descriptive_info_2025,
    currentaffairs_descriptive_info_2026,
    currentaffairs_descriptive_info_2027,
    currentaffairs_descriptive_info_2028,
]


# Custom AdminSite to supply grouped links on the index
class BankAdminSite(AdminSite):
    site_header = 'TutionPlus Admin'
    site_title = 'TutionPlus'
    index_title = 'Site administration'
    index_template = 'admin/custom_index.html'

    def index(self, request, extra_context=None):
        extra = extra_context or {}
        mcq_links = []
        desc_links = []
        for m in mcq_info_tables:
            app_label = m._meta.app_label
            model_name = m._meta.model_name
            try:
                url = reverse('admin:%s_%s_changelist' % (app_label, model_name))
            except Exception:
                url = '#'
            mcq_links.append({'name': m._meta.verbose_name_plural.title(), 'url': url})
        for m in descriptive_info_tables:
            app_label = m._meta.app_label
            model_name = m._meta.model_name
            try:
                url = reverse('admin:%s_%s_changelist' % (app_label, model_name))
            except Exception:
                url = '#'
            desc_links.append({'name': m._meta.verbose_name_plural.title(), 'url': url})
        extra.update({'mcq_links': mcq_links, 'desc_links': desc_links})
        return super().index(request, extra_context=extra)

    def app_index(self, request, app_label, extra_context=None):
        extra = extra_context or {}
        if app_label == 'bank':
            mcq_links = []
            desc_links = []
            for m in mcq_info_tables:
                app_label_m = m._meta.app_label
                model_name = m._meta.model_name
                try:
                    url = reverse('admin:%s_%s_changelist' % (app_label_m, model_name))
                except Exception:
                    url = '#'
                mcq_links.append({'name': m._meta.verbose_name_plural.title(), 'url': url})
            for m in descriptive_info_tables:
                app_label_m = m._meta.app_label
                model_name = m._meta.model_name
                try:
                    url = reverse('admin:%s_%s_changelist' % (app_label_m, model_name))
                except Exception:
                    url = '#'
                desc_links.append({'name': m._meta.verbose_name_plural.title(), 'url': url})
            extra.update({'mcq_links': mcq_links, 'desc_links': desc_links})
        return super().app_index(request, app_label, extra_context=extra)

# instantiate custom admin site
admin_site = BankAdminSite(name='bank_admin')

# Register info tables after admin_site is instantiated
for m in mcq_info_tables:
    if m not in [model for model, admin_cls in admin_site._registry.items()]:
        admin_site.register(m, CurrentAffairsMCQInfoAdmin)

for m in descriptive_info_tables:
    if m not in [model for model, admin_cls in admin_site._registry.items()]:
        admin_site.register(m, CurrentAffairsDescriptiveInfoAdmin)


admin_site.register(currentaffairs_descriptive,MessageAdmin)

# register the basic current affairs models
admin_site.register(current_affairs_slide)
admin_site.register(currentaffairs_mcq)
admin_site.register(total_mcq)

admin_site.register(total)
admin_site.register(the_hindu_word_Header1)
admin_site.register(the_hindu_word_list1)
admin_site.register(the_hindu_word_Header2)
admin_site.register(the_hindu_word_list2)
admin_site.register(the_economy_word_Header1)
admin_site.register(the_economy_word_list1)
admin_site.register(the_economy_word_Header2)
admin_site.register(the_economy_word_list2)
admin_site.register(total_english)
admin_site.register(math, MathAdmin)
admin_site.register(rule_math, RuleMathAdmin)
admin_site.register(math_translation)
admin_site.register(total_math)
admin_site.register(job)
admin_site.register(total_job)
admin_site.register(total_job_category)
admin_site.register(total_job_state)

admin_site.register(home)


admin_site.register(user_save)
admin_site.register(topic)


admin_site.register(total_reasoning)
admin_site.register(reasoning, ReasoningAdmin)

admin_site.register(total_close)
admin_site.register(close)

admin_site.register(total_error)
admin_site.register(error)

admin_site.register(total_polity)
admin_site.register(polity, SubjectMetaAdmin)

admin_site.register(total_history)
admin_site.register(history, SubjectMetaAdmin)

admin_site.register(total_geography)
admin_site.register(geography, SubjectMetaAdmin)

admin_site.register(total_economics)
admin_site.register(economics, SubjectMetaAdmin)

admin_site.register(total_physics)
admin_site.register(physics, SubjectMetaAdmin)
admin_site.register(total_chemistry)
admin_site.register(chemistry, SubjectMetaAdmin)
admin_site.register(total_biology)
admin_site.register(biology, SubjectMetaAdmin)

# Register GenAI app models with our custom admin site so GenAI appears in the custom admin
try:
    from genai.models import PDFUpload, CurrentAffairsGeneration, MathProblemGeneration, ProcessingTask, ProcessingLog, ContentSource
    from genai.admin import PDFUploadAdmin, CurrentAffairsGenerationAdmin, MathProblemGenerationAdmin, ProcessingTaskAdmin, ProcessingLogAdmin, ContentSourceAdmin

    admin_site.register(PDFUpload, PDFUploadAdmin)
    admin_site.register(CurrentAffairsGeneration, CurrentAffairsGenerationAdmin)
    admin_site.register(MathProblemGeneration, MathProblemGenerationAdmin)
    admin_site.register(ProcessingTask, ProcessingTaskAdmin)
    admin_site.register(ProcessingLog, ProcessingLogAdmin)
    admin_site.register(ContentSource, ContentSourceAdmin)
except Exception:
    # Avoid breaking admin if genai isn't available or imports fail
    pass

