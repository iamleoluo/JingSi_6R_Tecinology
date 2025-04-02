import pandas as pd
import numpy as np
from collections import defaultdict
import json
import os

class PatentDataProcessor:
    def __init__(self, csv_file_path):
        """
        Initialize the PatentDataProcessor with a CSV file path.
        
        Args:
            csv_file_path (str): Path to the CSV file containing patent data
        """
        self.csv_file_path = csv_file_path
        self.df = None
        self.category_dicts = {}
        self.output_dir = "status_check_result"
        
    def load_data(self):
        """
        Load data from the CSV file.
        
        Returns:
            self: Returns the instance for method chaining
        """
        self.df = pd.read_csv(self.csv_file_path)
        return self
    
    def create_category_dict(self, column_name):
        """
        Create a dictionary mapping categories to case numbers.
        
        Args:
            column_name (str): The column name to categorize by
            
        Returns:
            dict: Dictionary mapping categories to lists of case numbers
        """
        category_dict = defaultdict(list)
        for index, row in self.df.iterrows():
            category = row[column_name]
            case_number = row['公司案號']
            if pd.notna(category) and pd.notna(case_number):  # Ensure values are not NaN
                category_dict[category].append(case_number)
        return dict(category_dict)
    
    def process_categories(self, category_configs):
        """
        Process multiple categories based on user configuration.
        
        Args:
            category_configs (list): List of dictionaries with 'column_name' and 'output_filename' keys
            
        Returns:
            self: Returns the instance for method chaining
        """
        for config in category_configs:
            column_name = config['column_name']
            output_filename = config['output_filename']
            
            # Create the dictionary for this category
            self.category_dicts[output_filename] = self.create_category_dict(column_name)
            
        return self
    
    def save_dict_to_json(self, data_dict, filename):
        """
        Save dictionary data to a JSON file.
        
        Args:
            data_dict: Dictionary to save
            filename: Output filename (without path)
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Save dictionary to JSON file
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)
        
        print(f"已保存 {filename} 到 {self.output_dir} 目錄")
    
    def save_all_to_json(self):
        """
        Save all category dictionaries to JSON files.
        
        Returns:
            self: Returns the instance for method chaining
        """
        for filename, data_dict in self.category_dicts.items():
            self.save_dict_to_json(data_dict, filename)
        
        return self


# Example usage:
if __name__ == "__main__":
    # Define category configurations with Chinese column names and English output filenames
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

