# AI Engineering Interview - Candidate Guide

## Overview

This is a basic product which integrates EMR (Electronic Medical Record) data and wearables analytics so that a user can chat with their personalized health agent to receive AI-powered insights. The TODO implementations focus on two key areas:

### 1. EMR Data Processing (`services/emr_parser.py`)
- **Purpose**: Parse Synthea FHIR JSON data to extract patient health information
- **Key Functions**:
  - `parse_synthea_patient()`: Main parser for FHIR data
  - `extract_chronic_conditions()`: Filter for active chronic conditions
  - `extract_vital_events()`: Extract significant health events

### 2. Wearables Analytics (`services/wearables_analytics.py`)
- **Purpose**: Analyze biometric trends from Vital/Junction API data
- **Key Functions**:
  - `analyze_heartrate_trends()`: Process HR/HRV data for trends
  - `analyze_glucose_trends()`: Analyze CGM data for patterns

You will choose if you want to start with the EMR data processing or the wearables anlytics; they are independent of each other.


## Frontend
You can ignore most / all of the code within `frontend` as it merely creates the scaffold for the application; you are not expected to change any files there. The first section within the frontend allows you to create and/or load a sample user from Vital/Junction. The second section allows that sample user to chat with their AI health assistant.


## What's Already Implemented
- The chat agent and its tool calling is implemented within `chat_agent.py`. Although `user_id` is passed, it is not used within the EMR data flow since we are relying on a single source of local data from `synthea/data` for the EMR records. It is worth noting that the `user_id` from the EMR record and Vital/Junction data do not match and that is okay for the sake of this sample application.
- All of the data loading for the EMR sample data is done within `initialize_emr_data()` which calls `load_sample_synthea_data()`; `FHIR_README.md` and `SNOMED_CT_README.md` are provided for additional context.
- Data from Vital/Junction is loaded within `get_heartrate_data` and `get_glucose_data`; a sample format of this data is within the `GLUCOSE_README.md` and `HEARTRATE_README.md` for your reference.
- I have scaffolded in `tests/` which will allow you to execute the individual functions outside of the chat flow.
