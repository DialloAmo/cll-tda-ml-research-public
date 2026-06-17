from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


def get_project_root() -> Path:
    return ROOT_DIR


def get_data_dirs() -> dict:
    return {
        "raw": RAW_DATA_DIR,
        "interim": INTERIM_DATA_DIR,
        "processed": PROCESSED_DATA_DIR,
    }


def ensure_directories() -> None:
    for path in [RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def read_csv_from_processed(filename: str, **kwargs) -> pd.DataFrame:
    filepath = PROCESSED_DATA_DIR / filename
    return pd.read_csv(filepath, **kwargs)


def read_csv_from_raw(filename: str, **kwargs) -> pd.DataFrame:
    filepath = RAW_DATA_DIR / filename
    return pd.read_csv(filepath, **kwargs)


def save_dataframe_to_processed(df: pd.DataFrame, filename: str, index: bool = False, **kwargs) -> Path:
    ensure_directories()
    filepath = PROCESSED_DATA_DIR / filename
    df.to_csv(filepath, index=index, **kwargs)
    return filepath