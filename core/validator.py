import re
from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class PersonalInfo:
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    title: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None


@dataclass
class FieldError:
    field_name: str
    message: str


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[FieldError] = field(default_factory=list)


@dataclass
class EducationEntry:
    institution: str
    degree: str
    field: str
    start_date: Any
    end_date: Any
    gpa: str
    highlights: str


class ResumeValidator:
    """Handles field-level validation using strongly typed models"""

    @staticmethod
    def validate_email(email: str) -> bool:
        # Standard RFC 5322 regex
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone) -> bool:
        clean_phone = re.sub(r"[\s\-\(\)\+]", "", phone)
        return clean_phone.isdigit() and 10 <= len(clean_phone) <= 15

    @classmethod
    def validate_personal_info(cls, info: PersonalInfo) -> ValidationResult:
        errors = []

        required_fields = {
            "name": "Full Name",
            "email": "Email",
            "phone": "Phone Number",
            "location": "Location",
            "title": "Professional Title",
            "summary": "Professional Summary",
        }

        for field_key, display_name in required_fields.items():
            value = getattr(info, field_key)
            if not value or not str(value).strip():
                errors.append(FieldError(field_key, f"{display_name} is required."))

        if "email" not in [e.field_name for e in errors]:
            if not cls.validate_email(info.email):
                errors.append(
                    FieldError(
                        "email", "Invalid email format (e.g., user@example.com)."
                    )
                )

        elif "phone" not in [e.field_name for e in errors]:
            if not cls.validate_phone(info.phone):
                errors.append(
                    FieldError(
                        "phone", "Phone must contain only numbers (min 10 digits)."
                    )
                )

        elif "summary" not in [e.field_name for e in errors]:
            if len(str(info.summary).split()) < 5:
                errors.append(
                    FieldError("summary", "Summary is too short (min 5 words).")
                )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    @classmethod
    def validate_education(cls, entries: List[dict]) -> ValidationResult:
        errors = []
        if not entries:
            errors.append(
                FieldError("education", "At least one education entry is required.")
            )
            return ValidationResult(is_valid=False, errors=errors)

        for i, entry in enumerate(entries):
            # Check required text fields
            if not entry.get("institution"):
                errors.append(
                    FieldError(
                        f"edu_inst_{i}", f"Entry #{i+1}: Institution is required."
                    )
                )
            if not entry.get("degree"):
                errors.append(
                    FieldError(f"edu_degree_{i}", f"Entry #{i+1}: Degree is required.")
                )

            # Date Logic
            start = entry.get("start_date")
            end = entry.get("end_date")

            if start and end and start >= end:
                errors.append(
                    FieldError(
                        f"edu_end_{i}",
                        f"Entry #{i+1}: End date must be after start date.",
                    )
                )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    @classmethod
    def validate_experience(cls, entries: list) -> ValidationResult:
        errors = []
        if not entries:
            errors.append(
                FieldError(
                    "experience", "At least one work experience entry is required."
                )
            )
            return ValidationResult(is_valid=False, errors=errors)

        for i, entry in enumerate(entries):
            if not entry.get("company"):
                errors.append(
                    FieldError(
                        f"exp_company_{i}", f"Entry #{i+1}: Company is required."
                    )
                )
            if not entry.get("position"):
                errors.append(
                    FieldError(
                        f"exp_position_{i}", f"Entry #{i+1}: Position is required."
                    )
                )

            # Date Validation
            start = entry.get("start_date")
            end = entry.get("end_date")

            if start and end and start >= end:
                errors.append(
                    FieldError(
                        f"exp_end_{i}",
                        f"Entry #{i+1}: End date must be after start date.",
                    )
                )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    @classmethod
    def validate_projects(cls, entries: list) -> ValidationResult:
        errors = []
        if not entries:
            return ValidationResult(is_valid=True)
        for i, entry in enumerate(entries):
            if not entry.get("name"):
                errors.append(
                    FieldError(f"proj_name_{i}", f"Project #{i+1}: Name is required.")
                )
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    @classmethod
    def validate_skills(cls, entries: list) -> ValidationResult:
        errors = []
        if not entries:
            errors.append(
                FieldError("skills", "Please add at least one skill category.")
            )
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
