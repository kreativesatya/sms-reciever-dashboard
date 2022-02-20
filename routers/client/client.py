from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database.db import get_db

router = APIRouter(
    prefix="/client",
    tags=["client"],
    responses={404: {"description": "Not found"}},
)

get_db = get_db()


class client(BaseModel):
    client_id: str
    android_version: str
    device_name: str
    date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@router.get("/")
async def get_clients(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    clients = get_db.CLIENT
    client = list(clients.find({}, {"_id": False}))
    return JSONResponse(status_code=200, content={"clients": client})


@router.post("/add")
async def add_client(client: client):
    data = jsonable_encoder(client)
    if get_db.CLIENT.find_one({"client_id": data["client_id"], "device_name": data["device_name"]}) is None:
        get_db.CLIENT.insert_one(data)
        return JSONResponse(status_code=200, content={"message": "Client added"})
    return JSONResponse(status_code=200, content={"message": "client already exists"})

