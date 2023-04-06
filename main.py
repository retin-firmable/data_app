from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError

from database import engine, SessionLocal, Base
from models import User, UserType, CSVFile
from schemas import UserCreate, UserOut, CSVFileOut
from crud import get_user_by_email, create_user, delete_user, delete_csv_file
from auth import get_current_user

import csv
import io

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/admin/users", response_model=UserOut)
def admin_create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")
    return create_user(db, user)


@app.delete("/admin/users/{user_id}")
def admin_delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")
    delete_user(db, user_id)
    return {"detail": "User deleted"}


@app.delete("/admin/csv/{csv_id}")
def admin_delete_csv_file(csv_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")
    delete_csv_file(db, csv_id)
    return {"detail": "CSV file deleted"}


@app.post("/csv", response_model=CSVFileOut)
def upload_csv_file(csv_file: UploadFile = File(...), db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if csv_file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file format")
    if csv_file.filesize > 250000000:
        raise HTTPException(status_code=400, detail="File size too large. Max file size is 250MB")

    csv_data = csv.reader(io.StringIO(csv_file.file.read().decode('utf-8')))
    rows = [row for row in csv_data]
    columns = rows[0]
    data = rows[1:]

    csv_file_db = CSVFile(
        name=csv_file.filename,
        data=data,
        columns=columns,
        size=csv_file.filesize,
        upload_time=datetime.utcnow(),
        user_id=current_user.id
    )

    db.add(csv_file_db)
    db.commit()
    db.refresh(csv_file_db)
    return csv_file_db
