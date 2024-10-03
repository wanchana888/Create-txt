import csv
from datetime import datetime
import sys

# ฟังก์ชันเพื่อจัดรูปแบบข้อมูลให้มีความยาวคงที่
def fixed_width_format(data, width, align_left=True):
    if align_left:
        return str(data).ljust(width)
    else:
        return str(data).rjust(width)
    
  # ข้อมูลที่ต้องการใช้ในการสร้างไฟล์
# header = {
#     "record_type": "H",  # Header
#     "sequence_number": "000001",
#     "source_id" : "824",
#     "account_number": "1883047050",
#     "company_name": "SOCIAL SECURITY OFFICE [8D]",
#     "transaction_date": "25092024",
#     "time": "11000000"
# }

# transaction = {
#     "record_type": "D",  # Transaction
#     "sequence_number": "000002",
#     "source_id" : "824",
#     "account_number": "1883047050",
#     "transaction_date": "11092024",
#     "transaction_time": "141348",
#     "company_name": "ห้างหุ้นส่วนจำกัด พร พรหมรังสี พร็อพเพอร์ตี้",
#     "accountno": "73001428340025661",
#     "year": "2566",
#     "type": "1",
#     "invoicecode": "300066100006980",
#     "receiptno": "300067WQW000010",  
#     "branchNo" : "0000",
#     "tellerNo" : "0000",
#     "transaction_type": "CCSH",
#     "Cheque No" : "00000000",
#     "con_amount" : "00000001400",
#     "decimal" : "00",
#     "Cheque bank code": "000",
#     "Cheque bank branch": "0000"
# }

# footer = {
#     "record_type": "T",  # Footer
#     "sequence_number": "000003",
#     "account_number": "8241883047050",
#     "total_amount": "0000000000000000000000000534893",
#     "total_transactions": "0000010"
# }

# ฟังก์ชันในการเขียนไฟล์จากข้อมูลใน CSV
def write_to_txt(data_list, output_file="output.txt"):
    current_date = datetime.now().strftime("%d%m%Y")  # วันที่ปัจจุบัน
    current_time = datetime.now().strftime("%H%M%S")  # เวลาปัจจุบัน
    with open(output_file, "w", encoding="utf-8") as file:


        # เขียน Header
        file.write(
            fixed_width_format("H", 1) +  # Record type: Header
            fixed_width_format("000001", 6) +  # Sequence number
            fixed_width_format("824",3) +   # Source ID
            fixed_width_format("1883047050", 10) +  # Account number
            fixed_width_format("SOCIAL SECURITY OFFICE [8D]", 40) +  # Company name
            fixed_width_format(current_date, 8) +  # Transaction date
            fixed_width_format(current_time, 8) +  # Time
            "\n"
        )
        
        # เขียน Transactions จากข้อมูลใน CSV
        for idx, transaction in enumerate(data_list, start=2):
            file.write(
                fixed_width_format("D", 1) +  # Record type: Detail
                fixed_width_format(f"{idx:06}", 6) +  # Sequence number
                fixed_width_format("824", 3) +   # Source ID 
                fixed_width_format("1883047050", 10) +  # Account number
                fixed_width_format(current_date, 8) + +  # Transaction date
                fixed_width_format(current_time, 6) +  # Transaction time
                fixed_width_format(transaction["company_name"], 40) +  # Company name
                fixed_width_format(transaction["account_no"], 10) +  # accountno
                fixed_width_format(transaction["year"], 6) +  # year
                fixed_width_format(transaction["type"], 1) +  # typecode
                fixed_width_format(transaction["invoice_code"], 18) +  # invoicecode 
                fixed_width_format(transaction["receipt_no"], 20) +  # receiptno
                fixed_width_format("0000", 4) +  # branchNo
                fixed_width_format("0000", 4) +  # tellerNo
                fixed_width_format("CCSH", 4) +  # Transaction type
                fixed_width_format("00000000", 8) +  # Cheque No
                fixed_width_format(transaction["con_amount"], 11) +  # con_amount
                fixed_width_format("00", 2) +  # decimal
                fixed_width_format("000", 3) +  # Cheque bank code
                fixed_width_format("0000", 4) +  # Cheque bank branch
                "\n"
            )
        
        # เขียน Footer
        file.write(
            fixed_width_format("T", 1) +  # Record type: Footer
            fixed_width_format(f"{len(data_list) + 1:06}", 6) +  # Sequence number
            fixed_width_format("8241883047050", 13) +  # Account number
            fixed_width_format("0000000000000000000000000534893", 33) +  # Total amount
            fixed_width_format(f"{len(data_list):07}", 7) +  # Total transactions
            "\n"
        )
    print(f"ไฟล์ '{output_file}' ถูกสร้างแล้ว.")

# อ่านไฟล์ CSV ที่ได้จากการ query
def read_csv_file(file_path):
    data_list = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # จัดข้อมูลแต่ละแถวให้อยู่ในรูปแบบ dictionary ที่จะนำไปใช้เขียนไฟล์
            transaction = {
                "source_id": row["source_id"],
                "company_name": row["company_name"],
                "accountno": row["accountno"],
                "year": row["year"],
                "type": row["type"],
                "invoicecode": row["invoicecode"],
                "receiptno": row["receiptno"],                
                "con_amount": row["amount4"]
            }
            data_list.append(transaction)
    return data_list

# ใช้ไฟล์ CSV ที่ได้จากการ query
csv_file_path = "csv_to_txt.csv"  # เปลี่ยนเป็นชื่อไฟล์ CSV ที่ได้จากการ query
data_list = read_csv_file(csv_file_path)

# เขียนข้อมูลลงไฟล์ txt
write_to_txt(data_list)
