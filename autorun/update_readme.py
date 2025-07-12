import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 配置
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zEXZ0IkwySOkKju9IctvcH8JuJ1qCa-o2t2wBs3ss0U/edit#gid=0"
WORKSHEET = "Rankings"
CREDS_FILE = "service_account.json"

# 授权
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
client = gspread.authorize(creds)

# 获取数据
spreadsheet = client.open_by_url(SHEET_URL)
sheet = spreadsheet.worksheet(WORKSHEET)
data = sheet.get_all_values()

# 转 Markdown 表格
lines = ["# 📊 Google Sheet 自动同步\n"]
if data:
    header = "| " + " | ".join(data[0]) + " |"
    divider = "| " + " | ".join(["---"] * len(data[0])) + " |"
    lines.append(header)
    lines.append(divider)
    for row in data[1:]:
        lines.append("| " + " | ".join(row) + " |")
else:
    lines.append("No data found.")

# 写入 README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("✅ README.md 已更新！")
