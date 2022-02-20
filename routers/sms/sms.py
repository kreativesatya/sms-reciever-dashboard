from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database.db import get_db

router = APIRouter(
    prefix="/sms",
    tags=["sms"],
    responses={404: {"description": "Not found"}},
)

get_db = get_db()


class Sms(BaseModel):
    msg_from: str
    body: str
    device_id : str
    date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@router.post("/add")
async def add_sms(sms: Sms):
    sms_collection = get_db.SMS
    sms_collection.insert_one(jsonable_encoder(sms))
    return JSONResponse(status_code=200, content={"message": "success"})


@router.get("/{device_id}")
async def sms_reciver(device_id: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    response= []
    data = list(get_db.SMS.find({"device_id": device_id}, {
                "_id": False}).sort("date", -1))
    for i in data:
        response.append(list(i.values()))
    return JSONResponse({"sms": response})


@router.get("/limit/{device_id}/{limit}")
async def sms_reciver_limit(device_id: str, limit: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    response = []
    data = list(get_db.SMS.find({"device_id": device_id}, {"_id": False}).sort(
        {"created_at": -1}).limit(limit))
    for i in data:
        response.append(list(i.values()))
    return JSONResponse({"sms": response})


@router.get("/delete/{device_id}")
async def sms_reciver_delete(device_id: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    get_db.SMS.delete_many({"device_id": device_id})
    return JSONResponse(content={"message": "success"})
