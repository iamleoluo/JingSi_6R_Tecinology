import json
from typing import Dict, List, Any
from dataclasses import dataclass
from decimal import Decimal
import os
from datetime import datetime

@dataclass
class CompanyInfo:
    name: str
    tax_id: str
    bank_name: str
    bank_address: str
    account_number: str
    address: str

# Known company information
KNOWN_COMPANIES = {
    "世博科技顧問股份有限公司": CompanyInfo(
        name="世博科技顧問股份有限公司",
        tax_id="28182234",
        bank_name="中國信託商業銀行承德分行",
        bank_address="103 台北市大同區承德路一段 17 號",
        account_number="624-540-153660",
        address=""
    ),
    "淨斯人間志業股份有限公司": CompanyInfo(
        name="淨斯人間志業股份有限公司",
        tax_id="42825510",
        bank_name="",
        bank_address="",
        account_number="",
        address="台北市大安區昌隆里忠孝東路3段217巷7弄19號1樓"
    )
}

class BillingVerifier:
    def __init__(self, json_data: Dict[str, Any]):
        self.data = json_data
        self.errors = []
        self.verification_results = []
        self.page2_details = []

    def verify_page1_payment(self):
        """Verify page 1 payment calculations"""
        service_fee = self.data["page1"]["服務費"]
        official_fee = self.data["page1"]["官費"]
        total_payment = self.data["page1"]["付款金額"]
        
        if service_fee + official_fee != total_payment:
            self.errors.append(f"Page 1: 服務費({service_fee}) + 官費({official_fee}) != 付款金額({total_payment})")
            self.verification_results.append("❌ Page 1 付款金額驗證失敗")
        else:
            self.verification_results.append("✅ Page 1 付款金額驗證通過：服務費 + 官費 = 付款金額")

    def verify_page2_details(self):
        """Verify page 2 detailed calculations"""
        all_items_valid = True
        for item in self.data["page2"]["費用明細清單"]:
            service_fee = item["服務費 (NTD)"]
            converted_fee = item["折算金額 (NTD)"]
            total_fee = item["服務費及官費合計 (NTD)"]
            
            # Store item details for reporting
            item_details = {
                "序號": item["序號"],
                "申請人": item["申請人"],
                "案件名稱": item["案件名稱"],
                "服務項目": item["服務項目"],
                "服務費 (NTD)": service_fee,
                "折算金額 (NTD)": converted_fee,
                "合計 (NTD)": total_fee,
                "原幣金額": item["原幣金額"],
                "匯率": item["匯率"],
                "計算結果": "正確" if service_fee + converted_fee == total_fee else "錯誤"
            }
            self.page2_details.append(item_details)
            
            if service_fee + converted_fee != total_fee:
                self.errors.append(f"Page 2: 序號 {item['序號']} 服務費({service_fee}) + 折算金額({converted_fee}) != 合計({total_fee})")
                all_items_valid = False
            
            # Verify currency conversion
            if item["原幣金額"] and item["匯率"]:
                expected_converted = round(item["原幣金額"] * item["匯率"], 2)
                if abs(expected_converted - converted_fee) > 0.5:  # Allow small floating point differences
                    self.errors.append(f"Page 2: 序號 {item['序號']} 原幣金額({item['原幣金額']}) * 匯率({item['匯率']}) != 折算金額({converted_fee})")
                    all_items_valid = False
        
        if all_items_valid:
            self.verification_results.append("✅ Page 2 費用明細驗證通過：所有項目服務費 + 折算金額 = 合計，且匯率計算正確")
        else:
            self.verification_results.append("❌ Page 2 費用明細驗證失敗")

    def verify_page3_invoice(self):
        """Verify page 3 invoice calculations"""
        service_amount = self.data["page3"]["發票金額"]["服務費金額"]
        tax_amount = self.data["page3"]["發票金額"]["營業稅金額"]
        total_amount = self.data["page3"]["發票金額"]["總金額"]
        
        invoice_valid = True
        
        if service_amount + tax_amount != total_amount:
            self.errors.append(f"Page 3: 服務費金額({service_amount}) + 營業稅金額({tax_amount}) != 總金額({total_amount})")
            invoice_valid = False
        
        # Verify page 3 total matches page 1 service fee
        if total_amount != self.data["page1"]["服務費"]:
            self.errors.append(f"Page 3 總金額({total_amount}) != Page 1 服務費({self.data['page1']['服務費']})")
            invoice_valid = False
        
        if invoice_valid:
            self.verification_results.append("✅ Page 3 發票金額驗證通過：服務費金額 + 營業稅金額 = 總金額，且與 Page 1 服務費相符")
        else:
            self.verification_results.append("❌ Page 3 發票金額驗證失敗")

    def verify_page4_official_fees(self):
        """Verify page 4 official fees"""
        official_fee_total = sum(item["金額"] for item in self.data["page4"]["官(規)費明細"])
        if official_fee_total != self.data["page1"]["官費"]:
            self.errors.append(f"Page 4 官費總計({official_fee_total}) != Page 1 官費({self.data['page1']['官費']})")
            self.verification_results.append("❌ Page 4 官費驗證失敗")
        else:
            self.verification_results.append("✅ Page 4 官費驗證通過：官費總計與 Page 1 官費相符")

    def verify_company_info(self):
        """Verify company information consistency"""
        # Check remittance info
        remittance_info = self.data["page1"]["匯款資訊"]
        remittance_valid = False
        for company in KNOWN_COMPANIES.values():
            if (company.tax_id == remittance_info["統一編號"] and
                company.bank_name == remittance_info["匯款銀行"] and
                company.bank_address == remittance_info["銀行地址"] and
                company.account_number == remittance_info["帳號"]):
                remittance_valid = True
                break
        
        if not remittance_valid:
            self.errors.append("Page 1 匯款資訊與已知公司資料不匹配")
            self.verification_results.append("❌ Page 1 匯款資訊驗證失敗")
        else:
            self.verification_results.append("✅ Page 1 匯款資訊驗證通過：與已知公司資料相符")

        # Check invoice info
        invoice_info = self.data["page3"]["發票資訊"]
        invoice_valid = False
        for company in KNOWN_COMPANIES.values():
            if (company.name == invoice_info["買方"] and
                company.tax_id == invoice_info["統一編號"] and
                company.address == invoice_info["地址"]):
                invoice_valid = True
                break
        
        if not invoice_valid:
            self.errors.append("Page 3 發票資訊與已知公司資料不匹配")
            self.verification_results.append("❌ Page 3 發票資訊驗證失敗")
        else:
            self.verification_results.append("✅ Page 3 發票資訊驗證通過：與已知公司資料相符")

    def verify_all(self):
        """Run all verification checks"""
        self.verify_page1_payment()
        self.verify_page2_details()
        self.verify_page3_invoice()
        self.verify_page4_official_fees()
        self.verify_company_info()
        
        return self.errors, self.verification_results, self.page2_details

