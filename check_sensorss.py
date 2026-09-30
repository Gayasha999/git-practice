import pandas as pd
import yaml
import json
from pathlib import Path

# 1. Define project directory
BASE_DIR = Path(__file__).parent


# 2. Read configuration file
config_path = BASE_DIR / "config.yml"

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

max_days = config["max_days_since_calibration"]
output_file = BASE_DIR / config["output_file"]


# 3. Read sensor and calibration data
sensors_path = BASE_DIR / "sensors.xlsx"
calibrations_path = BASE_DIR / "calibrations.csv"

sensors_df = pd.read_excel(sensors_path)
calibrations_df = pd.read_csv(calibrations_path)


# 4. Join sensor information with calibration data
merged_df = pd.merge(
    sensors_df,
    calibrations_df,
    on="sensor_id",
    how="inner"
)


# 5. Filter overdue sensors
overdue_df = merged_df[
    merged_df["days_since_calibration"] > max_days
]


# 6. Select required output columns
output_columns = [
    "sensor_id",
    "lab_room",
    "owner",
    "days_since_calibration"
]

overdue_sensors = overdue_df[output_columns]


# 7. Export overdue sensors to JSON
with open(output_file, "w") as file:
    json.dump(
        overdue_sensors.to_dict(orient="records"),
        file,
        indent=2
    )


print(f"Calibration check completed.")
print(f"Overdue sensors found: {len(overdue_sensors)}")
print(f"Output saved to: {output_file}")