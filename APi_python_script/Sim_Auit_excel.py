from openpyxl import Workbook

# Your JSON Data
data = [
    {
        "serialNo": "8991102405911161628",
        "reason": "PROBABLE_NOT_REQUESTED_ACTIVATION_FROM_VODAFONE",
        "sentOn": "2025-03-17T15:50:49.488412"
    },
    {
        "serialNo": "8991102405911217875",
        "reason": "PROBABLE_NOT_REQUESTED_ACTIVATION_FROM_VODAFONE",
        "sentOn": "2025-03-17T15:50:49.488412"
    },
    {
        "serialNo": "8991102205732345487",
        "reason": "DEVICE_IN_DEAD_STATE",
        "sentOn": "2025-05-07T05:23:28.859774"
    },
    {
        "serialNo": "8991102406350828545",
        "reason": "DEVICE_IN_DEAD_STATE",
        "sentOn": "2025-06-24T17:05:34.701767"
    }
]

# Create Workbook
wb = Workbook()
ws = wb.active
ws.title = "SIM Data"

# Write Header
headers = ["Serial No", "Reason", "Sent On"]
ws.append(headers)

# Write Data Rows
for item in data:
    ws.append([
        item["serialNo"],
        item["reason"],
        item["sentOn"]
    ])

# Save File
file_name = "sim_report.xlsx"
wb.save(file_name)

print(f"Excel file '{file_name}' created successfully!")
