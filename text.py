import csv

# ฟังก์ชันเพื่อจัดรูปแบบข้อมูลให้มีความยาวคงที่
def fixed_width_format(data, width, align_left=True):
    if align_left:
        return str(data).ljust(width)
    else:
        return str(data).rjust(width)

# ฟังก์ชันในการเขียนไฟล์จากข้อมูลใน CSV
def write_to_txt(data_list, output_file="output.txt"):
    with open(output_file, "w", encoding="utf-8") as file:
        # เขียน Header
        file.write(
            fixed_width_format("H", 1) +  # Record type: Header
            fixed_width_format("000001", 6) +  # Sequence number
            fixed_width_format("8241883047050", 13) +  # Account number
            fixed_width_format("SOCIAL SECURITY OFFICE [8D]", 40) +  # Company name
            fixed_width_format("25092024", 8) +  # Transaction date
            fixed_width_format("11000000", 8) +  # Time
            "\n"
        )
        
        # เขียน Transactions จากข้อมูลใน CSV
        for idx, transaction in enumerate(data_list, start=2):
            file.write(
                fixed_width_format("D", 1) +  # Record type: Detail
                fixed_width_format(f"{idx:06}", 6) +  # Sequence number
                fixed_width_format(transaction["account_number"], 13) +  # Account number
                fixed_width_format(transaction["transaction_date"], 8) +  # Transaction date
                fixed_width_format(transaction["transaction_time"], 6) +  # Transaction time
                fixed_width_format(transaction["company_name"], 40) +  # Company name
                fixed_width_format(transaction["amount1"], 17) +  # Amount1
                fixed_width_format(transaction["amount2"], 18) +  # Amount2
                fixed_width_format(transaction["amount3"], 9) +  # Amount3
                fixed_width_format(transaction["code"], 11) +  # Code
                fixed_width_format(transaction["flag"], 8) +  # Flag
                fixed_width_format(transaction["transaction_type"], 4) +  # Transaction type
                fixed_width_format(transaction["amount4"], 18) +  # Amount4
                fixed_width_format(transaction["amount5"], 13) +  # Amount5
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
                "account_number": row["account_number"],
                "transaction_date": row["transaction_date"],
                "transaction_time": row["transaction_time"],
                "company_name": row["company_name"],
                "amount1": row["amount1"],
                "amount2": row["amount2"],
                "amount3": row["amount3"],
                "code": row["code"],
                "flag": row["flag"],
                "transaction_type": row["transaction_type"],
                "amount4": row["amount4"],
                "amount5": row["amount5"]
            }
            data_list.append(transaction)
    return data_list

# ใช้ไฟล์ CSV ที่ได้จากการ query
csv_file_path = "query_data.csv"  # เปลี่ยนเป็นชื่อไฟล์ CSV ที่ได้จากการ query
data_list = read_csv_file(csv_file_path)

# เขียนข้อมูลลงไฟล์ txt
write_to_txt(data_list)
