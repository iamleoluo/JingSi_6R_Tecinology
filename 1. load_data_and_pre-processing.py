import pandas as pd
import numpy as np
from collections import defaultdict

# save as json in status_check_result
import json
import os

# 讀取CSV文件
df = pd.read_csv('20250402export.csv')

# 建立各種分類的字典
def create_category_dict(df, column_name):
    category_dict = defaultdict(list)
    for index, row in df.iterrows():
        category = row[column_name]
        case_number = row['公司案號']
        if pd.notna(category) and pd.notna(case_number):  # 確保值不是NaN
            category_dict[category].append(case_number)
    return dict(category_dict)

# 建立所有所需分類
status_dict = create_category_dict(df, '案件狀態')
patent_type_dict = create_category_dict(df, '專利種類')
country_dict = create_category_dict(df, '申請國家')
owner_dict = create_category_dict(df, '專利權人')
agency_dict = create_category_dict(df, '事務所名稱')

def save_dict_to_json(data_dict, filename):
    """
    保存字典數據到JSON文件
    
    Args:
        data_dict: 要保存的字典數據
        filename: 文件名（不含路徑）
    """
    # 創建輸出目錄（如果不存在）
    if not os.path.exists("status_check_result"):
        os.makedirs("status_check_result")
    
    # 保存字典到 JSON 文件
    file_path = os.path.join("status_check_result", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
    
    print(f"已保存 {filename} 到 status_check_result 目錄")


# save status_dict to json
save_dict_to_json(status_dict, "status_dict.json")


# save patent_type_dict to json
save_dict_to_json(patent_type_dict, "patent_type_dict.json")


# save country_dict to json
save_dict_to_json(country_dict, "country_dict.json")


# save owner_dict to json
save_dict_to_json(owner_dict, "owner_dict.json")

# save agency_dict to json
save_dict_to_json(agency_dict, "agency_dict.json")

