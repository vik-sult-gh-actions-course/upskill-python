"""Module for reading various file formats using pandas with automatic reader selection."""

from pathlib import Path

import pandas as pd


def read_file(filename, **kwargs):
    """
    Reads a file using pandas based on its extension.

    Parameters:
    - filename: str or Path, path to the file to be read
    - **kwargs: additional arguments to pass to the pandas reader function

    Returns:
    - DataFrame containing the file data

    Supported extensions:
    - .csv, .tsv, .txt -> pd.read_csv()
    - .xls, .xlsx, .xlsm, .xlsb, .odf, .ods, .odt -> pd.read_excel()
    - .parquet, .pq -> pd.read_parquet()
    - .json -> pd.read_json()
    """
    file_path = Path(filename)
    ext = file_path.suffix.lower()

    reader_map = {
        # CSV and variants
        ".csv": pd.read_csv,
        ".tsv": pd.read_csv,
        ".txt": pd.read_csv,
        # Excel variants
        ".xls": pd.read_excel,
        ".xlsx": pd.read_excel,
        ".xlsm": pd.read_excel,
        ".xlsb": pd.read_excel,
        ".odf": pd.read_excel,
        ".ods": pd.read_excel,
        ".odt": pd.read_excel,
        # Parquet
        ".parquet": pd.read_parquet,
        ".pq": pd.read_parquet,
        # JSON
        ".json": pd.read_json,
    }

    if ext not in reader_map:
        raise ValueError(
            f"Unsupported file extension: {ext}. "
            f"Supported extensions are: {', '.join(reader_map.keys())}"
        )

    reader = reader_map[ext]

    # Handle extension-specific default arguments
    default_args = {}
    if ext == ".json":
        default_args["lines"] = True  # Set lines=True for JSON files

    if ext == ".xlsx":
        default_args["sheet_name"] = None
        default_args["engine"] = "openpyxl"

    # Merge default_args with user-provided kwargs (user kwargs take precedence)
    final_kwargs = {**default_args, **kwargs}

    return reader(filename, **final_kwargs)  # pylint: disable=missing-final-newline
