from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os

# Define the database URL
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    files = relationship("File", back_populates="owner")

# Define the File model
class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filesize = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")

# Initialize the database
Base.metadata.create_all(bind=engine)

# Define the CRUD operations for User
def get_user_by_username(db_session, username: str):
    return db_session.query(User).filter(User.username == username).first()

def get_user_by_id(db_session, user_id: int):
    return db_session.query(User).filter(User.id == user_id).first()

def create_user(db_session, username: str, password: str, role: str):
    db_user = User(username=username, password=password, role=role)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

def delete_user(db_session, user_id: int):
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.commit()

# Define the CRUD operations for File
def create_file(db_session, filename: str, filesize: int, owner: User):
    db_file = File(filename=filename, filesize=filesize, owner=owner)
    db_session.add(db_file)
    db_session.commit()
    db_session.refresh(db_file)
    return db_file

def get_file_by_id(db_session, file_id: int):
    return db_session.query(File).filter(File.id == file_id).first()

def get_files_by_owner(db_session, owner_id: int):
    return db_session.query(File).filter(File.owner_id == owner_id).all()

def delete_file(db_session, file_id: int):
    db_session.query(File).filter(File.id == file_id).delete()
    db_session.commit()

def update_filename(db_session, file_id: int, filename: str):
    db_session.query(File).filter(File.id == file_id).update({
        "filename": filename,
    })
    db_session.commit()
