from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.exceptions import HTTPException as StarletteHTTPException
from routers.sms import sms
from routers.auth import auth
from routers.client import client
import uvicorn

app = FastAPI(
    version="4.0",
    title="sms_reciver",
    description="sms_reciver",
    redoc_url=None,
)

origins = ["*"]
app.include_router(sms.router)
app.include_router(auth.router)
app.include_router(client.router)

auth.check_auth()
app.mount("/v4", StaticFiles(directory="build", html=True), name="build")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseModel):
    authjwt_secret_key: str = "jaihind"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return HTMLResponse(open("build/index.html", "rb").read())
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.get("/home")
async def root():
    return HTMLResponse(open("build/index.html", "rb").read())

@app.get("/")
async def root():
    return RedirectResponse("/home")


@app.get("/version")
async def version():
    return {"version": app.version}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)