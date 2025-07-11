"""Module for synchronizing data between SFTP server and database."""

import os
from pathlib import Path
from typing import Optional

import pandas as pd
import paramiko
from dotenv import load_dotenv
from pandas.core.frame import DataFrame

from sftp_api.db import engine as ENGINE, DB_SCHEMA
from sftp_api.file_reader import read_file
from sftp_api.utils.file_transfer import SftpFileTransfer

load_dotenv()

# SFTP connection configuration
HOST = os.getenv("SFTP_API_HOST", "")
USERNAME = os.getenv("SFTP_API_USERNAME", "")
PASSWORD = os.getenv("SFTP_API_PASSWORD", "")
PORT = int(os.getenv("SFTP_API_PORT", "22"))

# Initialize SFTP client
SSH_CLIENT = paramiko.SSHClient()
SSH_CLIENT.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SSH_CLIENT.connect(
    hostname=HOST, username=USERNAME, password=PASSWORD, port=PORT, look_for_keys=False
)

SFTP_CLIENT = SSH_CLIENT.open_sftp()

# Path configuration
REMOTE_FILE_PATH = "upload/"
LOCAL_PATH = "var/files/"

if not os.path.exists(LOCAL_PATH):
    os.makedirs(LOCAL_PATH)

# Initialize file transfer
transfer = SftpFileTransfer(
    sftp_client=SFTP_CLIENT,
    remote_base_path=REMOTE_FILE_PATH,
    local_base_path=LOCAL_PATH,
)

transfer.transfer_files()

TABLE_NAMES_MAP: dict[str, dict[str, str]] = {
    "department": {"Sheet1": "department"},
    "people_in_department_merged": {"Sheet1": "employee", "Sheet1 (2)": "department"},
}


def process_department_people(filepath: str, table_name: str) -> None:
    """
    Process department and people data from Excel file.

    Args:
        filepath: Path to the Excel file
        table_name: Name of the table to process
    """
    data_frames = read_file(filepath)
    table_names = TABLE_NAMES_MAP[table_name]
    for sheet, sheet_data_frame in data_frames.items():
        sheet_data_frame.columns = [
            col.replace("department_", "") for col in sheet_data_frame.columns
        ]
        sheet_data_frame = sheet_data_frame.rename(columns={"employee_id": "source_id"})
        sheet_data_frame["raw_create_date"] = pd.Timestamp.now()
        append_dataframe_to_sql(sheet_data_frame, table_names[sheet], ENGINE, DB_SCHEMA)


def get_table_name(filepath: str) -> str:
    """
    Extract table name from file path.

    Args:
        filepath: Path to the file

    Returns:
        The stem of the file path (filename without extension)
    """
    return Path(filepath).stem


def append_dataframe_to_sql(
    data_frame: DataFrame,
    table_name: str,
    engine,
    schema: Optional[str] = None,
    chunk_size: int = 1000,
) -> None:
    """
    Append DataFrame to SQL database.

    Args:
        data_frame: DataFrame to append
        table_name: Name of the target table
        engine: SQLAlchemy engine
        schema: Database schema (optional)
        chunk_size: Number of rows to insert at a time
    """
    data_frame.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists="append",
        chunksize=chunk_size,
        index=False,
    )


for file in os.listdir(LOCAL_PATH):
    print(f"Processing file: {file}")
    FILE_PATH = f"{LOCAL_PATH}{file}"

    df = read_file(FILE_PATH)

    name = get_table_name(FILE_PATH)

    if name == "ads_click":
        df = df.rename(columns={"ad_id": "source_id"})

    if name == "revenue_from_ads":
        df = df.rename(columns={"user_id": "source_id"})

    if name.startswith("number_of_clicks_"):
        df = df.rename(columns={"user_id": "source_id"})

    if name in ("people_in_department_merged", "department"):
        process_department_people(FILE_PATH, name)
    else:
        df["raw_create_date"] = pd.Timestamp.now()
        append_dataframe_to_sql(
            df, name, ENGINE, DB_SCHEMA
        ) # pylint: disable=missing-final-newline
