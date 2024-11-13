# Main application
from typing import Dict, Annotated, Optional
import uuid
import hashlib

from fastapi import (
    Depends,
    FastAPI,
    APIRouter,
    Request,
    Response,
    status,
    Header,
    HTTPException,
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError as PydanticValidationError

import crud, models, schemas, config
from database import SessionLocal, engine


app = FastAPI()

prefix_router = APIRouter(prefix="/blacklists")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Validate the token
def authenticate(token: str):
    if not token or not token.startswith("Bearer "):
        return False
    token = token.split(" ")[1]
    if token != config.BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
# health
@prefix_router.get("/ping")
def ping():
    raise HTTPException(status_code=500, detail="Internal Server Error")
    return "pong"


# Create a blacklist email
@prefix_router.post("")
def create_blacklist_email(
    blacklist_email: Dict,
    response: Response,
    db: Session = Depends(get_db),
    authorization: Annotated[Optional[str], Header()] = None,
    request: Request = None,
):
    authenticate(authorization)
    try:
        blacklist_email = schemas.CreateBlacklistEmail(**blacklist_email)
    except PydanticValidationError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=e.errors())
    if crud.get_blacklisted_email(db, email=blacklist_email.email):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"is_blacklisted": False, "reason": "Email already blacklisted"},
        )
    # Add requester ip

    blacklist_email = crud.create_blacklist_email(
        db=db, blacklist_email=blacklist_email, ip=request.client.host
    )
    response.status_code = status.HTTP_201_CREATED
    return {"is_blacklisted": True, "result": blacklist_email.blocked_reason}


# Chek if email is blacklisted
@prefix_router.get(
    "/{email}",
    response_model=schemas.BlacklistSearchResponse,
)
def check_blacklist_email(
    email: str,
    db: Session = Depends(get_db),
    authorization: Annotated[Optional[str], Header()] = None,
):
    authenticate(authorization)
    email_blacklisted = crud.get_blacklisted_email(db, email=email)
    return {
        "is_blacklisted": True if email_blacklisted else False,
        "blocked_reason": (
            email_blacklisted.blocked_reason if email_blacklisted else None
        ),
    }


# Rest the database
@prefix_router.post("/reset", response_model=schemas.DeleteResponse)
def reset(db: Session = Depends(get_db)):
    models.Base.metadata.drop_all(bind=db.get_bind())
    models.Base.metadata.create_all(bind=db.get_bind())
    db.commit()
    return schemas.DeleteResponse()




app.include_router(prefix_router)
