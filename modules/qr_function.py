import qrcode
import json
import datetime as datetime
from ensure import ensure_annotations
import hashlib


class attendance:
    def __init__(self):
        self.key = None
        self.path_attendance_key = "../secret/attendance_key_secret.json"

    @ensure_annotations
    def read_key(self):
        print(self.path_attendance_key)
        with open(self.path_attendance_key) as f:
            data = json.load(f)
        self.key = data["key"]

    @ensure_annotations
    def encryption_type(self) -> str:
        string_key = self.key + " - " + str(datetime.datetime.now())
        hashed_key = hashlib.sha256(string_key.encode("utf-8")).hexdigest()
        print(type(hashed_key))
        return hashed_key

    @ensure_annotations
    def qrcode_attendance(self, hashed_key: str):
        # Encoding data using make() function
        img = qrcode.make(hashed_key)
        # Saving as an image file
        img.save('MyQRCode1.png')


if __name__ == "__main__":
    # read class attendance
    attendance_students = attendance()
    attendance_students.read_key()
    hashed_key=attendance_students.encryption_type()
    attendance_students.qrcode_attendance(hashed_key)
