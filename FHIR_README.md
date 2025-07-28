# FHIR Primer

## What is FHIR?
**FHIR** (Fast Healthcare Interoperability Resources) is a standard for exchanging healthcare information electronically. Think of it as "JSON API for healthcare data."

## Key Concepts

### 1. **Bundle Structure**
Synthea data comes as a FHIR Bundle - essentially a container of healthcare records:
```json
{
  "resourceType": "Bundle",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "123",
        // ... patient data
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        "id": "456",
        // ... condition data
      }
    }
    // ... more resources
  ]
}
```

### 2. **Common Resource Types You'll See**

#### **Patient** - Basic demographics
```json
{
  "resourceType": "Patient",
  "id": "unique-id",
  "name": [{"given": ["John"], "family": "Doe"}],
  "birthDate": "1970-01-01",
  "gender": "male"
}
```

#### **Condition** - Medical conditions/diagnoses
```json
{
  "resourceType": "Condition",
  "code": {
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "44054006",
      "display": "Type 2 diabetes mellitus"
    }],
    "text": "Type 2 diabetes mellitus"
  },
  "clinicalStatus": {
    "coding": [{"code": "active"}]  // or "resolved"
  },
  "onsetDateTime": "2019-08-24T14:15:22Z"
}
```

#### **Encounter** - Hospital visits, appointments
```json
{
  "resourceType": "Encounter",
  "class": {
    "code": "EMER"  // or "AMB"
  },
  "period": {
    "start": "2023-01-15T10:00:00Z",
    "end": "2023-01-15T14:00:00Z"
  },
  "reasonCode": [{
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "82423001",
      "display": "Chronic pain (finding)"
    }]
  }],
}
```

#### **Procedure** - Medical procedures performed
```json
{
  "resourceType": "Procedure",
  "code": {
    "coding": [ {
        "system": "http://snomed.info/sct",
        "code": "243085009",
        "display": "Oral health education (procedure)"
      } ],
    "text": "Oral health education (procedure)"
  },
  "performedPeriod": {
    "start": "2017-06-04T09:41:33-05:00",
    "end": "2017-06-04T10:05:18-05:00"
  },
}
```

#### **MedicationRequest** - Prescriptions
```json
{
  "resourceType": "MedicationRequest",
  "medicationCodeableConcept": {
    "coding": [{
      "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
      "code": "751905",
      "display": "Trinessa 28 Day Pack"
    }],
  },
  "status": "active",  // or "completed"
  "dosageInstruction": [{
    "text": "Take 2 tablets daily"
  }]
}
```

## Tips for Processing FHIR

1. **Not all fields are required** - Always check if data exists before accessing
2. **Arrays everywhere** - Many fields like `coding` and `name` are arrays
3. **Display vs Code** - `display` is human-readable, `code` is for machines
4. **Reference resources** - Resources often reference each other by ID
5. **Time zones** - Timestamps usually include timezone (Z = UTC)

## Example: Finding Active Diabetes
```python
def has_active_diabetes(bundle):
    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        if resource.get("resourceType") == "Condition":
            # Check if it's diabetes
            code = resource.get("code", {}).get("coding", [{}])[0].get("code", "")
            if code in ["44054006", "73211009"]:  # Type 2 or Type 1
                # Check if active
                status = resource.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "")
                if status == "active":
                    return True
    return False
```
