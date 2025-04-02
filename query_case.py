# 案件查詢示例
def query_case_example(case_number):
    info = get_case_info(case_number, case_index)
    print(f"\n案件 {case_number} 的資訊：")
    for key, value in info.items():
        if pd.notna(value):  # 只顯示非空值
            print(f"{key}: {value}")