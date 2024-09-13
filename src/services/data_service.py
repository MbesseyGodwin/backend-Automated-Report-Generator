# backend/src/services/data_service.py

from sqlalchemy.orm import Session
from src.models.report import Report

class DataService:
    def __init__(self, db):
        self.db = db

    def get_report_data(self, report_id: int):
        report = self.db.query(Report).filter(Report.id == report_id).first()
        return report
