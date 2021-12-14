from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .utils.exception import Exceptional
from .routers import users, patients, medics, specialties, auth, cash, ticket_dumping, invoice

app = FastAPI(
    prefix='/api/v1'
)


@app.get('/')
async def home():
    return 'Its alive!'

# include routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(medics.router)
app.include_router(specialties.router)
app.include_router(cash.router)
app.include_router(ticket_dumping.router)
app.include_router(invoice.router)

# cors configuration
origins = [
    'http://127.0.0.1:8080',
    'http://192.168.0.102:8080',
    'http://127.0.0.1',
    'http://localhost',
    'http://192.168.0.102'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# custom error handlings
@app.exception_handler(Exceptional)
async def exceptional_exception_handler(request: Request, exc: Exceptional):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder(exc.errors()),
        status_code=400)
