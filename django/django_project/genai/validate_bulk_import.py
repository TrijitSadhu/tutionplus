"""
Validation and Testing Script for Bulk Import All Subjects
Run this to verify everything is working correctly
"""

import os
import sys
import json
import logging
from datetime import datetime, date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
import django
django.setup()

from genai.bulk_import_all_subjects import SubjectBulkImporter, bulk_import_subject
from django.apps import apps

logger = logging.getLogger(__name__)


class BulkImportValidator:
    """Validate bulk import system for all subjects"""
    
    def __init__(self):
        self.results = []
        self.errors = []
        self.subject_config = SubjectBulkImporter.SUBJECT_CONFIG
    
    def test_subject_availability(self):
        """Test that all configured subjects exist as models"""
        print("\n" + "="*70)
        print("TEST 1: Subject Model Availability")
        print("="*70)
        
        passed = 0
        failed = 0
        
        for subject, config in self.subject_config.items():
            try:
                model = apps.get_model(config['app_label'], config['model_name'])
                print(f"  ✅ {subject:30s} - Model found: {config['model_name']}")
                passed += 1
            except Exception as e:
                print(f"  ❌ {subject:30s} - Error: {str(e)}")
                failed += 1
                self.errors.append(f"{subject}: {str(e)}")
        
        print(f"\n  RESULT: {passed} passed, {failed} failed")
        self.results.append({
            'test': 'Subject Availability',
            'passed': passed,
            'failed': failed,
            'status': 'PASS' if failed == 0 else 'FAIL'
        })
    
    def test_polity_import(self):
        """Test import for Polity subject"""
        print("\n" + "="*70)
        print("TEST 2: Polity MCQ Import")
        print("="*70)
        
        json_data = json.dumps([
            {
                "question": "TEST: Which article deals with Fundamental Rights?",
                "option_1": "Articles 12-35",
                "option_2": "Articles 36-51",
                "option_3": "Articles 52-62",
                "option_4": "Articles 1-11",
                "option_5": "None",
                "ans": 1,
                "chapter": "1",
                "difficulty": "easy"
            },
            {
                "question": "TEST: How many states in India?",
                "option_1": "28",
                "option_2": "29",
                "option_3": "30",
                "option_4": "31",
                "option_5": "32",
                "ans": 2,
                "chapter": "2",
                "difficulty": "easy"
            }
        ])
        
        try:
            result = bulk_import_subject('polity', json_data, date.today())
            print(f"\n  Result: {result['message']}")
            print(f"  Created: {result['created']}")
            print(f"  Updated: {result['updated']}")
            print(f"  Errors: {len(result['errors'])}")
            
            if result['errors']:
                for error in result['errors']:
                    print(f"    - {error}")
            
            status = 'PASS' if result['success'] and result['created'] >= 2 else 'FAIL'
            print(f"\n  Status: {status}")
            self.results.append({'test': 'Polity Import', 'status': status})
            
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            self.errors.append(f"Polity import: {str(e)}")
            self.results.append({'test': 'Polity Import', 'status': 'FAIL'})
    
    def test_history_import(self):
        """Test import for History subject"""
        print("\n" + "="*70)
        print("TEST 3: History MCQ Import")
        print("="*70)
        
        json_data = json.dumps([
            {
                "question": "TEST: In which year did the Rebellion of 1857 occur?",
                "option_1": "1855",
                "option_2": "1856",
                "option_3": "1857",
                "option_4": "1858",
                "option_5": "1859",
                "ans": 3,
                "chapter": "1",
                "difficulty": "easy"
            }
        ])
        
        try:
            result = bulk_import_subject('history', json_data, date.today())
            print(f"  Result: {result['message']}")
            print(f"  Created: {result['created']}")
            status = 'PASS' if result['success'] else 'FAIL'
            self.results.append({'test': 'History Import', 'status': status})
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            self.results.append({'test': 'History Import', 'status': 'FAIL'})
    
    def test_currentaffairs_mcq_import(self):
        """Test import for Current Affairs MCQ"""
        print("\n" + "="*70)
        print("TEST 4: Current Affairs MCQ Import")
        print("="*70)
        
        json_data = json.dumps([
            {
                "question": "TEST: What is the latest news?",
                "option_1": "Option 1",
                "option_2": "Option 2",
                "option_3": "Option 3",
                "option_4": "Option 4",
                "ans": 1,
                "categories": ["National", "Business_Economy_Banking"],
                "explanation": "Test explanation"
            }
        ])
        
        try:
            result = bulk_import_subject('currentaffairs_mcq', json_data, date.today())
            print(f"  Result: {result['message']}")
            print(f"  Created: {result['created']}")
            status = 'PASS' if result['success'] else 'FAIL'
            self.results.append({'test': 'CA MCQ Import', 'status': status})
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            self.results.append({'test': 'CA MCQ Import', 'status': 'FAIL'})
    
    def test_currentaffairs_descriptive_import(self):
        """Test import for Current Affairs Descriptive"""
        print("\n" + "="*70)
        print("TEST 5: Current Affairs Descriptive Import")
        print("="*70)
        
        json_data = json.dumps([
            {
                "upper_heading": "TEST: Latest News",
                "yellow_heading": "Sub topic",
                "key_1": "Key point 1",
                "key_2": "Key point 2",
                "key_3": "Key point 3",
                "key_4": "Key point 4",
                "all_key_points": "All points combined",
                "categories": ["National", "International"]
            }
        ])
        
        try:
            result = bulk_import_subject('currentaffairs_descriptive', json_data, date.today())
            print(f"  Result: {result['message']}")
            print(f"  Created: {result['created']}")
            status = 'PASS' if result['success'] else 'FAIL'
            self.results.append({'test': 'CA Descriptive Import', 'status': status})
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            self.results.append({'test': 'CA Descriptive Import', 'status': 'FAIL'})
    
    def test_date_handling(self):
        """Test date handling with and without JSON dates"""
        print("\n" + "="*70)
        print("TEST 6: Date Handling")
        print("="*70)
        
        # Test with JSON dates
        json_with_dates = json.dumps([{
            "question": "TEST: Date in JSON",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "option_5": "E",
            "ans": 1,
            "chapter": "1",
            "year_now": "2025",
            "month": "December",
            "day": "2025-12-25"
        }])
        
        # Test without JSON dates
        json_without_dates = json.dumps([{
            "question": "TEST: No date in JSON",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "option_5": "E",
            "ans": 2,
            "chapter": "1"
        }])
        
        try:
            # Import with dates
            result1 = bulk_import_subject('polity', json_with_dates, date(2026, 1, 28))
            status1 = 'PASS' if result1['success'] else 'FAIL'
            print(f"  With JSON dates: {status1}")
            
            # Import without dates
            result2 = bulk_import_subject('polity', json_without_dates, date(2026, 1, 28))
            status2 = 'PASS' if result2['success'] else 'FAIL'
            print(f"  Without JSON dates (uses form date): {status2}")
            
            overall_status = 'PASS' if status1 == 'PASS' and status2 == 'PASS' else 'FAIL'
            self.results.append({'test': 'Date Handling', 'status': overall_status})
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            self.results.append({'test': 'Date Handling', 'status': 'FAIL'})
    
    def test_json_validation(self):
        """Test JSON validation"""
        print("\n" + "="*70)
        print("TEST 7: JSON Validation")
        print("="*70)
        
        invalid_json = "{ invalid json }"
        
        try:
            importer = SubjectBulkImporter('polity', invalid_json, date.today())
            if not importer.parse_json():
                print("  ✅ Invalid JSON correctly rejected")
                self.results.append({'test': 'JSON Validation', 'status': 'PASS'})
            else:
                print("  ❌ Invalid JSON not caught")
                self.results.append({'test': 'JSON Validation', 'status': 'FAIL'})
        except Exception as e:
            print(f"  ✅ Invalid JSON caught: {str(e)[:50]}")
            self.results.append({'test': 'JSON Validation', 'status': 'PASS'})
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*70)
        print("FINAL REPORT")
        print("="*70)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"\nTests Executed: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%\n")
        
        print("Test Results:")
        print("-" * 70)
        for result in self.results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            test_name = result['test']
            print(f"  {status_icon} {test_name:40s} {result['status']}")
        
        if self.errors:
            print("\nErrors:")
            print("-" * 70)
            for error in self.errors:
                print(f"  - {error}")
        
        print("\n" + "="*70)
        if failed_tests == 0:
            print("✅ ALL TESTS PASSED - System is ready for production!")
        else:
            print(f"⚠️  {failed_tests} TEST(S) FAILED - Review errors above")
        print("="*70 + "\n")
        
        return passed_tests == total_tests


def run_validation():
    """Run all validation tests"""
    print("\n" + "="*70)
    print("🧪 BULK IMPORT SYSTEM VALIDATION")
    print("   Testing all subjects and functionality")
    print("="*70)
    
    validator = BulkImportValidator()
    
    # Run tests
    validator.test_subject_availability()
    validator.test_polity_import()
    validator.test_history_import()
    validator.test_currentaffairs_mcq_import()
    validator.test_currentaffairs_descriptive_import()
    validator.test_date_handling()
    validator.test_json_validation()
    
    # Generate report
    success = validator.generate_report()
    
    return success


if __name__ == '__main__':
    try:
        success = run_validation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Validation error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
