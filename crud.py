from sqlalchemy.orm import Session
from typing import Optional


from models import BlacklistEmail
from schemas import CreateBlacklistEmail


def get_blacklisted_email(db: Session, email: str) -> Optional[BlacklistEmail]:
    return db.query(BlacklistEmail).filter(BlacklistEmail.email == email).first()


def create_blacklist_email(db: Session, blacklist_email: CreateBlacklistEmail, ip):
    blacklist_email = BlacklistEmail(**blacklist_email.model_dump(), ip=ip)
    db.add(blacklist_email)
    db.commit()
    db.refresh(blacklist_email)
    return blacklist_email
