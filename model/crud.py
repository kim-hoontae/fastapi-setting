import bcrypt
from sqlalchemy.orm import Session

from model import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode
    db_user = models.User(email=user.email, password=hashed_password, name=user.ame)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user