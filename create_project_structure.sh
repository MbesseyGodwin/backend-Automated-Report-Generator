#!/bin/bash

# Create project root directory
mkdir automated-report-generator
cd automated-report-generator

# Backend structure
mkdir -p backend/src/{utils,models,services,tests}
touch backend/src/{__init__.py,main.py,config.py}
touch backend/src/utils/{__init__.py,data_loader.py,report_generator.py,pdf_creator.py,excel_creator.py}
touch backend/src/models/{__init__.py,report.py}
touch backend/src/services/{__init__.py,data_service.py}
touch backend/src/tests/{__init__.py,test_data_loader.py,test_report_generator.py}
touch backend/.env backend/requirements.txt backend/README.md backend/setup.py backend/.gitignore

# Frontend structure
mkdir -p frontend/src/{assets,components,pages,styles}
touch frontend/src/components/{ReportForm.tsx,ReportList.tsx,ReportViewer.tsx}
touch frontend/src/pages/{Home.tsx,Reports.tsx,About.tsx}
touch frontend/src/{App.tsx,index.tsx}
touch frontend/src/styles/tailwind.css
mkdir -p frontend/public
touch frontend/public/index.html
touch frontend/{tsconfig.json,package.json,tailwind.config.js,postcss.config.js,.gitignore}

# Project root files
touch .gitignore README.md

echo "Project structure created successfully!"
