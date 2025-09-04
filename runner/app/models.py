from pydantic import BaseModel
from typing import Optional


class RunPythonRequest(BaseModel):
    code: str


class RunPythonResponse(BaseModel):
    stdout: str
    stderr: str
    return_code: Optional[int] = None
    timeout: Optional[bool] = None
