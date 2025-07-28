"""
Wearables Analytics Test Script

This script allows candidates to test the wearables analytics functions individually
outside of the chat agent flow.

Usage:
    poetry run python tests/test_wearables_analytics.py [function_name] [user_id]

Available functions:
    - analyze_heartrate_trends
    - analyze_glucose_trends
    - all (tests all functions)

Note: You'll need to set up your environment variables (VITAL_API_KEY, etc.)
before running these tests.
"""

import sys
import os
import traceback

# Add the parent directory to the path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.wearables_analytics import (
    analyze_heartrate_trends,
    analyze_glucose_trends,
    get_heartrate_data,
    get_glucose_data
)


def test_analyze_heartrate_trends(user_id: str):
    """Test the analyze_heartrate_trends function"""
    print("=" * 60)
    print("Testing analyze_heartrate_trends function")
    print("=" * 60)
    
    try:
        print(f"Analyzing heartrate trends for user: {user_id}")
        
        # Test the analysis
        heartrate_analysis = analyze_heartrate_trends(user_id)
        
        if not heartrate_analysis:
            print("❌ No heartrate analysis returned (likely no data available)")
            return False
        
        print("✅ Heartrate analysis completed successfully")
        
        # Display results
        print(f"\nResults for user {user_id}:")
        print(f"- Resting HR trend: {heartrate_analysis.resting_hr_trend.trend_direction.value}")
        print(f"  - Average value: {heartrate_analysis.resting_hr_trend.average_value:.1f} bpm")
        print(f"  - Confidence: {heartrate_analysis.resting_hr_trend.confidence_score:.1%}")
        
        print(f"- Max HR trend: {heartrate_analysis.max_hr_trend.trend_direction.value}")
        print(f"  - Average value: {heartrate_analysis.max_hr_trend.average_value:.1f} bpm")
        print(f"  - Confidence: {heartrate_analysis.max_hr_trend.confidence_score:.1%}")
        
        if heartrate_analysis.hrv_trend:
            print(f"- HRV trend: {heartrate_analysis.hrv_trend.trend_direction.value}")
            print(f"  - Average value: {heartrate_analysis.hrv_trend.average_value:.1f} ms")
            print(f"  - Confidence: {heartrate_analysis.hrv_trend.confidence_score:.1%}")
        else:
            print("- HRV trend: No data available")
        
        print(f"- Anomalies detected: {heartrate_analysis.anomaly_count}")
        
        if heartrate_analysis.risk_factors:
            print(f"- Risk factors: {', '.join(heartrate_analysis.risk_factors)}")
        else:
            print("- Risk factors: None identified")
        
        return True
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ Error testing analyze_heartrate_trends: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return False


def test_analyze_glucose_trends(user_id: str):
    """Test the analyze_glucose_trends function"""
    print("=" * 60)
    print("Testing analyze_glucose_trends function")
    print("=" * 60)
    
    try:
        print(f"Analyzing glucose trends for user: {user_id}")
        
        # Test the analysis
        glucose_analysis = analyze_glucose_trends(user_id)
        
        if not glucose_analysis:
            print("❌ No glucose analysis returned (likely no data available)")
            return False
        
        print("✅ Glucose analysis completed successfully")
        
        # Display results
        print(f"\nResults for user {user_id}:")
        print(f"- Average glucose trend: {glucose_analysis.average_glucose_trend.trend_direction.value}")
        print(f"  - Average value: {glucose_analysis.average_glucose_trend.average_value:.1f} mg/dL")
        print(f"  - Confidence: {glucose_analysis.average_glucose_trend.confidence_score:.1%}")

        print(f"- Time in range trend: {glucose_analysis.time_in_range_trend.trend_direction.value}")
        print(f"  - Average value: {glucose_analysis.time_in_range_trend.average_value:.1f}%")
        print(f"  - Confidence: {glucose_analysis.time_in_range_trend.confidence_score:.1%}")
        
        print(f"- Variability trend: {glucose_analysis.variability_trend.trend_direction.value}")
        print(f"  - Average value: {glucose_analysis.variability_trend.average_value:.1f}")
        print(f"  - Confidence: {glucose_analysis.variability_trend.confidence_score:.1%}")
        
        if glucose_analysis.dawn_phenomenon_severity is not None:
            print(f"- Dawn phenomenon severity: {glucose_analysis.dawn_phenomenon_severity:.1f}")
        else:
            print("- Dawn phenomenon severity: Not detected")
        
        print(f"- Hypoglycemic episodes: {glucose_analysis.hypo_episodes}")
        print(f"- Hyperglycemic episodes: {glucose_analysis.hyper_episodes}")
        
        if glucose_analysis.risk_factors:
            print(f"- Risk factors: {', '.join(glucose_analysis.risk_factors)}")
        else:
            print("- Risk factors: None identified")
        
        return True
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ Error testing analyze_glucose_trends: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return False


