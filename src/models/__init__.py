from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql://admin:Admin123@localhost/report_generator_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import all your models here so that Alembic can recognize them
# from .user import User
# from .report import Report

from .user import User
from .data_source import DataSource
from .report import Report

__all__ = ["User", "Report", "DataSource"]

