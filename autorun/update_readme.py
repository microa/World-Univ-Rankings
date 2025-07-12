import gspread
import os

# --- 配置 ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zEXZ0IkwySOkKju9IctvcH8JuJ1qCa-o2t2wBs3ss0U/edit#gid=0"
WORKSHEET_NAME = "Rankings"
# 工作流会从 GitHub Secret 创建这个文件
SERVICE_ACCOUNT_FILE = "service_account.json" 

# --- 授权 (更现代、更简单的方式) ---
print("🚀 正在授权 Google Sheets...")
try:
    # 使用 gspread 内置的服务账户授权方法
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    print("✅ 授权成功！")
except FileNotFoundError:
    print(f"❌ 错误: 找不到凭证文件 '{SERVICE_ACCOUNT_FILE}'。请检查 GitHub Actions 工作流是否正确创建了该文件。")
    exit(1)
except Exception as e:
    print(f"❌ 授权时发生未知错误: {e}")
    exit(1)

# --- 获取数据 ---
print(f"📊 正在从工作表 '{WORKSHEET_NAME}' 获取数据...")
try:
    spreadsheet = gc.open_by_url(SHEET_URL)
    sheet = spreadsheet.worksheet(WORKSHEET_NAME)
    data = sheet.get_all_values()
    print(f"✅ 成功获取 {len(data)} 行数据。")
except gspread.exceptions.SpreadsheetNotFound:
    print(f"❌ 错误: 找不到电子表格。")
    print("   请确认:")
    print(f"   1. Google Sheet URL 是否正确: {SHEET_URL}")
    print(f"   2. 是否已将服务账户邮箱共享给该表格并授予“编辑者”权限。")
    exit(1)
except gspread.exceptions.WorksheetNotFound:
    print(f"❌ 错误: 在电子表格中找不到名为 '{WORKSHEET_NAME}' 的工作表。")
    exit(1)
except Exception as e:
    print(f"❌ 获取数据时发生未知错误: {e}")
    exit(1)

# --- 转为 Markdown 表格 ---
print("📝 正在生成 Markdown 内容...")
lines = ["# 📊 Google Sheet 自动同步\n"]
if data:
    header = "| " + " | ".join(data[0]) + " |"
    divider = "| " + " | ".join(["---"] * len(data[0])) + " |"
    lines.append(header)
    lines.append(divider)
    for row in data[1:]:
        # 确保所有单元格内容都是字符串，避免 join 出错
        str_row = [str(cell) for cell in row]
        lines.append("| " + " | ".join(str_row) + " |")
else:
    lines.append("No data found.")

# --- 写入 README.md ---
try:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("✅ README.md 已成功更新！")
except Exception as e:
    print(f"❌ 写入 README.md 时发生错误: {e}")
    exit(1)
