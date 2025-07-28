# Test Scripts for Individual Function Testing

This directory contains standalone test scripts that allow candidates to test the EMR parser and wearables analytics functions individually, outside of the chat agent flow.

## Available Test Scripts

### 1. `test_emr_parser.py`
Tests the EMR parser functions that process Synthea patient data.

**Functions tested:**
- `parse_synthea_patient()` - Parses Synthea JSON and extracts patient health information
- `extract_chronic_conditions()` - Identifies chronic conditions from patient data
- `extract_vital_events()` - Extracts significant health events

### 2. `test_wearables_analytics.py`
Tests the wearables analytics functions that analyze health data from wearables.

**Functions tested:**
- `analyze_heartrate_trends()` - Analyzes heartrate and HRV trends
- `analyze_glucose_trends()` - Analyzes glucose trends from CGM data
- Raw data retrieval functions

## Prerequisites

Making the python test files executable from the root directory:
```bash
chmod +x backend/python/tests/test_emr_parser.py backend/python/tests/test_wearables_analytics.py
```

Within `backend/python` run `poetry install`


### EMR Parser Tests

```bash
# Test all EMR parser functions
poetry run python tests/test_emr_parser.py all

# Test individual functions
poetry run python tests/test_emr_parser.py parse_synthea_patient
poetry run python tests/test_emr_parser.py extract_chronic_conditions
poetry run python tests/test_emr_parser.py extract_vital_events
```

### Wearables Analytics Tests

Tests the wearables analytics functions that analyze health data from wearables:

- `analyze_heartrate_trends()` - Analyzes heartrate and HRV trends
- `analyze_glucose_trends()` - Analyzes glucose trends from CGM data

**Prerequisites:**
- Environment variables must be set: `VITAL_API_KEY`, `VITAL_ENV`, `VITAL_REGION`

**Usage:**
```bash
# Test all wearables analytics functions
poetry run python tests/test_wearables_analytics.py all

# Test individual functions with a specific user ID
poetry run python tests/test_wearables_analytics.py analyze_heartrate_trends user123
poetry run python tests/test_wearables_analytics.py analyze_glucose_trends user123
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're running from the `backend/python` directory
2. **Missing environment variables**: Set up your `.env` file with Vital/Junction API credentials
3. **No data returned**: This is expected for test users without real data - implement the functions to handle this gracefully
4. **API errors**: Check your Vital/Junction API credentials and network connectivity
