"""
Medical History API Router - Manage patient medical history
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.schemas.medical_history import (
    AllergyCreate,
    AllergyResponse,
    MedicalConditionCreate,
    MedicalConditionResponse,
    MedicationCreate,
    MedicationResponse,
    SymptomLogCreate,
    SymptomLogResponse,
)
from backend.models.user import User
from backend.repositories.allergy_repository import AllergyRepository
from backend.repositories.medical_history_repository import MedicalHistoryRepository
from backend.repositories.medication_repository import MedicationRepository
from backend.repositories.symptom_repository import SymptomRepository

router = APIRouter(prefix="/medical-history", tags=["Medical History"])


# Medical Conditions Endpoints
@router.post(
    "/conditions", response_model=MedicalConditionResponse, status_code=status.HTTP_201_CREATED
)
def add_medical_condition(
    condition: MedicalConditionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a new medical condition"""
    repo = MedicalHistoryRepository(db)
    new_condition = repo.add_condition(
        user_id=current_user.id,
        condition_name=condition.condition_name,
        status=condition.status,
        severity=condition.severity,
        diagnosed_date=condition.diagnosed_date,
        notes=condition.notes,
    )
    if not new_condition:
        raise HTTPException(status_code=500, detail="Failed to add condition")
    return new_condition.to_dict()


@router.get("/conditions", response_model=List[MedicalConditionResponse])
def get_medical_conditions(
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all medical conditions for current user"""
    repo = MedicalHistoryRepository(db)
    conditions = repo.get_by_user(current_user.id, status=status)
    return [c.to_dict() for c in conditions]


# Medications Endpoints
@router.post("/medications", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
def add_medication(
    medication: MedicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a new medication"""
    repo = MedicationRepository(db)
    new_med = repo.add_medication(
        user_id=current_user.id,
        medication_name=medication.medication_name,
        dosage=medication.dosage,
        frequency=medication.frequency,
        route=medication.route,
        start_date=medication.start_date,
        reason=medication.reason,
        prescribing_doctor=medication.prescribing_doctor,
    )
    if not new_med:
        raise HTTPException(status_code=500, detail="Failed to add medication")
    return new_med.to_dict()


@router.get("/medications", response_model=List[MedicationResponse])
def get_medications(
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all medications for current user"""
    repo = MedicationRepository(db)
    medications = repo.get_by_user(current_user.id, status=status)
    return [m.to_dict() for m in medications]


@router.patch("/medications/{medication_id}/discontinue", response_model=MedicationResponse)
def discontinue_medication(
    medication_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark medication as discontinued"""
    repo = MedicationRepository(db)
    medication = repo.discontinue_medication(medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication.to_dict()


# Allergies Endpoints
@router.post("/allergies", response_model=AllergyResponse, status_code=status.HTTP_201_CREATED)
def add_allergy(
    allergy: AllergyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a new allergy"""
    repo = AllergyRepository(db)
    new_allergy = repo.add_allergy(
        user_id=current_user.id,
        allergen=allergy.allergen,
        reaction=allergy.reaction,
        severity=allergy.severity,
        allergen_type=allergy.allergen_type,
        verified_date=allergy.verified_date,
        verified_by=allergy.verified_by,
        notes=allergy.notes,
    )
    if not new_allergy:
        raise HTTPException(status_code=500, detail="Failed to add allergy")
    return new_allergy.to_dict()


@router.get("/allergies", response_model=List[AllergyResponse])
def get_allergies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all allergies for current user"""
    repo = AllergyRepository(db)
    allergies = repo.get_by_user(current_user.id)
    return [a.to_dict() for a in allergies]


# Symptom Logs Endpoints
@router.post("/symptoms", response_model=SymptomLogResponse, status_code=status.HTTP_201_CREATED)
def log_symptom(
    symptom: SymptomLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a new symptom"""
    repo = SymptomRepository(db)
    new_symptom = repo.log_symptom(
        user_id=current_user.id,
        symptom_description=symptom.symptom_description,
        severity=symptom.severity,
        body_part=symptom.body_part,
        onset_date=symptom.onset_date,
        duration=symptom.duration,
        frequency=symptom.frequency,
        quality=symptom.quality,
        associated_symptoms=symptom.associated_symptoms,
        triggers=symptom.triggers,
        relieving_factors=symptom.relieving_factors,
        aggravating_factors=symptom.aggravating_factors,
        impact_on_life=symptom.impact_on_life,
        notes=symptom.notes,
    )
    if not new_symptom:
        raise HTTPException(status_code=500, detail="Failed to log symptom")
    return new_symptom.to_dict()


@router.get("/symptoms", response_model=List[SymptomLogResponse])
def get_symptoms(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get symptom logs for current user"""
    repo = SymptomRepository(db)
    symptoms = repo.get_by_user(current_user.id, limit=limit)
    return [s.to_dict() for s in symptoms]


@router.get("/symptoms/recent", response_model=List[SymptomLogResponse])
def get_recent_symptoms(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get recent symptoms (last N days)"""
    repo = SymptomRepository(db)
    symptoms = repo.get_recent_symptoms(current_user.id, days=days)
    return [s.to_dict() for s in symptoms]
