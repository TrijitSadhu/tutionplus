"""
Save handlers for different content types (Subject MCQ, Current Affairs MCQ, Current Affairs Descriptive)
Manages database saving with proper field mapping, date handling, and category Boolean flags
"""

from django.utils import timezone
from django.contrib.auth import get_user_model
from bank.models import currentaffairs_mcq, currentaffairs_descriptive

User = get_user_model()

# ==================== CATEGORY MAPPING ====================
# Maps LLM category names to CurrentAffairsMCQ/Descriptive field names
CATEGORY_MAPPING = {
    'Science and Technology': 'Science_Techonlogy',  # Note: original typo in model
    'Science_Technology': 'Science_Techonlogy',
    'National': 'National',
    'International': 'International',
    'Business': 'Business',
    'Sports': 'Sports',
    'Environment': 'Environment',
    'Defence': 'Defence',
    'Politics': 'Politics',
    'Law and Justice': 'Law_and_Justice',
    'Health': 'Health',
    'Economy': 'Economy',
    'Agriculture': 'Agriculture',
    'Culture': 'Culture',
    'Social': 'Social',
    'Scheme': 'Scheme',
    'Report': 'Report',
    'Awards': 'Awards',
    'Person': 'Person',
}

def set_category_flags(instance, categories_list):
    """
    Set Boolean category flags on model instance based on LLM response categories
    
    Args:
        instance: CurrentAffairsMCQ or CurrentAffairsDescriptive model instance
        categories_list: List of category strings from LLM response
    """
    # Set all categories to False first
    for db_field in CATEGORY_MAPPING.values():
        setattr(instance, db_field, False)
    
    # Set matching categories to True
    if categories_list:
        for category in categories_list:
            # Try exact match first
            if category in CATEGORY_MAPPING:
                db_field = CATEGORY_MAPPING[category]
                setattr(instance, db_field, True)
            else:
                # Try case-insensitive match
                for orig, db_field in CATEGORY_MAPPING.items():
                    if orig.lower() == str(category).lower():
                        setattr(instance, db_field, True)
                        break


def get_date_and_year(processing_log, response_data=None):
    """
    Determine ca_date and ca_year based on processing_log and response
    
    Modes:
    1. ca_auto_date=False: Use user-provided ca_date and ca_year
    2. ca_auto_date=True: Try to extract from response, fallback to today/current year
    
    Args:
        processing_log: ProcessingLog instance
        response_data: Dictionary from LLM with potential date/year fields
    
    Returns:
        tuple: (ca_date, ca_year)
    """
    today = timezone.now().date()
    current_year = str(today.year)
    
    if processing_log.ca_auto_date and response_data:
        # LLM decides - try to extract from response
        ca_date = response_data.get('date')
        ca_year = response_data.get('year')
        
        # Fallback to today if not provided
        if not ca_date:
            ca_date = today
        if not ca_year:
            ca_year = current_year
    else:
        # User provides or use defaults
        ca_date = processing_log.ca_date or today
        ca_year = processing_log.ca_year or current_year
    
    # Ensure types
    if isinstance(ca_year, int):
        ca_year = str(ca_year)
    
    return ca_date, ca_year


