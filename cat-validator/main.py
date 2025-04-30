from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional, List, Union

app = FastAPI()

class Cat(BaseModel):
    name: str
    age: int
    breed: Optional[str] = None

class ValidationResponse(BaseModel):
    valid: bool
    data: Optional[Cat] = None
    errors: Optional[List[str]] = None

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        loc = " -> ".join(str(x) for x in error["loc"])
        msg = f"{loc}: {error['msg']}"
        error_messages.append(msg)
    
    return JSONResponse(
        status_code=422,
        content=ValidationResponse(
            valid=False,
            errors=error_messages
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=422,
        content=ValidationResponse(
            valid=False,
            errors=[str(exc)]
        ).model_dump()
    )

@app.post("/validate", response_model=ValidationResponse)
async def validate_cat(cat: Cat):
    return ValidationResponse(
        valid=True,
        data=cat
    )
