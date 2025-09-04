from fastapi import FastAPI
import uvicorn
import os

from runner import run_code
from models import RunPythonRequest

app = FastAPI()


@app.post("/run")
async def run_code_endpoint(req: RunPythonRequest):
    result = await run_code(req.code)
    return result


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv('PORT', 8000)),
        reload=True
    )