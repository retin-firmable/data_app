from sqlalchemy.orm import Session
import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_csvfile(db: Session, csvfile_id: int):
    return db.query(models.CSVFile).filter(models.CSVFile.id == csvfile_id).first()

def get_csvfiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CSVFile).offset(skip).limit(limit).all()

def create_csvfile(db: Session, csvfile: schemas.CSVFileCreate, user_id: int):
    db_csvfile = models.CSVFile(**csvfile.dict(), owner_id=user_id)
    db.add(db_csvfile)
    db.commit()
    db.refresh(db_csvfile)
    return db_csvfile

def delete_csvfile(db: Session, csvfile_id: int):
    db.query(models.CSVFile).filter(models.CSVFile.id == csvfile_id).delete()
    db.commit()
