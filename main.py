import numpy as np
import pandas as pd
import datetime as datetime
from ensure import ensure_annotations
from google.cloud import storage
import json


class operation_file:
    @ensure_annotations
    def __init__(self):
        self.file_name_download = None
        self.folder_download = None
        self.folder_upload = None
        self.bucket = None
        self.client = None
        self.file_name = None
        self.bucket_name = None
        self.secret = None
        self.message_late = "llego tarde"
        self.message_on_time = "llego temprano"
        self.path_admin_secret = "secret/admin_secret.json"

    @ensure_annotations
    def read_admin_secret(self):
        # Open the JSON file and read its contents
        with open(self.path_admin_secret) as f:
            data = json.load(f)
        self.bucket_name = data["bucket_name"]
        self.secret = data["secret"]
        self.file_name = data["file_name"]
        self.folder_upload = data["folder_upload"]
        self.folder_download = data["folder_download"]
        self.file_name_download = data["file_name_download"]

    @ensure_annotations
    def connection_bd(self):
        self.client = storage.Client.from_service_account_json(self.secret)
        self.bucket = self.client.get_bucket(self.bucket_name)

    @ensure_annotations
    def read_file(self):
        # open the file
        xlsx = pd.read_excel("temporal_files/datos_test_demo.xlsx", sheet_name="Hoja1")
        # get the first sheet as an object
        return xlsx

    @ensure_annotations
    def compare_attendance(self, datetime_str: datetime.timedelta) -> str:
        if datetime_str.days > 0:
            return self.message_late
        elif datetime_str.seconds > 900:
            return self.message_late
        else:
            return self.message_on_time

    @ensure_annotations
    def upload_bd(self, data: pd.DataFrame) -> str:
        data.to_excel("temporal_files/" + self.file_name, index=False)
        blob = self.bucket.blob(self.folder_upload + self.file_name)
        blob.upload_from_filename("temporal_files/" + self.file_name)
        return "ok"

    @ensure_annotations
    def download_bd(self):
        blob = self.bucket.blob(self.folder_download + self.file_name_download)
        blob.download_to_filename("temporal_files/" + self.file_name_download)


if __name__ == '__main__':
    # class definition
    file_functions = operation_file()
    # get names from secret admin names
    file_functions.read_admin_secret()
    # connection to bd firebase
    file_functions.connection_bd()
    # download current file - origin bot
    file_functions.download_bd()
    # read file
    df = file_functions.read_file()
    # subtract timestamp attendance operation
    status_arrive = df.Timestamp - df.Hora_apertura_formulario
    #add status arrive to dataframe
    attendace_str = list(map(file_functions.compare_attendance, status_arrive))
    df["attendance"] = attendace_str
    # upload new file with status operation
    status_upload = file_functions.upload_bd(df)
    print(status_upload)
