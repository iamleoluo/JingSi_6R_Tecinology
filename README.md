# Patent Case Management and Analysis System

This project provides a comprehensive solution for managing and analyzing patent case data. It includes functionality for data preprocessing, case searching, and cross-analysis of different patent attributes.

## Features

- Data preprocessing and categorization
- Case searching by case number
- Cross-analysis between different patent attributes
- Export results to CSV format
- Support for Chinese characters

## Project Structure

The project consists of three main Python scripts:

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

## Dependencies

- pandas
- numpy
- json
- datetime
- collections

## Usage

1. **Data Preprocessing**
   ```bash
   python 1.load_data_and_pre-processing.py
   ```
   This will process the input CSV file and create categorized JSON files in the `status_check_result` directory.

2. **Case Searching**
   ```python
   from searching import CaseSearcher
   
   searcher = CaseSearcher()
   searcher.query_case('2024-001-T-TW')
   ```

3. **Cross Analysis**
   ```bash
   python 3.compare.py
   ```
   Follow the interactive prompts to select which attributes to compare.

## Input Data Format

The system expects a CSV file with the following columns:
- 公司案號 (Company Case Number)
- 案件狀態 (Case Status)
- 專利種類 (Patent Type)
- 申請國家 (Application Country)
- 專利權人 (Patent Owner)
- 事務所名稱 (Agency Name)

## Output

- Processed data is saved in JSON format in the `status_check_result` directory
- Cross-analysis results are saved as CSV files in the `compare_result` directory
- Search results are displayed in the console

## Notes

- The system supports Chinese characters in both input and output
- All timestamps in output files are in the format YYYYMMDD_HHMMSS
- The system automatically creates necessary directories if they don't exist 
