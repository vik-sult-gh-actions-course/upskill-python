import os
import pandas as pd
from pandas.core.frame import DataFrame

import paramiko
from dotenv import load_dotenv
from pathlib import Path

from db import engine, DB_SCHEMA
from sftp_api.file_reader import read_file
from utils.file_transfer import SftpFileTransfer

load_dotenv()

host = os.getenv("SFTP_API_HOST")
username = os.getenv("SFTP_API_USERNAME")
password = os.getenv("SFTP_API_PASSWORD")
port = int(os.getenv("SFTP_API_PORT", 22))

SSH_Client = paramiko.SSHClient()
SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SSH_Client.connect(hostname=host, username=username, password=password, port=port, look_for_keys=False)

sftp_client = SSH_Client.open_sftp()

remote_file_path = "upload/"
local_path = 'var/files/'

if not os.path.exists(local_path):
    os.makedirs(local_path)

transfer = SftpFileTransfer(
    sftp_client=sftp_client,
    remote_base_path=remote_file_path,
    local_base_path=local_path
)

transfer.transfer_files()

table_names_map: dict[str, dict[str, str]] = {
    'department': {'Sheet1': 'department'},
    'people_in_department_merged': {'Sheet1': 'employee', 'Sheet1 (2)': 'department'}
}


def process_department_people(filepath, table_name):
    data_frames = read_file(filepath)
    table_names = table_names_map[table_name]
    for sheet, sheet_data_frame in data_frames.items():
        sheet_data_frame.columns = [col.replace('department_', '') for col in sheet_data_frame.columns]
        sheet_data_frame = sheet_data_frame.rename(columns={'employee_id': 'source_id'})
        sheet_data_frame['raw_create_date'] = pd.Timestamp.now()
        append_dataframe_to_sql(sheet_data_frame, table_names[sheet], engine, DB_SCHEMA)


def get_table_name(filepath: str):
    return Path(filepath).stem


def append_dataframe_to_sql(data_frame: DataFrame, table_name: str, engine, schema: str = None, chunk_size: int = 1000):
    data_frame.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists='append',
        chunksize=chunk_size,
        index=False
    )


for file in os.listdir(local_path):
    print(f"Processing file: {file}")
    file_path = f"{local_path}{file}"

    df = read_file(file_path)

    name = get_table_name(file_path)

    if name == 'ads_click':
        df = df.rename(columns={'ad_id': 'source_id'})

    if name == 'revenue_from_ads':
        df = df.rename(columns={'user_id': 'source_id'})

    if name.startswith("number_of_clicks_"):
        df = df.rename(columns={'user_id': 'source_id'})

    if name == 'people_in_department_merged' or name == 'department':
        process_department_people(file_path, name)
    else:
        df['raw_create_date'] = pd.Timestamp.now()
        append_dataframe_to_sql(df, name, engine, DB_SCHEMA)
