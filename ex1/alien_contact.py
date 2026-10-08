from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional
from typing_extensions import Self

class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = datetime.now()
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = False


    @model_validator(mode="after")
    def validate_data(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        elif self.contact_type == "PHYSICAL" and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        elif self.contact_type.value == "telepathic" and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3"
                                  " witnesses")
        elif self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include"
                                  " received messages")
        return self

def main() -> None:
    try:
        data: dict[str, str] = {
        "contact_id": "AC_2024_001",
        "contact_type": "radio",
        "location": "Area 51, Nevada",
        "signal_strength": "8.5",
        "duration_minutes": "45",
        "witness_count": "5",
        "message_received": "'Greetings from Zeta Reticuli'"
        }
        valid_contact = AlienContact(**data)
        print("Alien Contact Log Validation")
        print("======================================")
        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}") 
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: {valid_contact.message_received}")
        print()
        print("======================================")
    except ValidationError as e:
        print(e)
    try:
        in_data: dict[str, str] = {
                "contact_id": "AC_2024_002",
                "contact_type": "telepathic",
                "location": "Polo Digital",
                "signal_strength": "8.5",
                "duration_minutes": "42",
                "witness_count": "2",
                "message_received": "'Greetings from Zeta Reticuli'"
            }
        invalid_contact = AlienContact(**in_data)
        print("Alien Contact Log Validation")
        print("======================================")
        print("Valid contact report:")
        print(f"ID: {invalid_contact.contact_id}")
        print(f"Type: {invalid_contact.contact_type.value}") 
        print(f"Location: {invalid_contact.location}")
        print(f"Signal: {invalid_contact.signal_strength}/10")
        print(f"Duration: {invalid_contact.duration_minutes} minutes")
        print(f"Witnesses: {invalid_contact.witness_count}")
        print(f"Message: {invalid_contact.message_received}")
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    main()