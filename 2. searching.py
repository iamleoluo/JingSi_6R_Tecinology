import pandas as pd
import numpy as np
from collections import defaultdict

class CaseSearcher:
    def __init__(self, csv_path=None):
        """
        Initialize the CaseSearcher with an optional CSV file path.
        If no path is provided, the default path will be used.
        """
        self.csv_path = csv_path or '20250402export.csv'
        self.df = None
        self.case_index = {}
        self.load_data()
    
    def load_data(self):
        """
        Load data from the CSV file and create the case index.
        """
        try:
            self.df = pd.read_csv(self.csv_path)
            self.case_index = self.create_case_index()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = None
            self.case_index = {}
    
    def change_csv_path(self, new_path):
        """
        Change the CSV file path and reload the data.
        """
        self.csv_path = new_path
        self.load_data()
    
    def create_case_index(self):
        """
        Create an index of cases from the dataframe.
        """
        case_index = {}  # Initialize empty dictionary to store case indices
        if self.df is None:
            return case_index
            
        for index, row in self.df.iterrows():  # Iterate through each row in the dataframe
            case_number = row['公司案號']  # Get the case number from the current row
            if pd.notna(case_number):  # Check if the case number is not null
                # Convert the current row to a dictionary and store it with the case number as the key
                case_index[case_number] = row.to_dict()
        return case_index  # Return the created case index dictionary
    
    def get_case_info(self, case_number):
        """
        Get information for a specific case number.
        """
        return self.case_index.get(case_number, "案件不存在")
    
    def query_case(self, case_number):
        """
        Query and display information for a specific case number.
        """
        info = self.get_case_info(case_number)
        if info == "案件不存在":
            print(f"\n案件 {case_number} 不存在")
            return
            
        print(f"\n案件 {case_number} 的資訊：")
        for key, value in info.items():
            if pd.notna(value):  # Only display non-null values
                print(f"{key}: {value}")


# Example usage
if __name__ == "__main__":
    # Create a CaseSearcher instance with default CSV path
    searcher = CaseSearcher()
    
    # Query a case example
    searcher.query_case('2024-001-T-TW')
    
    # Example of changing the CSV path
    # searcher.change_csv_path('new_export.csv')
    # searcher.query_case('2024-001-T-TW')