from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional
import sys


class SpaceStation(BaseModel):
    try:
        station_id: str = Field(min_length=3, max_length=10)
        name: str = Field(min_length=1, max_length=50)
        crew_size: int = Field(ge=1, le=20)
        power_level: float = Field(ge=0.0, le=100.0)
        oxygen_level: float = Field(ge=0.0, le=100.0)
        last_maintenance: datetime = datetime(2026, 10, 6, 15, 30, 0)
        is_operational: bool = True
        notes: Optional[str] = Field(max_length=200)
    except ValidationError as e:
        print(e)


def main() -> None:
    valid_data: dict[str, str] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": "6",
        "power_level": "85.5",
        "oxygen_level": "92.3",
        "notes": "None"
    }
    invalid_data: dict[str, str] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": "60",
        "power_level": "85.5",
        "oxygen_level": "92.3",
        "notes": "jejejeje"
    }
    valid_station = SpaceStation(**valid_data)
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Crew: {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    if valid_station.is_operational:
        print("Status: Operational")
    else:
        print("Status: No Operational")
    print("\n========================================")
    try:
        invalid_station = SpaceStation(**invalid_data)
        print(invalid_station.name)
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])

        sys.exit()


if __name__ == "__main__":
    main()
