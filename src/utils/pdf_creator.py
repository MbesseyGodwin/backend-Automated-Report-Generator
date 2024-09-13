# backend/src/utils/pdf_creator.py

from fpdf import FPDF

class PDFCreator:
    def create_pdf(self, report_data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for data in report_data:
            pdf.cell(200, 10, txt=data, ln=True, align='L')
        pdf.output("report.pdf")
