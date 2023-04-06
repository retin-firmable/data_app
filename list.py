from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db
from .auth import get_current_user
from .models import User, CSVFile
from .schemas import CSVFileList


router = APIRouter(prefix="/list", tags=["List"])


@router.get("/", response_model=List[CSVFileList])
def list_csv_files(db: Session = Depends(get_db)):
    """
    List all CSV files uploaded by all users
    """
    csv_files = db.query(CSVFile).all()
    csv_files_list = []
    for csv_file in csv_files:
        csv_file_dict = csv_file.__dict__
        csv_file_dict['uploaded_at'] = datetime.strftime(csv_file_dict['uploaded_at'], "%Y-%m-%d %H:%M:%S")
        csv_file_dict.pop('_sa_instance_state')
        csv_files_list.append(csv_file_dict)
    return csv_files_list


@router.get(f"/{username}", response_model=List[CSVFileList])
def list_user_csv_files(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    List all CSV files uploaded by a specific user
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.role == "user" and current_user.username != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to view other users' files")
    csv_files = db.query(CSVFile).filter(CSVFile.uploader_id == user.id).all()
    csv_files_list = []
    for csv_file in csv_files:
        csv_file_dict = csv_file.__dict__
        csv_file_dict['uploaded_at'] = datetime.strftime(csv_file_dict['uploaded_at'], "%Y-%m-%d %H:%M:%S")
        csv_file_dict.pop('_sa_instance_state')
        csv_files_list.append(csv_file_dict)
    return csv_files_list
