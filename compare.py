import pandas as pd
import json
import numpy as np
from datetime import datetime
import os

class CrossAnalyzer:
    def __init__(self, result_dir="status_check_result"):
        self.result_dir = result_dir
        self.available_dicts = self._load_available_dicts()
        
    def _load_available_dicts(self):
        """Load all JSON files from the result directory"""
        available_dicts = {}
        for idx, filename in enumerate(os.listdir(self.result_dir), 1):
            if filename.endswith('.json'):
                available_dicts[str(idx)] = filename
        return available_dicts
    
    def _load_json(self, filepath):
        """Load a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_cross_analysis(self, dict1_path, dict2_path, output_csv=True):
        # 讀取JSON文件
        dict1 = self._load_json(dict1_path)
        dict2 = self._load_json(dict2_path)
        
        # 獲取所有唯一的類別
        categories1 = list(dict1.keys())
        categories2 = list(dict2.keys())
        
        # 創建一個空的DataFrame
        df = pd.DataFrame(index=categories1, columns=categories2)
        
        # 填充DataFrame
        for cat1 in categories1:
            for cat2 in categories2:
                # 找出兩個類別的交集
                common_cases = list(set(dict1[cat1]) & set(dict2[cat2]))
                # 如果有交集，填入案號，否則填入空字符串
                df.at[cat1, cat2] = ', '.join(common_cases) if common_cases else ''
        
        # 添加總計行和列
        df['總計'] = [len(dict1[cat]) for cat in categories1]
        
        # 計算每個列的總計
        row_totals = pd.Series([len(dict2[cat]) for cat in categories2], index=categories2)
        
        # 確保總計行不會與總計列衝突
        df.loc['總計'] = row_totals
        
        # 計算整個項目的總數
        row_sum = sum(len(dict1[cat]) for cat in categories1)
        col_sum = sum(len(dict2[cat]) for cat in categories2)
        
        # 檢查總數是否一致
        if row_sum == col_sum:
            df.at['總計', '總計'] = row_sum
            print(f"項目總數: {row_sum}")
        else:
            raise ValueError(f"總計不一致: 行總計={row_sum}, 列總計={col_sum}")
        
        if output_csv:
            # 生成時間戳記
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 從文件路徑中提取字典名稱
            dict1_name = os.path.basename(dict1_path).replace('.json', '')
            dict2_name = os.path.basename(dict2_path).replace('.json', '')
            
            # 創建輸出文件名
            output_filename = f'cross_analysis_{dict1_name}_vs_{dict2_name}_{timestamp}.csv'
            
            # 確保輸出目錄存在
            os.makedirs("compare_result", exist_ok=True)
            
            # 保存為CSV
            output_path = os.path.join("compare_result", output_filename)
            df.to_csv(output_path, encoding='utf-8-sig')
            print(f"\n分析結果已保存至: {output_filename}")
        
        return df
    
    def run_analysis(self):
        """Run the cross-analysis with user input"""
        # 顯示可用的字典
        print("可用的字典文件：")
        for key, value in self.available_dicts.items():
            print(f"{key}: {value}")
        
        # 獲取用戶輸入
        print("\n請選擇要交叉比對的兩個字典（輸入編號）：")
        dict1_num = input("第一個字典編號: ")
        dict2_num = input("第二個字典編號: ")
        
        # 驗證輸入
        if dict1_num not in self.available_dicts or dict2_num not in self.available_dicts:
            raise ValueError("無效的字典編號")
        
        # 獲取文件路徑
        dict1_path = os.path.join(self.result_dir, self.available_dicts[dict1_num])
        dict2_path = os.path.join(self.result_dir, self.available_dicts[dict2_num])
        
        # 創建交叉分析表格並保存為CSV
        result_df = self.create_cross_analysis(dict1_path, dict2_path, output_csv=True)
        
        # 顯示結果
        print(f"\n交叉分析結果 ({self.available_dicts[dict1_num]} vs {self.available_dicts[dict2_num]}):")
        
        # 設置顯示選項
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        
        return result_df

if __name__ == "__main__":
    analyzer = CrossAnalyzer()
    result = analyzer.run_analysis()