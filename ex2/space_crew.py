from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional
from typing_extensions import Self

#TODO: revisar datetimes

class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = datetime.now()
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_items=1, max_items=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)


    def valid_crew(self, crew: list[CrewMember]) -> bool:
        for member in crew:
            if member.rank.value == "commander" or member.rank.value == "captain":
                return True
        return False

    def valid_experience(self, crew: list[CrewMember]) -> bool:
        for member in crew:
            if member.years_experience < 5:
                return False
        return True

    def valid_status(self, crew: list[CrewMember]) -> bool:
        for member in crew:
            if not member.is_active:
                return False
        return True


    @model_validator(mode="after")
    def validate_data(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")
        elif not self.valid_crew(self.crew):
            raise ValueError("Crew must have at least one Commander or Captain")
        elif self.duration_days > 365 and not self.valid_experience(self.crew):
            raise ValueError(r"Long missions (> 365 days) need 50% experienced crew (5+ years)")
        elif not self.valid_status(self.crew):
            raise ValueError("All crew members must be active")


def main() -> None:

    sarah_data:dict[str, str] = {
        "member_id": "sconor",
        "name": "Sarah Connor",
        "rank": "commander",
        "age": "30",
        "specialization": "Mission Command",
        "years_experience": "10",
    }
    john_data:dict[str, str] = {
        "member_id": "jsmith",
        "name": "John Smith",
        "rank": "lieutenant",
        "age": "40",
        "specialization": "Navigation",
        "years_experience": "10",
    }
    alice_data:dict[str, str] = {
        "member_id": "ajohnson",
        "name": "Alice Johnson",
        "rank": "officer",
        "age": "50",
        "specialization": "Engineering",
        "years_experience": "30",
    }

    sarah = CrewMember(**sarah_data)
    john = CrewMember(**john_data)
    alice = CrewMember(**alice_data)
    members: list[CrewMember] = []
    members.append(sarah)
    members.append(john)
    members.append(alice)
    m_data: dict[str, str] = {
        "mission_name": "Mars Colony Establishment",
        "mission_id": "M2024_MARS",
        "destination": "Mars",
        "duration_days": "900",
        "budget_millions": "2500.0",
    }
    mission_data = SpaceMission(**m_data, crew=members)
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {mission_data.mission_name}")
    print(f"ID: {mission_data.mission_id}")
    print(f"Destination: {mission_data.destination}")
    print(f"Duration: {mission_data.duration_days} days") 
    print(f"Budget: ${mission_data.budget_millions}M")
    print(f"Crew size: {len(mission_data.crew)}")
    print("Crew members:")
    for member in members:
        print(member.name,end=" ")
        print("("+member.rank.value+")", end=" - ")
        print(member.specialization)
    print("\n=========================================")
    try:
        members.remove(sarah)
        new_mission = SpaceMission(**m_data, crew=members)
        print(new_mission.destination)
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    main()