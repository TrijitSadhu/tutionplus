"""
Bulk import utility for JSON data to bank models
Handles mapping JSON fields to model fields and saving records
"""

import json
import logging
from datetime import datetime, date, time
from typing import Dict, Any, List, Tuple
from decimal import Decimal

logger = logging.getLogger(__name__)


class BulkImporter:
    """Handles bulk import of JSON data to bank models"""
    
    def __init__(self, table_name: str, json_data: str, form_date: date = None, form_time: time = None):
        """
        Initialize bulk importer
        
        Args:
            table_name: Name of the target bank model table
            json_data: JSON string containing array of objects
            form_date: Date from the intermediate form (fallback if not in JSON)
            form_time: Time from the intermediate form (fallback if not in JSON)
        """
        print("\n" + "="*80)
        print(f"📦 [IMPORTER_INIT] BulkImporter.__init__() called")
        print(f"   table_name: {table_name}")
        print(f"   json_data length: {len(json_data)} chars")
        print(f"   form_date: {form_date}")
        print(f"   form_time: {form_time}")
        print("="*80)
        
        self.table_name = table_name
        self.json_data = json_data
        self.form_date = form_date or date.today()
        self.form_time = form_time or datetime.now().time()
        self.records = []
        self.errors = []
        self.created_count = 0
        self.updated_count = 0
        
        print(f"   ✅ Importer initialized")
        print(f"   Using date: {self.form_date}")
        print(f"   Using time: {self.form_time}\n")
        
    def parse_json(self) -> bool:
        """Parse and validate JSON data"""
        print(f"\n[PARSE_JSON] Starting JSON parse...")
        try:
            print(f"   [ATTEMPT] json.loads({len(self.json_data)} chars)...")
            self.records = json.loads(self.json_data)
            print(f"   ✅ JSON parsed successfully")
            print(f"   Type of parsed data: {type(self.records)}")
            
            if not isinstance(self.records, list):
                print(f"   ⚠️  Data is not a list, wrapping in list")
                self.records = [self.records]
            
            print(f"   ✅ Total records to import: {len(self.records)}")
            for idx, record in enumerate(self.records[:3]):
                print(f"      Record {idx}: {str(record)[:100]}...")
            if len(self.records) > 3:
                print(f"      ... and {len(self.records) - 3} more records")
            
            logger.info(f"Parsed {len(self.records)} records from JSON")
            return True
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON Parse Error: {str(e)}")
            self.errors.append(f"Invalid JSON: {str(e)}")
            logger.error(f"JSON parse error: {str(e)}")
            return False
    
    def get_model_class(self):
        """Get the Django model class for the target table"""
        from django.apps import apps
        
        model_map = {
            # Subject MCQ Tables
            'polity': 'bank.polity',
            'history': 'bank.history',
            'geography': 'bank.geography',
            'economics': 'bank.economics',
            'physics': 'bank.physics',
            'chemistry': 'bank.chemistry',
            'biology': 'bank.biology',
            'reasoning': 'bank.reasoning',
            'error': 'bank.error',
            'mcq': 'bank.mcq',
            # Current Affairs Tables
            'currentaffairs_mcq': 'bank.currentaffairs_mcq',
            'currentaffairs_descriptive': 'bank.currentaffairs_descriptive',
            'current_affairs_slide': 'bank.current_affairs_slide',
            # Other Tables
            'total': 'bank.total',
            'total_english': 'bank.total_english',
            'total_math': 'bank.total_math',
            'total_job': 'bank.total_job',
            'total_job_category': 'bank.total_job_category',
            'total_job_state': 'bank.total_job_state',
            'home': 'bank.home',
            'topic': 'bank.topic',
            'math': 'bank.math',
            'job': 'bank.job',
            'the_hindu_word_Header1': 'bank.the_hindu_word_Header1',
            'the_hindu_word_Header2': 'bank.the_hindu_word_Header2',
            'the_hindu_word_list1': 'bank.the_hindu_word_list1',
            'the_hindu_word_list2': 'bank.the_hindu_word_list2',
            'the_economy_word_Header1': 'bank.the_economy_word_Header1',
            'the_economy_word_Header2': 'bank.the_economy_word_Header2',
            'the_economy_word_list1': 'bank.the_economy_word_list1',
            'the_economy_word_list2': 'bank.the_economy_word_list2',
        }
        
        model_path = model_map.get(self.table_name)
        if not model_path:
            raise ValueError(f"Unknown table: {self.table_name}")
        
        return apps.get_model(model_path)
    
    def extract_date_from_record(self, record: Dict) -> Tuple[str, str, date]:
        """
        Extract date information from record
        Priority: JSON fields > form date
        
        Returns: (year_now, month, day_date)
        """
        year_now = record.get('year_now') or record.get('year')
        month = record.get('month')
        day_date = None
        
        # Try to extract day from record
        if 'day' in record:
            day_val = record['day']
            if isinstance(day_val, str):
                try:
                    day_date = datetime.strptime(day_val, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        day_date = datetime.strptime(day_val, '%d/%m/%Y').date()
                    except ValueError:
                        day_date = None
            elif isinstance(day_val, date):
                day_date = day_val
        
        # Use form date as fallback
        if not day_date:
            day_date = self.form_date
        
        # Use form year/month as fallback
        if not year_now:
            year_now = str(self.form_date.year)
        if not month:
            month_names = {
                1: "January", 2: "February", 3: "March", 4: "April",
                5: "May", 6: "June", 7: "July", 8: "August",
                9: "September", 10: "October", 11: "November", 12: "December"
            }
            month = month_names.get(self.form_date.month, "January")
        
        return str(year_now), str(month), day_date
    
    def process_currentaffairs_mcq(self, record: Dict, model_class) -> bool:
        """Process and save currentaffairs_mcq records"""
        print(f"\n   [PROCESS_MCQ] Processing MCQ record...")
        try:
            print(f"      [EXTRACT_DATE] Extracting date information...")
            year_now, month, day_date = self.extract_date_from_record(record)
            print(f"         Year: {year_now}, Month: {month}, Day: {day_date}")
            
            # Extract fields
            question = record.get('question', '')
            option_1 = record.get('option_1', '')
            option_2 = record.get('option_2', '')
            option_3 = record.get('option_3', '')
            option_4 = record.get('option_4', '')
            option_5 = record.get('option_5', '')
            
            print(f"      [FIELDS] Extracted question: {question[:80]}...")
            print(f"               Option fields extracted: 5")
            
            # Handle correct answer
            ans = record.get('ans', record.get('correct_answer', 1))
            if isinstance(ans, str):
                ans_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, '1': 1, '2': 2, '3': 3, '4': 4}
                ans = ans_map.get(ans.upper(), 1)
            print(f"      [ANSWER] Correct answer: {ans}")
            
            # Extract creation time
            creation_time = record.get('creation_time')
            if isinstance(creation_time, str):
                try:
                    creation_time = datetime.strptime(creation_time, '%H:%M:%S').time()
                except ValueError:
                    creation_time = self.form_time
            elif not creation_time:
                creation_time = self.form_time
            print(f"      [TIME] Creation time: {creation_time}")
            
            # Create or update record
            print(f"      [DB] Calling update_or_create()...")
            obj, created = model_class.objects.update_or_create(
                question=question,
                day=day_date,
                defaults={
                    'year_now': year_now,
                    'month': month,
                    'option_1': option_1,
                    'option_2': option_2,
                    'option_3': option_3,
                    'option_4': option_4,
                    'option_5': option_5,
                    'ans': int(ans),
                    'creation_time': creation_time,
                    'extra': record.get('extra', record.get('explanation', '')),
                    'is_live': record.get('is_live', True),
                }
            )
            print(f"         {'✅ CREATED' if created else '✏️  UPDATED'} Record (ID: {obj.id})")
            
            # Handle categories (boolean fields)
            categories = record.get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            
            print(f"      [CATEGORIES] Setting categories: {categories}")
            if isinstance(categories, list):
                category_fields = [
                    'Science_Techonlogy', 'National', 'International',
                    'Business_Economy_Banking', 'Environment', 'Defence',
                    'Sports', 'Art_Culture', 'Awards_Honours', 'Persons_in_News',
                    'Government_Schemes', 'State', 'appointment', 'obituary',
                    'important_day', 'rank', 'mythology', 'agreement', 'medical', 'static_gk'
                ]
                
                # Reset all categories to False first
                for field in category_fields:
                    if hasattr(obj, field):
                        setattr(obj, field, False)
                
                # Set specified categories to True
                for cat in categories:
                    if isinstance(cat, str):
                        cat = cat.strip()
                        if hasattr(obj, cat):
                            setattr(obj, cat, True)
                            print(f"         ✓ {cat} = True")
                
                obj.save()
                print(f"         ✅ Categories saved")
            
            if created:
                self.created_count += 1
            else:
                self.updated_count += 1
            
            print(f"      ✅ MCQ processing complete")
            logger.info(f"{'Created' if created else 'Updated'} MCQ: {question[:50]}...")
            return True
        
        except Exception as e:
            error_msg = f"Error processing MCQ: {str(e)}"
            print(f"      ❌ {error_msg}")
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False
    
    def process_currentaffairs_descriptive(self, record: Dict, model_class) -> bool:
        """Process and save currentaffairs_descriptive records"""
        print(f"\n   [PROCESS_DESC] Processing descriptive record...")
        try:
            print(f"      [EXTRACT_DATE] Extracting date information...")
            year_now, month, day_date = self.extract_date_from_record(record)
            print(f"         Year: {year_now}, Month: {month}, Day: {day_date}")
            
            # Extract fields
            upper_heading = record.get('upper_heading', '')
            yellow_heading = record.get('yellow_heading', '')
            key_1 = record.get('key_1', '')
            key_2 = record.get('key_2', '')
            key_3 = record.get('key_3', '')
            key_4 = record.get('key_4', '')
            
            print(f"      [FIELDS] Extracted upper_heading: {upper_heading[:80]}...")
            print(f"               Key fields extracted: 4")
            
            # Extract creation time
            creation_time = record.get('creation_time')
            if isinstance(creation_time, str):
                try:
                    creation_time = datetime.strptime(creation_time, '%H:%M:%S').time()
                except ValueError:
                    creation_time = self.form_time
            elif not creation_time:
                creation_time = self.form_time
            print(f"      [TIME] Creation time: {creation_time}")
            
            # Create or update record
            print(f"      [DB] Calling update_or_create()...")
            obj, created = model_class.objects.update_or_create(
                upper_heading=upper_heading,
                day=day_date,
                defaults={
                    'year_now': year_now,
                    'month': month,
                    'yellow_heading': yellow_heading,
                    'key_1': key_1,
                    'key_2': key_2,
                    'key_3': key_3,
                    'key_4': key_4,
                    'creation_time': creation_time,
                    'all_key_points': record.get('all_key_points', ''),
                    'paragraph': record.get('paragraph', ''),
                    'link': record.get('link', ''),
                    'url': record.get('url', ''),
                }
            )
            print(f"         {'✅ CREATED' if created else '✏️  UPDATED'} Record (ID: {obj.id})")
            
            # Handle categories (boolean fields)
            categories = record.get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            
            print(f"      [CATEGORIES] Setting categories: {categories}")
            if isinstance(categories, list):
                category_fields = [
                    'Science_Techonlogy', 'National', 'International',
                    'Business_Economy_Banking', 'Environment', 'Defence',
                    'Sports', 'Art_Culture', 'Awards_Honours', 'Persons_in_News',
                    'Government_Schemes', 'State', 'appointment', 'obituary',
                    'important_day', 'rank', 'mythology', 'agreement', 'medical', 'static_gk'
                ]
                
                # Reset all categories to False first
                for field in category_fields:
                    if hasattr(obj, field):
                        setattr(obj, field, False)
                
                # Set specified categories to True
                for cat in categories:
                    if isinstance(cat, str):
                        cat = cat.strip()
                        if hasattr(obj, cat):
                            setattr(obj, cat, True)
                            print(f"         ✓ {cat} = True")
                
                obj.save()
                print(f"         ✅ Categories saved")
            
            if created:
                self.created_count += 1
            else:
                self.updated_count += 1
            
            print(f"      ✅ Descriptive processing complete")
            logger.info(f"{'Created' if created else 'Updated'} Descriptive: {upper_heading[:50]}...")
            return True
        
        except Exception as e:
            error_msg = f"Error processing descriptive: {str(e)}"
            print(f"      ❌ {error_msg}")
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False
    
    def process_current_affairs_slide(self, record: Dict, model_class) -> bool:
        """Process and save current_affairs_slide records"""
        try:
            day_date = record.get('day', self.form_date)
            if isinstance(day_date, str):
                try:
                    day_date = datetime.strptime(day_date, '%Y-%m-%d').date()
                except ValueError:
                    day_date = self.form_date
            
            creation_time = record.get('creation_time', self.form_time)
            if isinstance(creation_time, str):
                try:
                    creation_time = datetime.strptime(creation_time, '%H:%M:%S').time()
                except ValueError:
                    creation_time = self.form_time
            
            upper_heading = record.get('upper_heading', '')
            
            obj, created = model_class.objects.update_or_create(
                upper_heading=upper_heading,
                day=day_date,
                defaults={
                    'yellow_heading': record.get('yellow_heading', ''),
                    'key_1': record.get('key_1', ''),
                    'key_2': record.get('key_2', ''),
                    'key_3': record.get('key_3', ''),
                    'key_4': record.get('key_4', ''),
                    'creation_time': creation_time,
                }
            )
            
            if created:
                self.created_count += 1
            else:
                self.updated_count += 1
            
            logger.info(f"{'Created' if created else 'Updated'} Slide: {upper_heading[:50]}...")
            return True
        
        except Exception as e:
            error_msg = f"Error processing slide: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False
    
    def process_generic_model(self, record: Dict, model_class) -> bool:
        """Process and save generic model records (fallback for unknown models)"""
        try:
            # Use the first available field as unique identifier
            model_fields = {f.name: f for f in model_class._meta.get_fields()}
            
            # Try to find a text field to use as identifier
            identifier_field = None
            identifier_value = None
            
            for field_name in ['name', 'title', 'heading', 'upper_heading', 'question']:
                if field_name in model_fields:
                    identifier_field = field_name
                    identifier_value = record.get(field_name)
                    if identifier_value:
                        break
            
            if not identifier_field or not identifier_value:
                self.errors.append(f"Cannot find unique identifier in record: {record}")
                return False
            
            # Prepare defaults dict with only valid model fields
            defaults = {}
            for key, value in record.items():
                if key in model_fields and key != identifier_field:
                    # Convert values if needed
                    if isinstance(value, bool) or isinstance(value, int) or isinstance(value, str):
                        defaults[key] = value
            
            # Create or update
            obj, created = model_class.objects.update_or_create(
                **{identifier_field: identifier_value},
                defaults=defaults
            )
            
            if created:
                self.created_count += 1
            else:
                self.updated_count += 1
            
            logger.info(f"{'Created' if created else 'Updated'} {model_class.__name__}: {identifier_value[:50] if isinstance(identifier_value, str) else identifier_value}...")
            return True
        
        except Exception as e:
            error_msg = f"Error processing {model_class.__name__}: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False
    
    def import_data(self) -> Dict[str, Any]:
        """Main import method"""
        print("\n" + "="*80)
        print(f"🚀 [IMPORT_DATA] import_data() MAIN METHOD STARTED")
        print(f"   Table: {self.table_name}")
        print(f"   JSON Data Size: {len(self.json_data)} chars")
        print("="*80)
        
        result = {
            'success': False,
            'created': 0,
            'updated': 0,
            'errors': [],
            'message': ''
        }
        
        # Parse JSON
        print(f"\n[STEP 1] PARSING JSON")
        print(f"   Calling parse_json()...")
        if not self.parse_json():
            print(f"   ❌ JSON PARSE FAILED")
            result['errors'] = self.errors
            result['message'] = f"Failed to parse JSON: {self.errors[0]}"
            print(f"   Message: {result['message']}")
            return result
        print(f"   ✅ JSON PARSED - {len(self.records)} records extracted\n")
        
        # Get model class
        print(f"[STEP 2] GETTING MODEL CLASS")
        print(f"   Calling get_model_class() for table: {self.table_name}...")
        try:
            model_class = self.get_model_class()
            print(f"   ✅ Model class obtained: {model_class.__name__}\n")
        except Exception as e:
            print(f"   ❌ FAILED to get model class")
            result['errors'] = [str(e)]
            result['message'] = f"Failed to get model class: {str(e)}"
            print(f"   Message: {result['message']}")
            logger.error(f"Model class error: {str(e)}")
            return result
        
        # Process each record
        print(f"[STEP 3] PROCESSING RECORDS")
        print(f"   Total records to process: {len(self.records)}\n")
        
        for idx, record in enumerate(self.records, 1):
            print(f"\n   ['RECORD {idx}/{len(self.records)}]")
            
            if not isinstance(record, dict):
                print(f"      ❌ Record is not a dict: {type(record)}")
                self.errors.append(f"Record {idx} is not a dict: {type(record)}")
                continue
            
            # Use specific processor based on table name
            if self.table_name == 'currentaffairs_mcq':
                print(f"      [ROUTE] → process_currentaffairs_mcq()")
                self.process_currentaffairs_mcq(record, model_class)
            elif self.table_name == 'currentaffairs_descriptive':
                print(f"      [ROUTE] → process_currentaffairs_descriptive()")
                self.process_currentaffairs_descriptive(record, model_class)
            elif self.table_name == 'current_affairs_slide':
                print(f"      [ROUTE] → process_current_affairs_slide()")
                self.process_current_affairs_slide(record, model_class)
            else:
                print(f"      [ROUTE] → process_generic_model()")
                self.process_generic_model(record, model_class)
        
        # Prepare final result
        print(f"\n[STEP 4] FINALIZING RESULTS")
        result['success'] = len(self.errors) == 0
        result['created'] = self.created_count
        result['updated'] = self.updated_count
        result['errors'] = self.errors
        result['message'] = f"Import completed! Created: {self.created_count}, Updated: {self.updated_count}, Errors: {len(self.errors)}"
        
        print(f"   Created Records: {self.created_count}")
        print(f"   Updated Records: {self.updated_count}")
        print(f"   Total Errors: {len(self.errors)}")
        print(f"   Success: {result['success']}")
        
        if self.errors:
            print(f"\n   Errors encountered:")
            for err in self.errors[:5]:
                print(f"      - {err}")
            if len(self.errors) > 5:
                print(f"      ... and {len(self.errors) - 5} more errors")
        
        print(f"\n✅ [IMPORT_DATA] COMPLETED")
        print("="*80 + "\n")
        logger.info(result['message'])
        return result
