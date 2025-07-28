"""
EMR Parser Test Script

This script allows candidates to test the EMR parser functions individually
outside of the chat agent flow.

Usage:
    poetry runpython tests/test_emr_parser.py [function_name]

Available functions:
    - parse_synthea_patient
    - extract_chronic_conditions  
    - extract_vital_events
    - all (tests all functions)
"""

import sys
import os
import traceback

# Add the parent directory to the path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.emr_parser import (
    initialize_emr_data,
    parse_synthea_patient,
    extract_chronic_conditions,
    extract_vital_events,
    load_sample_synthea_data
)


def test_parse_synthea_patient():
    """Test the parse_synthea_patient function"""
    print("=" * 60)
    print("Testing parse_synthea_patient function")
    print("=" * 60)
    
    try:
        # Load sample data
        print("Loading sample Synthea data...")
        synthea_data = load_sample_synthea_data()
        
        if not synthea_data:
            print("❌ Failed to load sample data")
            return False
        
        print(f"✅ Loaded sample data")
        
        # Test parsing
        print("\nParsing Synthea patient data...")
        patient_profile = parse_synthea_patient(synthea_data)
        
        print(f"✅ Patient ID: {patient_profile.patient_id}")
        print(f"✅ Chronic conditions: {len(patient_profile.chronic_conditions)}")
        print(f"✅ Health events: {len(patient_profile.health_events)}")
        print(f"✅ Medications: {len(patient_profile.medications)}")
        
        # Show some details if data exists
        if patient_profile.chronic_conditions:
            print("\nChronic conditions found:")
            for condition in patient_profile.chronic_conditions[:3]:  # Show first 3
                print(f"  - {condition.description} ({condition.status})")
        
        if patient_profile.health_events:
            print("\nHealth events found:")
            for event in patient_profile.health_events[:3]:  # Show first 3
                date_str = event.date.strftime("%Y-%m-%d") if event.date else "Unknown"
                print(f"  - {event.description} ({event.event_type}) on {date_str}")
        
        return True
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ Error testing parse_synthea_patient: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return False


def test_extract_chronic_conditions():
    """Test the extract_chronic_conditions function"""
    print("=" * 60)
    print("Testing extract_chronic_conditions function")
    print("=" * 60)
    
    try:
        # Initialize EMR data first
        print("Initializing EMR data...")
        initialize_emr_data()
        
        # Test extraction
        print("\nExtracting chronic conditions...")
        chronic_conditions = extract_chronic_conditions("test_user_id")
        
        print(f"✅ Found {len(chronic_conditions)} chronic conditions")
        
        if chronic_conditions:
            print("\nChronic conditions:")
            for i, condition in enumerate(chronic_conditions, 1):
                onset_str = condition.onset_date.strftime("%Y-%m-%d") if condition.onset_date else "Unknown"
                severity_str = f" (Severity: {condition.severity})" if condition.severity else ""
                print(f"  {i}. {condition.description}")
                print(f"     Code: {condition.code}")
                print(f"     Status: {condition.status}")
                print(f"     Onset: {onset_str}{severity_str}")
                print()
        else:
            print("No chronic conditions found")
        
        return True
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ Error testing extract_chronic_conditions: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return False


def test_extract_vital_events():
    """Test the extract_vital_events function"""
    print("=" * 60)
    print("Testing extract_vital_events function")
    print("=" * 60)
    
    try:
        # Initialize EMR data first
        print("Initializing EMR data...")
        initialize_emr_data()
        
        # Test extraction
        print("\nExtracting vital events...")
        vital_events = extract_vital_events("test_user_id")
        
        print(f"✅ Found {len(vital_events)} vital events")
        
        if vital_events:
            print("\nVital events:")
            for i, event in enumerate(vital_events, 1):
                date_str = event.date.strftime("%Y-%m-%d") if event.date else "Unknown"
                provider_str = f" at {event.provider}" if event.provider else ""
                code_str = f" (Code: {event.code})" if event.code else ""
                print(f"  {i}. {event.description}")
                print(f"     Type: {event.event_type}")
                print(f"     Date: {date_str}{provider_str}{code_str}")
                print()
        else:
            print("No vital events found")
        
        return True
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ Error testing extract_vital_events: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return False


def test_all():
    """Test all EMR parser functions"""
    print("Testing all EMR parser functions...\n")
    
    results = []
    results.append(("parse_synthea_patient", test_parse_synthea_patient()))
    results.append(("extract_chronic_conditions", test_extract_chronic_conditions()))
    results.append(("extract_vital_events", test_extract_vital_events()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for function_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{function_name}: {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")


def main():
    """Main function to run tests based on command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python test_emr_parser.py [function_name]")
        print("\nAvailable functions:")
        print("  - parse_synthea_patient")
        print("  - extract_chronic_conditions")
        print("  - extract_vital_events")
        print("  - all")
        return
    
    function_name = sys.argv[1].lower()
    
    if function_name == "parse_synthea_patient":
        test_parse_synthea_patient()
    elif function_name == "extract_chronic_conditions":
        test_extract_chronic_conditions()
    elif function_name == "extract_vital_events":
        test_extract_vital_events()
    elif function_name == "all":
        test_all()
    else:
        print(f"Unknown function: {function_name}")
        print("Available functions: parse_synthea_patient, extract_chronic_conditions, extract_vital_events, all")


if __name__ == "__main__":
    main() 