def verify_billing_file(file_path: str) -> tuple[List[str], List[str], List[Dict]]:
    """Verify a billing JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    verifier = BillingVerifier(data)
    return verifier.verify_all()

def save_verification_results(file_path: str, errors: List[str], verification_results: List[str], page2_details: List[Dict]):
    """Save verification results to a JSON file"""
    # Create results directory if it doesn't exist
    results_dir = "bills_information/json_verification_result"
    os.makedirs(results_dir, exist_ok=True)
    
    # Get the original filename without extension
    original_filename = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create result filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_filename = f"{original_filename}_verification_{timestamp}.json"
    result_path = os.path.join(results_dir, result_filename)
    
    # Prepare verification results
    verification_data = {
        "verification_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_file": file_path,
        "verification_results": verification_results,
        "errors": errors,
        "page2_details": page2_details,
        "overall_status": "通過" if not errors else "失敗"
    }
    
    # Save to JSON file
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(verification_data, f, ensure_ascii=False, indent=2)
    
    return result_path

if __name__ == "__main__":
    # Example usage
    file_path = "bills_information/bills_info_json/240618-WP2405002GP-淨斯-請款單(CN,US)-v1F.json"
    errors, verification_results, page2_details = verify_billing_file(file_path)
    
    # Save verification results
    result_path = save_verification_results(file_path, errors, verification_results, page2_details)
    
    print("\n=== 帳單驗證報告 ===")
    print("\n驗證項目：")
    for result in verification_results:
        print(f"- {result}")
    
    if errors:
        print("\n發現以下錯誤：")
        for error in errors:
            print(f"- {error}")
        
        # Print detailed Page 2 information if verification failed
        if "Page 2 費用明細驗證失敗" in [r for r in verification_results if r.startswith("❌")]:
            print("\n=== Page 2 費用明細 ===")
            for item in page2_details:
                print(f"\n序號: {item['序號']}")
                print(f"申請人: {item['申請人']}")
                print(f"案件名稱: {item['案件名稱']}")
                print(f"服務項目: {item['服務項目']}")
                print(f"服務費 (NTD): {item['服務費 (NTD)']}")
                print(f"折算金額 (NTD): {item['折算金額 (NTD)']}")
                print(f"合計 (NTD): {item['合計 (NTD)']}")
                if item['原幣金額']:
                    print(f"原幣金額: {item['原幣金額']}")
                    print(f"匯率: {item['匯率']}")
                print(f"計算結果: {item['計算結果']}")
    else:
        print("\n所有驗證通過，沒有發現錯誤。")
    
    print(f"\n驗證結果已儲存至: {result_path}")