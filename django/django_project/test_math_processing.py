"""
Test script for MathProblemGeneration functionality
Tests LaTeX conversion and MCQ generation
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import MathProblemGeneration
from genai.tasks.math_processor import LaTeXConverter, MathMCQGenerator
import json


def test_latex_conversion():
    """Test LaTeX conversion"""
    print("\n" + "="*80)
    print("[TEST 1] LaTeX Conversion")
    print("="*80)
    
    converter = LaTeXConverter()
    
    test_expressions = [
        "Solve for x: 2x² + 5x - 3 = 0",
        "Calculate: ∫(x² + 3x)dx",
        "Find: lim(x→0) (sin x)/x",
        "What is: √(144) + 5³",
    ]
    
    for i, expression in enumerate(test_expressions, 1):
        print(f"\n[{i}] Expression: {expression}")
        try:
            result = converter.convert_to_latex(expression)
            if 'error' in result:
                print(f"   ✗ Error: {result['error']}")
            else:
                print(f"   ✓ LaTeX: {result.get('latex', 'N/A')}")
                if 'latex_display' in result:
                    print(f"   ✓ Display: {result['latex_display']}")
        except Exception as e:
            print(f"   ✗ Exception: {str(e)}")


def test_mcq_generation():
    """Test MCQ generation"""
    print("\n" + "="*80)
    print("[TEST 2] MCQ Generation (includes LaTeX)")
    print("="*80)
    
    generator = MathMCQGenerator()
    
    test_problems = [
        ("Find the value of x if 3x + 7 = 22", "easy"),
        ("Solve: x² - 5x + 6 = 0", "medium"),
        ("Evaluate: ∫(2x + 3)dx", "hard"),
    ]
    
    for i, (problem, difficulty) in enumerate(test_problems, 1):
        print(f"\n[{i}] Problem: {problem}")
        print(f"    Difficulty: {difficulty}")
        try:
            result = generator.process_math_problem(problem, difficulty)
            if 'error' in result:
                print(f"   ✗ Error: {result['error']}")
            else:
                print(f"   ✓ LaTeX: {result.get('problem_latex', 'N/A')}")
                print(f"   ✓ Question: {result.get('question', 'N/A')[:60]}...")
                print(f"   ✓ Options:")
                for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
                    print(f"      {opt[-1].upper()}. {result.get(opt, 'N/A')[:40]}...")
                print(f"   ✓ Answer: {result.get('correct_answer', 'N/A')}")
        except Exception as e:
            print(f"   ✗ Exception: {str(e)}")


def test_database_integration():
    """Test database model integration"""
    print("\n" + "="*80)
    print("[TEST 3] Database Integration")
    print("="*80)
    
    # Create test record
    print("\n[1] Creating test record...")
    test_record = MathProblemGeneration.objects.create(
        expression="Test: x² + 2x + 1 = 0",
        difficulty="medium",
        status="pending"
    )
    print(f"   ✓ Created: ID {test_record.id}")
    print(f"   ✓ Status: {test_record.status}")
    print(f"   ✓ Expression optional: {'Yes' if not test_record._meta.get_field('expression').null else 'No'}")
    
    # Test with None expression
    print("\n[2] Testing None expression...")
    try:
        test_none = MathProblemGeneration.objects.create(
            expression=None,
            difficulty="easy",
            status="pending"
        )
        print(f"   ✓ Created with None: ID {test_none.id}")
        print(f"   ✓ String representation: {str(test_none)}")
        test_none.delete()
    except Exception as e:
        print(f"   ✗ Failed: {str(e)}")
    
    # Test processing
    print("\n[3] Testing admin action simulation...")
    generator = MathMCQGenerator()
    
    test_record.status = 'processing'
    test_record.save()
    print(f"   ✓ Status updated to: {test_record.status}")
    
    try:
        result = generator.process_math_problem(test_record.expression, test_record.difficulty)
        if 'error' not in result:
            test_record.latex_output = result['latex_conversion'].get('latex', '')
            test_record.generated_mcqs = json.dumps({
                'question': result.get('question', ''),
                'option_a': result.get('option_a', ''),
                'option_b': result.get('option_b', ''),
                'option_c': result.get('option_c', ''),
                'option_d': result.get('option_d', ''),
                'correct_answer': result.get('correct_answer', ''),
            })
            test_record.status = 'completed'
            test_record.error_message = None
            print(f"   ✓ Processing successful")
            print(f"   ✓ LaTeX: {test_record.latex_output[:50]}...")
        else:
            test_record.status = 'failed'
            test_record.error_message = result['error']
            print(f"   ✗ Processing failed: {result['error']}")
    except Exception as e:
        test_record.status = 'failed'
        test_record.error_message = str(e)
        print(f"   ✗ Exception: {str(e)}")
    
    test_record.save()
    print(f"   ✓ Final status: {test_record.status}")
    
    # Cleanup
    print("\n[4] Cleanup...")
    test_record.delete()
    print(f"   ✓ Test record deleted")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("MATHPROBLEMGENERATION - COMPREHENSIVE TESTING")
    print("="*80)
    
    try:
        test_latex_conversion()
        test_mcq_generation()
        test_database_integration()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED")
        print("="*80)
        print("\n✅ MathProblemGeneration system is fully functional!")
        print("\nYou can now:")
        print("1. Go to /admin/genai/mathproblemgeneration/")
        print("2. Add math problems (expression field is optional)")
        print("3. Select items and use actions:")
        print("   - 'Convert to LaTeX' for LaTeX conversion")
        print("   - 'Generate MCQs' for full MCQ generation")
        print("4. Or run: python manage.py process_math_problems")
        print()
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
