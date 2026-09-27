import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

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
              "instead - see data/raw/README.md)")

    return df


def assign_split(df: pd.DataFrame) -> pd.DataFrame:
    # All 5 classes now participate in the split, including Valve position
    # fault (117 rows) - thin, but included via SMOTE later in training.
    train_val, test = train_test_split(
        df, test_size=0.20, stratify=df["labeling"], random_state=42
    )
    train, val = train_test_split(
        train_val, test_size=0.25, stratify=train_val["labeling"], random_state=42
    )

    train["split"] = "train"
    val["split"] = "val"
    test["split"] = "test"

    result = pd.concat([train, val, test]).sort_index()
    print(result["split"].value_counts(dropna=False))
    return result


def get_engine():
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db = os.environ["POSTGRES_DB"]
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


def write_to_postgres(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql("sensor_readings", engine, if_exists="append", index=False, chunksize=5000)
    print(f"Wrote {len(df)} rows to sensor_readings")


if __name__ == "__main__":
    df = load_and_clean("data/raw/office_scientific_data.csv")
    df = assign_split(df)
    write_to_postgres(df)