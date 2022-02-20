from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database.db import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

get_db = get_db()


class creds(BaseModel):
    username: str
    password: str


def check_auth():
    check = list(get_db.ADMIN.find())
    if len(check) == 0:
        get_db.ADMIN.insert_one({"username": "admin", "password": "admin"})


@router.post("/login")
async def add_sms(creds: creds, Authorize: AuthJWT = Depends()):
    admin_collection = get_db.ADMIN
    check = list(admin_collection.find(
        {"username": creds.username, "password": creds.password}))
    if len(check) != 0:
        return JSONResponse(status_code=200, content={"token": Authorize.create_access_token(subject=creds.username, expires_time=False)})
    return JSONResponse(status_code=401, content={"message": "Invalid Credentials"})
