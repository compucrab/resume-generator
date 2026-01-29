import re
from dataclasses import dataclass, field
from typing import List, Optional


from dataclasses import dataclass
from typing import Optional


@dataclass
class PersonalInfo:
    name: str  # Required string
    email: str  # Required string
    phone: Optional[str] = None  # Can be string OR None
    location: Optional[str] = None
    label: Optional[str] = None
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


class ResumeValidator:
    """Handles field-level validation using strongly typed models"""

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        clean_phone = re.sub(r"[\s\-\(\)]", "", phone)
        return len(clean_phone) >= 10

    @classmethod
    def validate_personal_info(cls, info: PersonalInfo) -> ValidationResult:
        errors = []

        if not info.name.strip():
            errors.append(FieldError("name", "Full Name is required."))

        if not info.email.strip():
            errors.append(FieldError("email", "Email is required."))
        elif not cls.validate_email(info.email):
            errors.append(FieldError("email", "Invalid email format."))

        if info.phone and not cls.validate_phone(info.phone):
            errors.append(FieldError("phone", "Phone must be at least 10 digits."))

        if info.summary and len(info.summary.split()) < 5:
            errors.append(FieldError("summary", "Summary is too short (min 5 words)."))

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
