# backend/src/utils/report_generator.py

from .data_loader import DataLoader
# Corrected import statement
from .pdf_creator import PDFCreator


class ReportGenerator:
    def __init__(self, data_service):
        self.data_service = data_service

    def generate_report(self, report_id: int):
        # Fetch data for the report
        report_data = self.data_service.get_report_data(report_id)
        
        # Generate PDF report
        pdf_creator = PDFCreator()
        pdf_creator.create_pdf(report_data)
