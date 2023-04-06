from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from .models import CSVFile, CSVFileOut
from .auth import get_current_user, is_admin
from .crud import get_csv_file_by_id, get_csv_files_by_user_id, update_csv_file_columns

router = APIRouter()


@router.get("/csv/{csv_file_id}", response_model=CSVFileOut)
def get_csv_file(csv_file_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    csv_file = get_csv_file_by_id(db, csv_file_id)
    if not csv_file:
        raise HTTPException(status_code=404, detail="CSV file not found")
    if csv_file.user_id != current_user.id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized")
    return csv_file


@router.get("/csv/user", response_model=List[CSVFileOut])
def get_csv_files_by_user(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    if is_admin(current_user):
        csv_files = db.query(CSVFile).all()
    else:
        csv_files = get_csv_files_by_user_id(db, current_user.id)
    return csv_files


@router.put("/csv/{csv_file_id}/columns", response_model=CSVFileOut)
def update_csv_file(csv_file_id: int, column_names: List[str], db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    csv_file = get_csv_file_by_id(db, csv_file_id)
    if not csv_file:
        raise HTTPException(status_code=404, detail="CSV file not found")
    if csv_file.user_id != current_user.id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_csv_file = update_csv_file_columns(db, csv_file, column_names)
    return updated_csv_file
