from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.user import User
from src.models.report import Report
from src.models.data_source import DataSource
from src.schemas import UserCreate, UserLogin, ReportCreate, DataSourceCreate, TestConnection, UserOut, ReportOut, DataSourceOut
from src.utils import hash_password, verify_password, generate_jwt_token
from src.services.data_service import DataService
from src.utils.report_generator import ReportGenerator

from passlib.context import CryptContext

import jwt
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_jwt_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Generated JWT: {encoded_jwt}")  # Add this line for debugging
    return encoded_jwt


# FastAPI app initialization
app = FastAPI()

origins = [
    "http://localhost:3000",  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE_URL = "mysql://admin:Admin123@localhost/report_generator_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize services
@app.on_event("startup")
def startup_event():
    global data_service
    db = next(get_db())
    data_service = DataService(db)
    global report_generator
    report_generator = ReportGenerator(data_service)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Report Generator API"}

# User registration
@app.post("/users/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



# User login
@app.post("/users/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = generate_jwt_token(db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}



# Password reset
@app.post("/users/reset-password")
def reset_password(email: str, new_password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = hash_password(new_password)
    db_user.password_hash = hashed_password
    db.commit()
    return {"message": "Password updated successfully"}


# Get user details
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_from_database(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# def get_user_from_database(user_id: int, db: Session) -> UserOut:
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         return None
#     # Convert the SQLAlchemy model to Pydantic model
#     return UserOut.from_orm(db_user)

def get_user_from_database(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        # Convert datetime to string if needed
        return {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
            "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None,
        }
    return None



# Data source management
@app.post("/data-sources", response_model=DataSourceOut)
def add_data_source(data_source: DataSourceCreate, db: Session = Depends(get_db)):
    db_data_source = DataSource(**data_source.dict())
    db.add(db_data_source)
    db.commit()
    db.refresh(db_data_source)
    
    # Convert to dict if necessary, for example:
    # return db_data_source.dict()
    
    # Or convert to a Pydantic model explicitly
    return DataSourceOut.from_orm(db_data_source)

@app.put("/data-sources/{source_id}", response_model=DataSourceOut)
def update_data_source(source_id: int, data_source: DataSourceCreate, db: Session = Depends(get_db)):
    db_data_source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if db_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    for key, value in data_source.dict().items():
        setattr(db_data_source, key, value)
    db.commit()
    db.refresh(db_data_source)
    return db_data_source

@app.delete("/data-sources/{source_id}", response_model=dict)
def delete_data_source(source_id: int, db: Session = Depends(get_db)):
    db_data_source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if db_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    db.delete(db_data_source)
    db.commit()
    return {"message": "Data source deleted"}

@app.post("/data-sources/test-connection")
def test_connection(test: TestConnection, db: Session = Depends(get_db)):
    # Simulated connection test logic
    return {"message": "Connection successful"}




# Report management
@app.post("/reports", response_model=ReportOut)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports/{report_id}/download")
def download_report(report_id: int, format: str, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    # Simulate report generation and return URL or file path
    return {"url": f"/reports/{report_id}/download?format={format}"}

@app.get("/reports/{report_id}", response_model=ReportOut)
def get_report_metadata(report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@app.post("/report-files")
def upload_report_file(report_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Simulate file upload logic
    return {"filename": file.filename, "report_id": report_id}

@app.get("/report-files/{report_id}")
def list_report_files(report_id: int, db: Session = Depends(get_db)):
    # Simulate file listing logic
    return [{"id": 1, "file_path": "/path/to/file", "created_at": "timestamp"}]

@app.get("/user-reports/{user_id}")
def get_user_reports(user_id: int, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    return reports

@app.get("/report-analytics")
def get_report_analytics(start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    # Simulated analytics logic
    return {
        "total_reports_generated": 100,
        "most_common_data_source": "Database",
        "report_generation_trends": {
            "daily": 10,
            "weekly": 50,
            "monthly": 200
        }
    }
