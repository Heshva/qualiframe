import pandas as pd
from pathlib import Path


def load(file):
    """
    Load and validate a CSV file.

    Checks:
        - File format is CSV
        - File exists
        - File is not completely empty
        - CSV can be parsed correctly
        - DataFrame contains data

    Parameters
    ----------
    file : str or Path
        Path to the CSV file.

    Returns
    -------
    DataFrame or None
        Returns the loaded DataFrame if valid,
        otherwise returns None.
    """

    # Convert file path to Path object
    file = Path(file)

    # Check file format
    if file.suffix.lower() != ".csv":
        print("File format invalid")
        return None

    # Check if file exists
    if not file.exists():
        print("File not found")
        return None

    # Check if file is completely empty (0 bytes)
    if file.stat().st_size == 0:
        print("File is completely empty.")
        return None

    # Try to load the CSV file
    try:
        df = pd.read_csv(file)

    # Handle empty CSV files
    except pd.errors.EmptyDataError:
        print("File contains no data.")
        return None

    # Handle incorrectly formatted CSV files
    except pd.errors.ParserError:
        print("Unable to parse the CSV file.")
        return None

    # Handle any other unexpected error
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    # Check if CSV contains headers but no data rows
    if df.empty:
        print("File contains no data.")
        return None

    print("File Loaded successfully")

    return df
