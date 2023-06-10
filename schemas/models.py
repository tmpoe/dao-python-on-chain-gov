from pydantic import BaseModel

class AccountImportData(BaseModel):
    file_path: str
    password: str