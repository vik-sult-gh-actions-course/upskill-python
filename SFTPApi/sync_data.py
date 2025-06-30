import os
from dotenv import load_dotenv
import paramiko
import pandas as pd
from utils.file_transfer import SftpFileTransfer
from db import SessionLocal

from SFTPApi.data_loaders.excel_file_reader import ExcelFileReader
from SFTPApi.data_loaders.parquet_file_reader import ParquetReader
from SFTPApi.services.department_service import DepartmentService
from SFTPApi.services.people_service import PeopleService

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
# todo Create directory var/files/ if doesn't exist

transfer = SftpFileTransfer(sftp_client=sftp_client, remote_base_path=remote_file_path, local_base_path=local_path)
transfer.transfer_files()

reader = ParquetReader()
excel_reader = ExcelFileReader()
session = SessionLocal()

# Load departments data from an Excel file
department_file_path = f"{local_path}department.xlsx"
people_file_path = f"{local_path}people_in_department_merged.xlsx"

# df_departments = excel_reader.load_data(department_file_path)
df_departments = excel_reader.load_data(people_file_path, 1)
department_service = DepartmentService(session)

def sync_departments():
    try:
        department_service.process_department_dataframe(df_departments)
    finally:
        session.close()

sync_departments()

# Load people data from an Excel file
df_department_people_sheet_1 = excel_reader.load_data(people_file_path)
# df_department_people_sheet_2 = excel_reader.load_data(file_path, 1)

# print(df_department_people_sheet_1)
# print(df_department_people_sheet_2)

people_service = PeopleService(session)
def sync_people():
    try:
        people_service.process_people_dataframe(df_department_people_sheet_1)
    finally:
        session.close()

sync_people()