def save_currentaffairs_mcq(mcq_data, processing_log, created_by):
    """
    Save Current Affairs MCQ from LLM response to database
    
    Args:
        mcq_data: Dictionary with {questions: [...], categories: [...]} from LLM
        processing_log: ProcessingLog instance containing metadata
        created_by: User instance
    
    Returns:
        list: Saved CurrentAffairsMCQ instances
    """
    print(f"[CA MCQ] Starting to save MCQs from LLM response...")
    saved_items = []
    
    questions = mcq_data.get('questions', [])
    print(f"  - Found {len(questions)} questions in response")
    
    # Get date and year
    ca_date, ca_year = get_date_and_year(processing_log, mcq_data)
    print(f"  - Using date: {ca_date}, year: {ca_year}")
    
    for idx, question_data in enumerate(questions, 1):
        try:
            # Extract fields with defaults - handle both 'option_1' and 'option_a' formats
            question = question_data.get('question', '')
            option_1 = (question_data.get('option_1', '') or 
                       question_data.get('option_a', '') or 
                       question_data.get('options', {}).get('A', '') or
                       question_data.get('options', {}).get('a', ''))
            option_2 = (question_data.get('option_2', '') or 
                       question_data.get('option_b', '') or 
                       question_data.get('options', {}).get('B', '') or
                       question_data.get('options', {}).get('b', ''))
            option_3 = (question_data.get('option_3', '') or 
                       question_data.get('option_c', '') or 
                       question_data.get('options', {}).get('C', '') or
                       question_data.get('options', {}).get('c', ''))
            option_4 = (question_data.get('option_4', '') or 
                       question_data.get('option_d', '') or 
                       question_data.get('options', {}).get('D', '') or
                       question_data.get('options', {}).get('d', ''))
            
            # Normalize answer format (A/B/C/D or 1/2/3/4 → 1/2/3/4)
            correct_answer = question_data.get('correct_answer', '')
            if correct_answer.upper() in ['A', 'B', 'C', 'D']:
                correct_answer = str(ord(correct_answer.upper()) - ord('A') + 1)
            elif correct_answer.lower() == 'option_1':
                correct_answer = '1'
            elif correct_answer.lower() == 'option_2':
                correct_answer = '2'
            elif correct_answer.lower() == 'option_3':
                correct_answer = '3'
            elif correct_answer.lower() == 'option_4':
                correct_answer = '4'
            
            extra = question_data.get('extra', question_data.get('explanation', ''))
            
            # Create model instance
            mcq = currentaffairs_mcq(
                question=question,
                option_1=option_1,
                option_2=option_2,
                option_3=option_3,
                option_4=option_4,
                ans=correct_answer,
                extra=extra,
                day=ca_date,  # Use 'day' field instead of 'ca_date'
                year_now=ca_year,
            )
            
            # Set category Boolean flags
            categories = question_data.get('categories', [])
            set_category_flags(mcq, categories)
            print(f"  - Question {idx}: ✓ Created MCQ with {len(categories)} categories")
            
            # Save to database
            mcq.save()
            saved_items.append(mcq)
            
        except Exception as e:
            print(f"  - Question {idx}: ✗ Error - {str(e)}")
            continue
    
    print(f"\n  ✓ Successfully saved {len(saved_items)}/{len(questions)} MCQs\n")
    return saved_items


def save_currentaffairs_descriptive(desc_data, processing_log, created_by):
    """
    Save Current Affairs Descriptive from LLM response to database
    
    Args:
        desc_data: Dictionary with {upper_heading, yellow_heading, key_1-4, 
                   all_key_points, categories} from LLM
        processing_log: ProcessingLog instance containing metadata
        created_by: User instance
    
    Returns:
        list: Saved CurrentAffairsDescriptive instances (usually just 1)
    """
    print(f"[CA Descriptive] Starting to save descriptive content from LLM response...")
    saved_items = []
    
    try:
        # Get date and year
        ca_date, ca_year = get_date_and_year(processing_log, desc_data)
        print(f"  - Using date: {ca_date}, year: {ca_year}")
        
        # Extract fields
        upper_heading = desc_data.get('upper_heading', '')
        yellow_heading = desc_data.get('yellow_heading', '')
        key_1 = desc_data.get('key_1', '')
        key_2 = desc_data.get('key_2', '')
        key_3 = desc_data.get('key_3', '')
        key_4 = desc_data.get('key_4', '')
        
        # all_key_points should be formatted with /// separator
        all_key_points = desc_data.get('all_key_points', '')
        if isinstance(all_key_points, list):
            # If LLM returns as list, join with ///
            all_key_points = '///'.join(all_key_points)
        
        print(f"  - Upper heading: {upper_heading[:50]}...")
        print(f"  - Yellow heading: {yellow_heading[:50]}...")
        print(f"  - Key points count: {all_key_points.count('//') + 1}")
        
        # Create model instance
        descriptive = currentaffairs_descriptive(
            upper_heading=upper_heading,
            yellow_heading=yellow_heading,
            key_1=key_1,
            key_2=key_2,
            key_3=key_3,
            key_4=key_4,
            all_key_points=all_key_points,
            day=ca_date,  # Use 'day' field instead of 'ca_date'
            year_now=ca_year,
        )
        
        # Set category Boolean flags
        categories = desc_data.get('categories', [])
        set_category_flags(descriptive, categories)
        print(f"  - Descriptive: ✓ Created with {len(categories)} categories")
        
        # Save to database
        descriptive.save()
        saved_items.append(descriptive)
        
        print(f"\n  ✓ Successfully saved descriptive content\n")
        
    except Exception as e:
        print(f"  - ✗ Error saving descriptive: {str(e)}\n")
    
    return saved_items
