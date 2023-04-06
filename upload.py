import os
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import CSVFile, CSVFileCreate, CSVFileUpdate, User
from utils import allowed_file


router = APIRouter()


@router.get("/files", response_model=List[CSVFile])
def get_all_csv_files(db: Session = Depends(get_db)):
    """
    Returns a list of all CSV files uploaded by all users
    """
    files = db.query(CSVFile).all()
    return files


@router.get("/files/user", response_model=List[CSVFile])
def get_user_csv_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns a list of all CSV files uploaded by the current user
    """
    files = db.query(CSVFile).filter_by(user_id=current_user.id).all()
    return files


@router.post("/files", response_model=CSVFile)
def create_csv_file(csv_file: UploadFile = File(...), db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    """
    Uploads a new CSV file for the current user
    """
    if not allowed_file(csv_file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")
    if csv_file.filesize > 250000000:
        raise HTTPException(status_code=400, detail="File size too large. Max file size is 250MB")

    # Save the CSV file to the server
    upload_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, csv_file.filename)
    with open(file_path, "wb") as f:
        f.write(csv_file.file.read())

    # Add the CSV file to the database
    csv_file_data = CSVFileCreate(
        name=csv_file.filename,
        size=csv_file.filesize,
        upload_time=datetime.now(),
        user_id=current_user.id
    )
    csv_file_db = CSVFile(**csv_file_data.dict())
    db.add(csv_file_db)
    db.commit()
    db.refresh(csv_file_db)

    return csv_file_db


@router.delete("/files/{file_id}")
def delete_csv_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes a CSV file uploaded by the current user
    """
    csv_file = db.query(CSVFile).filter_by(id=file_id).first()
    if not csv_file:
        raise HTTPException(status_code=404, detail="CSV file not found")
    if csv_file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this file")

    # Delete the CSV file from the server
    file_path = os.path.join(os.getcwd(), "uploads", csv_file.name)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the CSV file from the database
    db.delete(csv_file)
    db.commit()

    return {"detail": "CSV file deleted successfully"}
