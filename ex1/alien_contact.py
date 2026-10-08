from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional
from typing_extensions import Self

class ContactType(Enum):
    RADIO = 1
    VISUAL = 2
    PHYSICAL = 3
    TELEPATHIC = 4


class AlienContact(BaseModel):
    try:
        contact_id: str = Field(min_length=5, max_length=15)
        timestamp: datetime = datetime.now()
        location: str = Field(min_length=3, max_length=100)
        contact_type: ContactType = ContactType(Enum)
        signal_strength: float = Field(ge=0.0, le=10.0)
        duration_minutes: int = Field(ge=1, le=1440)
        witness_count: int = Field(ge=1, le=100)
        message_received: Optional[str] = Field(max_length=500)
        is_verified: bool = False
    except ValidationError as e:
        print(e)

    @model_validator(mode="after")
    def validate_data(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValidationError("Contact ID must start with 'AC'")
        elif self.contact_type == "PHYSICAL" and not self.is_verified:
            raise ValidationError("Physical contact reports must be verified")
        elif self.contact_type == "TELEPATHIC" and self.witness_count < 3:
            raise ValidationError("Telepathic contact requires at least 3"
                                  " witnesses")
        elif self.signal_strength > 7.0 and not self.message_received:
            raise ValidationError("Strong signals (> 7.0) should include"
                                  " received messages")
        return self