def test_raw_data_functions(user_id: str):
    """Test the raw data retrieval functions"""
    print("=" * 60)
    print("Testing raw data retrieval functions")
    print("=" * 60)
    
    try:
        print(f"Testing data retrieval for user: {user_id}")
        
        # Test heartrate data retrieval
        print("\nRetrieving heartrate data...")
        heartrate_data = get_heartrate_data(user_id)
        if heartrate_data:
            print(f"✅ Heartrate data retrieved: {len(heartrate_data)} data points")
            if len(heartrate_data) > 0:
                print(f"   Sample data point: {heartrate_data[0]}")
        else:
            print("❌ No heartrate data available")
        
        # Test glucose data retrieval
        print("\nRetrieving glucose data...")
        glucose_data = get_glucose_data(user_id)
        if glucose_data:
            print(f"✅ Glucose data retrieved: {len(glucose_data)} data points")
            if len(glucose_data) > 0:
                print(f"   Sample data point: {glucose_data[0]}")
        else:
            print("❌ No glucose data available")
        
        return True
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"❌ Error testing raw data functions: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return False


def test_all(user_id: str):
    """Test all wearables analytics functions"""
    print("Testing all wearables analytics functions...\n")
    
    results = []
    results.append(("Raw data retrieval", test_raw_data_functions(user_id)))
    results.append(("analyze_heartrate_trends", test_analyze_heartrate_trends(user_id)))
    results.append(("analyze_glucose_trends", test_analyze_glucose_trends(user_id)))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for function_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{function_name}: {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")


def check_environment():
    """Check if required environment variables are set"""
    print("Checking environment setup...")
    
    required_vars = ["VITAL_API_KEY", "VITAL_ENV", "VITAL_REGION"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the tests.")
        return False
    else:
        print("✅ All required environment variables are set")
        return True


def main():
    """Main function to run tests based on command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python test_wearables_analytics.py [function_name] [user_id]")
        print("\nAvailable functions:")
        print("  - analyze_heartrate_trends")
        print("  - analyze_glucose_trends")
        print("  - all")
        print("\nExample:")
        print("  python test_wearables_analytics.py analyze_heartrate_trends user123")
        print("  python test_wearables_analytics.py all user123")
        return
    
    # Check environment first
    if not check_environment():
        return
    
    function_name = sys.argv[1].lower()
    user_id = sys.argv[2] if len(sys.argv) > 2 else "19f6cb0b-b067-4b25-af6b-3df9ebd91440"
    
    if function_name == "analyze_heartrate_trends":
        test_analyze_heartrate_trends(user_id)
    elif function_name == "analyze_glucose_trends":
        test_analyze_glucose_trends(user_id)
    elif function_name == "all":
        test_all(user_id)
    else:
        print(f"Unknown function: {function_name}")
        print("Available functions: analyze_heartrate_trends, analyze_glucose_trends, all")


if __name__ == "__main__":
    main() 