from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from src.database import Base

class DataSource(Base):
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, index=True)
    source_type = Column(String)
    connection_details = Column(JSON)  # Change this to JSON type
    created_at = Column(TIMESTAMP, server_default=func.now())
