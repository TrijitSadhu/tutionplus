"""
Enhanced Save Methods for All Subject Models
This module provides save method patterns and utilities for all subject models
"""

import logging
from datetime import datetime, date
from django.db import models

logger = logging.getLogger(__name__)


class SubjectSaveMixin:
    """
    Mixin providing common save logic for all MCQ-based subjects
    Apply to models: polity, history, geography, economics, physics, biology, chemistry, 
                    reasoning, error, mcq
    """

    def generate_new_id(self):
        """Generate unique ID from question and date"""
        question_start = self.question[:100] if hasattr(self, 'question') and self.question else 'unknown'
        day_str = self.day.strftime('%d-%m-%Y') if hasattr(self, 'day') and self.day else date.today().strftime('%d-%m-%Y')
        return f"{question_start}==={day_str}"

    def update_chapter_count(self):
        """Update total count for specific chapter"""
        if not hasattr(self, 'chapter') or not hasattr(self, 'day'):
            return

        # Find the corresponding total model (e.g., total_polity for polity)
        model_name = self.__class__.__name__
        total_model_name = f"total_{model_name}"
        
        try:
            from django.apps import apps
            total_model = apps.get_model('bank', total_model_name)
            
            # Get or create total record
            total_record, created = total_model.objects.get_or_create(pk=1)
            
            # Count records in this chapter
            chapter_count = self.__class__.objects.filter(chapter=self.chapter).count()
            
            # Calculate pages (5 per page)
            if chapter_count % 5 == 0:
                chapter_pages = chapter_count // 5
            else:
                chapter_pages = (chapter_count // 5) + 1
            
            # Set chapter count field
            chapter_field = f"chapter_{self.chapter}"
            if hasattr(total_record, chapter_field):
                setattr(total_record, chapter_field, chapter_pages)
            
            # Update total count
            total_count = self.__class__.objects.count()
            if hasattr(total_record, f'total_{model_name}'):
                setattr(total_record, f'total_{model_name}', total_count)
            
            # Calculate total pages
            if total_count % 5 == 0:
                total_pages = total_count // 5
            else:
                total_pages = (total_count // 5) + 1
            
            if hasattr(total_record, f'total_{model_name}_page'):
                setattr(total_record, f'total_{model_name}_page', total_pages)
            
            # Save without triggering this save again
            total_record.save()
            
            logger.info(f"✅ Updated counts for {model_name} - Chapter {self.chapter}: {chapter_pages} pages, Total: {total_pages} pages")
            
        except Exception as e:
            logger.warning(f"Could not update chapter counts: {str(e)}")

    def validate_answer(self):
        """Validate answer is within valid range"""
        if hasattr(self, 'ans'):
            if self.ans is None or self.ans < 1:
                self.ans = 1
            elif self.ans > 5:
                self.ans = 5

    def truncate_fields(self):
        """Truncate text fields to model max_length"""
        field_limits = {
            'question': 1000,
            'option_1': 600,
            'option_2': 600,
            'option_3': 600,
            'option_4': 600,
            'option_5': 600,
            'year_exam': 250,
            'extra': None,  # TextField, no limit
        }
        
        for field, max_len in field_limits.items():
            if hasattr(self, field) and max_len:
                value = getattr(self, field, '')
                if value and len(str(value)) > max_len:
                    setattr(self, field, str(value)[:max_len])

    def ensure_creation_time(self):
        """Ensure creation_time is set"""
        if hasattr(self, 'creation_time') and not self.creation_time:
            self.creation_time = datetime.now().time()

    def save_with_logging(self, *args, **kwargs):
        """Enhanced save with logging and validation"""
        try:
            # Pre-save operations
            if hasattr(self, 'validate_answer'):
                self.validate_answer()
            
            if hasattr(self, 'truncate_fields'):
                self.truncate_fields()
            
            if hasattr(self, 'ensure_creation_time'):
                self.ensure_creation_time()
            
            if hasattr(self, 'generate_new_id') and hasattr(self, 'new_id'):
                self.new_id = self.generate_new_id()
            
            # Call parent save
            super().save(*args, **kwargs)
            
            # Post-save operations
            if hasattr(self, 'update_chapter_count'):
                self.update_chapter_count()
            
            logger.info(f"✅ Saved {self.__class__.__name__} (ID: {self.pk}) - Question: {getattr(self, 'question', 'N/A')[:50]}")
            
        except Exception as e:
            logger.error(f"❌ Error saving {self.__class__.__name__}: {str(e)}")
            raise


class CurrentAffairsSaveMixin:
    """
    Mixin for Current Affairs models (descriptive and MCQ)
    Provides common save logic for: currentaffairs_mcq, currentaffairs_descriptive
    """

    def ensure_date_fields(self):
        """Ensure year_now, month, day are populated"""
        if hasattr(self, 'day') and self.day:
            if not self.year_now:
                self.year_now = str(self.day.year)
            
            if not self.month:
                month_names = {
                    1: "January", 2: "February", 3: "March", 4: "April",
                    5: "May", 6: "June", 7: "July", 8: "August",
                    9: "September", 10: "October", 11: "November", 12: "December"
                }
                self.month = month_names.get(self.day.month, "January")

    def ensure_creation_time(self):
        """Ensure creation_time is set"""
        if hasattr(self, 'creation_time') and not self.creation_time:
            self.creation_time = datetime.now().time()

    def truncate_text_fields(self):
        """Truncate heading fields"""
        field_limits = {
            'upper_heading': 250,
            'yellow_heading': 250,
            'key_1': 200,
            'key_2': 200,
            'key_3': 200,
            'key_4': 200,
            'question': 1000,
            'option_1': 600,
            'option_2': 600,
            'option_3': 600,
            'option_4': 600,
        }
        
        for field, max_len in field_limits.items():
            if hasattr(self, field) and max_len:
                value = getattr(self, field, '')
                if value and len(str(value)) > max_len:
                    setattr(self, field, str(value)[:max_len])

    def validate_categories(self):
        """Ensure category fields are boolean"""
        category_fields = [
            'Science_Techonlogy', 'National', 'State', 'International',
            'Business_Economy_Banking', 'Environment', 'Defence',
            'Persons_in_News', 'Awards_Honours', 'Sports', 'Art_Culture',
            'Government_Schemes', 'appointment', 'obituary', 'important_day',
            'rank', 'mythology', 'agreement', 'medical', 'static_gk'
        ]
        
        for field in category_fields:
            if hasattr(self, field):
                value = getattr(self, field)
                if value is None or value == '':
                    setattr(self, field, False)
                elif isinstance(value, str):
                    setattr(self, field, value.lower() in ['true', '1', 'yes'])

    def validate_mcq_answer(self):
        """Validate MCQ answer for current affairs"""
        if hasattr(self, 'ans'):
            if self.ans is None or self.ans < 1:
                self.ans = 1
            elif self.ans > 4:
                self.ans = 4

    def save_with_logging(self, *args, **kwargs):
        """Enhanced save for current affairs models"""
        try:
            # Pre-save operations
            if hasattr(self, 'ensure_date_fields'):
                self.ensure_date_fields()
            
            if hasattr(self, 'ensure_creation_time'):
                self.ensure_creation_time()
            
            if hasattr(self, 'truncate_text_fields'):
                self.truncate_text_fields()
            
            if hasattr(self, 'validate_categories'):
                self.validate_categories()
            
            if hasattr(self, 'validate_mcq_answer'):
                self.validate_mcq_answer()
            
            # Call parent save
            super().save(*args, **kwargs)
            
            logger.info(f"✅ Saved {self.__class__.__name__} (ID: {self.pk})")
            
        except Exception as e:
            logger.error(f"❌ Error saving {self.__class__.__name__}: {str(e)}")
            raise


# Template Save Methods for Copy-Paste into Models

STANDARD_MCQ_SAVE_METHOD = '''
    def save(self, *args, **kwargs):
        """Enhanced save method with validation and counting"""
        # Validate answer
        if self.ans is None or self.ans < 1:
            self.ans = 1
        elif self.ans > 5:
            self.ans = 5
        
        # Ensure creation_time
        if not self.creation_time:
            from datetime import datetime
            self.creation_time = datetime.now().time()
        
        # Truncate fields
        if len(self.question) > 1000:
            self.question = self.question[:1000]
        for field in ['option_1', 'option_2', 'option_3', 'option_4', 'option_5']:
            value = getattr(self, field, '')
            if value and len(value) > 600:
                setattr(self, field, value[:600])
        
        # Generate new_id
        self.new_id = self.question[:100] + '===' + self.day.strftime('%d-%m-%Y')
        
        # Call parent save
        super({model_name}, self).save(*args, **kwargs)
        
        # Update chapter counts
        try:
            from django.apps import apps
            total_model_name = 'total_{model_name}'
            total_model = apps.get_model('bank', total_model_name)
            
            total_record, created = total_model.objects.get_or_create(pk=1)
            
            chapter_count = {model_name}.objects.filter(chapter=self.chapter).count()
            chapter_pages = (chapter_count + 4) // 5  # Ceiling division
            
            chapter_field = f'chapter_{self.chapter}'
            setattr(total_record, chapter_field, chapter_pages)
            
            total_count = {model_name}.objects.count()
            setattr(total_record, 'total_{model_name}', total_count)
            setattr(total_record, 'total_{model_name}_page', (total_count + 4) // 5)
            
            total_record.save()
        except Exception as e:
            import logging
            logging.error(f'Could not update chapter counts: {e}')
'''

CURRENTAFFAIRS_MCQ_SAVE_METHOD = '''
    def save(self, *args, **kwargs):
        """Enhanced save method for Current Affairs MCQ"""
        from datetime import datetime
        
        # Ensure date fields
        if self.day:
            if not self.year_now:
                self.year_now = str(self.day.year)
            if not self.month:
                month_names = {1: "January", 2: "February", 3: "March", 4: "April",
                              5: "May", 6: "June", 7: "July", 8: "August",
                              9: "September", 10: "October", 11: "November", 12: "December"}
                self.month = month_names.get(self.day.month, "January")
        
        # Ensure creation_time
        if not self.creation_time:
            self.creation_time = datetime.now().time()
        
        # Validate answer (1-4 for CA)
        if self.ans is None or self.ans < 1:
            self.ans = 1
        elif self.ans > 4:
            self.ans = 4
        
        # Truncate fields
        if len(self.question) > 1000:
            self.question = self.question[:1000]
        for field in ['option_1', 'option_2', 'option_3', 'option_4']:
            value = getattr(self, field, '')
            if value and len(value) > 600:
                setattr(self, field, value[:600])
        
        # Validate categories
        category_fields = ['Science_Techonlogy', 'National', 'State', 'International',
                          'Business_Economy_Banking', 'Environment', 'Defence',
                          'Persons_in_News', 'Awards_Honours', 'Sports', 'Art_Culture',
                          'Government_Schemes', 'appointment', 'obituary', 'important_day',
                          'rank', 'mythology', 'agreement', 'medical', 'static_gk']
        
        for field in category_fields:
            if hasattr(self, field):
                value = getattr(self, field)
                if value is None or value == '':
                    setattr(self, field, False)
                elif isinstance(value, str):
                    setattr(self, field, value.lower() in ['true', '1', 'yes'])
        
        super(currentaffairs_mcq, self).save(*args, **kwargs)
'''

CURRENTAFFAIRS_DESCRIPTIVE_SAVE_METHOD = '''
    def save(self, *args, **kwargs):
        """Enhanced save method for Current Affairs Descriptive"""
        from datetime import datetime
        
        # Ensure date fields
        if self.day:
            if not self.year_now:
                self.year_now = str(self.day.year)
            if not self.month:
                month_names = {1: "January", 2: "February", 3: "March", 4: "April",
                              5: "May", 6: "June", 7: "July", 8: "August",
                              9: "September", 10: "October", 11: "November", 12: "December"}
                self.month = month_names.get(self.day.month, "January")
        
        # Ensure creation_time
        if not self.creation_time:
            self.creation_time = datetime.now().time()
        
        # Truncate heading fields
        for field in ['upper_heading', 'yellow_heading', 'key_1', 'key_2', 'key_3', 'key_4']:
            value = getattr(self, field, '')
            max_len = 250 if field in ['upper_heading', 'yellow_heading'] else 200
            if value and len(value) > max_len:
                setattr(self, field, value[:max_len])
        
        # Validate categories
        category_fields = ['Science_Techonlogy', 'National', 'State', 'International',
                          'Business_Economy_Banking', 'Environment', 'Defence',
                          'Persons_in_News', 'Awards_Honours', 'Sports', 'Art_Culture',
                          'Government_Schemes', 'appointment', 'obituary', 'important_day',
                          'rank', 'mythology', 'agreement', 'medical', 'static_gk']
        
        for field in category_fields:
            if hasattr(self, field):
                value = getattr(self, field)
                if value is None or value == '':
                    setattr(self, field, False)
                elif isinstance(value, str):
                    setattr(self, field, value.lower() in ['true', '1', 'yes'])
        
        super(currentaffairs_descriptive, self).save(*args, **kwargs)
'''

# Usage instructions for updating models
IMPLEMENTATION_INSTRUCTIONS = """
=== SAVE METHOD IMPLEMENTATION GUIDE ===

For STANDARD MCQ SUBJECTS (polity, history, geography, economics, physics, biology, chemistry, reasoning, error, mcq):

Replace the save() method in each model with:

```python
def save(self, *args, **kwargs):
    # Validate answer
    if self.ans is None or self.ans < 1:
        self.ans = 1
    elif self.ans > 5:
        self.ans = 5
    
    # Ensure creation_time
    if not self.creation_time:
        from datetime import datetime
        self.creation_time = datetime.now().time()
    
    # Truncate fields
    if len(self.question) > 1000:
        self.question = self.question[:1000]
    for field in ['option_1', 'option_2', 'option_3', 'option_4', 'option_5']:
        value = getattr(self, field, '')
        if value and len(value) > 600:
            setattr(self, field, value[:600])
    
    # Generate new_id
    self.new_id = self.question[:100] + '===' + self.day.strftime('%d-%m-%Y')
    
    # Call parent save
    super({ModelName}, self).save(*args, **kwargs)
    
    # Update chapter counts
    try:
        from django.apps import apps
        model_name = self.__class__.__name__
        total_model_name = f'total_{model_name}'
        total_model = apps.get_model('bank', total_model_name)
        
        total_record, created = total_model.objects.get_or_create(pk=1)
        
        chapter_count = self.__class__.objects.filter(chapter=self.chapter).count()
        chapter_pages = (chapter_count + 4) // 5
        
        chapter_field = f'chapter_{self.chapter}'
        setattr(total_record, chapter_field, chapter_pages)
        
        total_count = self.__class__.objects.count()
        setattr(total_record, f'total_{model_name}', total_count)
        setattr(total_record, f'total_{model_name}_page', (total_count + 4) // 5)
        
        total_record.save()
    except Exception as e:
        import logging
        logging.error(f'Could not update chapter counts: {e}')
```

For CURRENT AFFAIRS MCQ (currentaffairs_mcq):
- Validate answer: 1-4 (not 5)
- Ensure year_now, month from day field
- Validate all category boolean fields
- See CURRENTAFFAIRS_MCQ_SAVE_METHOD above

For CURRENT AFFAIRS DESCRIPTIVE (currentaffairs_descriptive):
- Ensure year_now, month from day field
- Truncate heading fields to 250 chars
- Validate all category boolean fields
- See CURRENTAFFAIRS_DESCRIPTIVE_SAVE_METHOD above
"""
