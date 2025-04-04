# Patent and Invoicing Management System

This project provides two comprehensive solutions:
1. Patent case management and analysis
2. Invoicing information verification and management

## 1. Patent Case Management System

### Features
- Data preprocessing and categorization
- Case searching by case number
- Cross-analysis between different patent attributes
- Export results to CSV format
- Support for Chinese characters

### Project Structure
The patent management system consists of three main Python scripts:

1. `1. load_data_and_pre-processing.py`
   - Loads the patent data from CSV
   - Creates categorized dictionaries for different patent attributes
   - Saves categorized data as JSON files

2. `2. searching.py`
   - Provides case searching functionality
   - Allows querying specific case information
   - Supports dynamic CSV file path changes

3. `3. compare.py`
   - Performs cross-analysis between different patent attributes
   - Generates comparison matrices
   - Exports results to CSV files

### Usage
```python
from load_data_and_pre-processing import PatentDataProcessor

# Define category configurations
category_configs = [
    {'column_name': '案件狀態', 'output_filename': 'status_dict.json'},
    {'column_name': '專利種類', 'output_filename': 'patent_type_dict.json'},
    {'column_name': '申請國家', 'output_filename': 'country_dict.json'},
    {'column_name': '專利權人', 'output_filename': 'owner_dict.json'},
    {'column_name': '事務所名稱', 'output_filename': 'agency_dict.json'}
]

# Create processor instance and process data
processor = PatentDataProcessor('20250402export.csv')
processor.load_data().process_categories(category_configs).save_all_to_json()
```

## 2. Invoicing Information System

### Features
- Invoicing information verification and validation
- JSON file loading and display
- Multi-page payment verification
- Currency conversion validation
- Company information consistency checks

### Project Structure
The invoicing system consists of two main Python scripts:

1. `Invoicing information_calculation_and_verification.py`
   - Verifies payment calculations across multiple pages
   - Validates service fees, official fees, and total payments
   - Checks currency conversion and exchange rates
   - Verifies company information consistency
   - Generates detailed verification reports
   - Saves verification results in JSON format

2. `Load_invoicing_info.py`
   - Loads and displays invoicing information from JSON files
   - Shows detailed breakdown of payment information
   - Displays service fee details and invoice information
   - Presents official fee breakdowns

### Usage

#### Invoicing Verification
```python
from Invoicing information_calculation_and_verification import verify_invoicing_file, save_verification_results

# Verify an invoicing file
file_path = "invoices_information/invoices_info_json/example.json"
errors, verification_results, details = verify_invoicing_file(file_path)

# Save verification results
result_path = save_verification_results(file_path, errors, verification_results, details)
```

#### Loading Invoicing Information
```python
# Run the script and input the JSON filename when prompted
python Load_invoicing_info.py
```

The script will display:
- Basic payment information
- Remittance details
- Service fee breakdown
- Invoice information
- Official fee details

## Dependencies

- pandas
- numpy
- json
- datetime
- collections

## Input Data Format

### Patent System
The system expects a CSV file with the following columns:
- 公司案號 (Company Case Number)
- 案件狀態 (Case Status)
- 專利種類 (Patent Type)
- 申請國家 (Application Country)
- 專利權人 (Patent Owner)
- 事務所名稱 (Agency Name)

### Invoicing System
The system expects JSON files with the following structure:
- Page 1: Basic payment information
- Page 2: Detailed service fees
- Page 3: Invoice information
- Page 4: Official fees

## Output

### Patent System
- Processed data is saved in JSON format in the `status_check_result` directory
- Cross-analysis results are saved as CSV files in the `compare_result` directory
- Search results are displayed in the console

### Invoicing System
- Verification results are saved in JSON format in the `invoices_information/json_verification_result` directory
- All timestamps in output files are in the format YYYYMMDD_HHMMSS
- The system automatically creates necessary directories if they don't exist

## Notes

- The system supports Chinese characters in both input and output
- All timestamps in output files are in the format YYYYMMDD_HHMMSS
- The system automatically creates necessary directories if they don't exist 
