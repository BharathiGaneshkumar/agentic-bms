import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

COLUMN_MAP = {
    "AHU name": "ahu_id",
    "Time": "reading_time",
    "Set point temperature": "set_point_temp",
    "Return temperature": "return_temp",
    "Supply air temperature": "supply_air_temp",
    "Supply fan": "supply_fan",
    "Valve position": "valve_position",
    "Heating supply temperature1": "heating_supply_temp_1",
    "Heating supply temperature2": "heating_supply_temp_2",
    "Total heating pump": "total_heating_pump",
    "Heating pump 1": "heating_pump_1",
    "Heating pump 2": "heating_pump_2",
    "Heating pump 3": "heating_pump_3",
    "Cooling supply temperature 1": "cooling_supply_temp_1",
    "Cooling supply temperature 2": "cooling_supply_temp_2",
    "Total cooling pump": "total_cooling_pump",
    "cooling pump 1": "cooling_pump_1",
    "cooling pump 2": "cooling_pump_2",
    "cooling pump 3": "cooling_pump_3",
    "cooling pump 4": "cooling_pump_4",
    "labeling": "labeling",
}
def load_and_clean(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.rename(columns=COLUMN_MAP)

    # Parse "2024-06-01 00" (hour, no minutes) into a real timestamp
    df["reading_time"] = pd.to_datetime(df["reading_time"], format="%Y-%m-%d %H")

    print(f"Loaded {len(df)} rows")

    before = len(df)
    df = df.drop_duplicates()
    if len(df) < before:
        print(f"Dropped {before - len(df)} exact duplicate rows")
    else:
        print("No exact duplicate rows found (paper's stated 332-row dedup does not "
              "reproduce on this Figshare release; verified via per-AHU gap analysis "
              "instead — see README)")

    return df

if __name__ == "__main__":
    df = load_and_clean("data/raw/office_scientific_data.csv")
    print(df.head())
    print(df.dtypes)