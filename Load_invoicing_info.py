import json
file_name = input("請輸入 JSON 檔案名稱: ")
# 讀取 JSON 檔案
with open(f'bills_information/json_verification_result/{file_name}', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Page 1
p1 = data['details']['page1']
print("=== Page 1 基本資訊 ===")
print(f"單號：{p1['單號']}")
print(f"日期：{p1['日期']}")
print(f"服務費：{p1['服務費']}")
print(f"官費：{p1['官費']}")
print(f"付款金額：{p1['付款金額']}")
print(f"付款期限：{p1['付款期限']}")

print("\n=== 匯款資訊 ===")
for key, value in p1['匯款資訊'].items():
    print(f"{key}：{value}")

# Page 2
print("\n=== Page 2 明細列表 ===")
for item in data['details']['page2']:
    print(f"[{item['序號']}] {item['申請人']} | {item['案件名稱']} | {item['服務項目']} | 服務費: {item['服務費 (NTD)']} | 合計: {item['合計 (NTD)']}")

# Page 3
p3 = data['details']['page3']
print("\n=== Page 3 發票資訊 ===")
inv = p3['發票資訊']
print(f"發票號碼：{inv['發票號碼']}")
print(f"買方：{inv['買方']}")
print(f"統一編號：{inv['統一編號']}")
print(f"地址：{inv['地址']}")
print("金額資訊：")
print(f"  服務費金額：{p3['發票金額']['服務費金額']}")
print(f"  營業稅金額：{p3['發票金額']['營業稅金額']}")
print(f"  總金額：{p3['發票金額']['總金額']}")