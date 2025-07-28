"""
EMR Data Processing Service

This module handles parsing and extracting key health information from various EMR formats,
specifically Synthea patient JSON files.

TODO: Implement the following functions for the coding interview:
1. parse_synthea_patient() - Extract key health events and conditions
2. extract_chronic_conditions() - Identify chronic conditions from patient data
3. extract_vital_events() - Parse key health events (hospitalizations, procedures, etc.)
"""
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class ChronicCondition(BaseModel):
    """Represents a chronic condition from EMR data"""
    code: str
    description: str
    onset_date: Optional[datetime]
    severity: Optional[str]
    status: str  # active, resolved, etc.


class HealthEvent(BaseModel):
    """Represents a significant health event"""
    event_type: str  # hospitalization, procedure, medication, etc.
    description: str
    date: datetime
    code: Optional[str]
    provider: Optional[str]


class Medication(BaseModel):
    """Represents a medication from EMR data"""
    status: str  # active, completed, etc.
    code: Optional[str]
    display: str
    dosage_instructions: Optional[str] 
    prescribed_date: Optional[datetime]

class PatientHealthProfile(BaseModel):
    """Consolidated patient health profile from EMR data"""
    patient_id: str
    chronic_conditions: List[ChronicCondition]
    health_events: List[HealthEvent]
    medications: List[Medication]
    last_updated: datetime

# Global variable to store parsed patient data
_parsed_patient_data: Optional[PatientHealthProfile] = None


def initialize_emr_data() -> None:
    """
    Initialize EMR data by loading and parsing sample Synthea data.
    This should be called once at application startup.
    """
    global _parsed_patient_data
    
    # Load sample data
    synthea_json = load_sample_synthea_data()
    
    # Parse the data
    _parsed_patient_data = parse_synthea_patient(synthea_json)
    
    print(f"EMR data initialized for patient: {_parsed_patient_data.patient_id}")


def extract_patient_id(synthea_json: Dict[str, Any]) -> str:
    """
    Extract patient ID from FHIR Bundle.
    
    Args:
        synthea_json: Raw Synthea patient JSON (FHIR Bundle)
        
    Returns:
        str: Patient ID
    """
    try:
        # The patient ID is in the first entry's resource
        if synthea_json.get("entry") and len(synthea_json["entry"]) > 0:
            first_entry = synthea_json["entry"][0]
            if first_entry.get("resource") and first_entry["resource"].get("resourceType") == "Patient":
                return first_entry["resource"]["id"]
        
        # Fallback: try to extract from fullUrl
        if synthea_json.get("entry") and len(synthea_json["entry"]) > 0:
            full_url = synthea_json["entry"][0].get("fullUrl", "")
            if full_url.startswith("urn:uuid:"):
                return full_url.replace("urn:uuid:", "")
        
        return "Unknown"
    except Exception as e:
        print(f"Error extracting patient ID: {e}")
        return "Unknown"


def parse_synthea_patient(synthea_json: Dict[str, Any]) -> PatientHealthProfile:
    patient_id=extract_patient_id(synthea_json)

    """
    TODO: Parse Synthea patient JSON and extract key health information.
    
    Expected input: Synthea JSON
    Expected output: PatientHealthProfile with extracted conditions and events
    
    Key areas to implement:
    - Extract Condition resources for chronic conditions
    - Parse Encounter resources for hospitalizations/visits
    - Extract Procedure resources for medical procedures
    - Parse MedicationRequest resources for current medications
    
    Args:
        synthea_json: Raw Synthea patient JSON (FHIR Bundle)
        
    Returns:
        PatientHealthProfile: Structured patient health data
    """
    # STUB: Candidate should implement this function
    
    return PatientHealthProfile(
        patient_id=patient_id,
        chronic_conditions=[],
        health_events=[],
        medications=[],
        last_updated=datetime.now()
    )


def extract_chronic_conditions(user_id: str) -> List[ChronicCondition]:
    """
    TODO: Extract and classify chronic conditions from FHIR Condition resources.
    
    Focus on conditions that are:
    - Currently active
    - Chronic/long-term (not acute)
    
    Args:
        user_id: Ignored for now since sample data is used
        
    Returns:
        List[ChronicCondition]: Filtered chronic conditions
    """
    global _parsed_patient_data
    
    if _parsed_patient_data is None:
        print("Warning: EMR data not initialized. Call initialize_emr_data() first.")
        return []
    
    # STUB: Candidate should implement filtering logic
    # Should filter _parsed_patient_data.chronic_conditions based on criteria
    return _parsed_patient_data.chronic_conditions


def extract_vital_events(user_id: str) -> List[HealthEvent]:
    """
    TODO: Extract significant health events from encounters and procedures.
    
    Focus on events that impact health:
    - Emergency room visits
    - Hospitalizations
    - Major procedures
    - Specialist consultations
    
    Args:
        user_id: Ignored for now since sample data is used
        
    Returns:
        List[HealthEvent]: Significant health events chronologically ordered
    """
    global _parsed_patient_data
    
    if _parsed_patient_data is None:
        print("Warning: EMR data not initialized. Call initialize_emr_data() first.")
        return []
    
    # STUB: Candidate should implement event extraction
    # Should filter _parsed_patient_data.health_events based on criteria
    return _parsed_patient_data.health_events


def load_sample_synthea_data() -> Dict[str, Any]:
    try:
        # Get the directory where this module is located
        module_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try multiple possible paths for the synthea data
        possible_paths = [
            # Docker path: /app/synthea/data
            os.path.join("/app", "synthea", "data"),
            # Local development path: go up from services/ to project root, then to synthea/data
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(module_dir))), "synthea", "data"),
            # Alternative local path: relative to current working directory
            os.path.join("synthea", "data"),
        ]
        
        sample_file = "Colleen54_Maxie520_Olson653_e49e402a-d3c3-e448-18a6-388444f8825e.json"
        
        for data_dir in possible_paths:
            file_path = os.path.join(data_dir, sample_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
        
        # If we get here, none of the paths worked
        print(f"Could not find sample data file. Tried paths: {possible_paths}")
        return {}
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
        return {}