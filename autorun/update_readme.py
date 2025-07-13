import gspread
import os

# --- 1. 在这里自定义你的内容和格式 ---

# README 标题
README_TITLE = "# 🌏 世界大学排名「均值榜」自动更新"

# 在表格前显示的自定义文字。
# 你可以在 """ 和 """之间使用多行文字，也支持 Markdown 语法（如 **加粗**、*斜体* 等）。
CUSTOM_TEXT_BEFORE_TABLE = """
大家好！欢迎来到世界大学排名「均值榜」榜单自动更新版。  
众所周知，大学排行榜是一项争议不断、充满政治色彩以及商业味重的工作。  
那我们今天就将各方力量揉和在一起，提出一个「均值榜」供大家参考。  

这个榜单的数据来源于四大综合榜榜单，它们分别是：  
QS World University Rankings  
The Times Higher Education World University Rankings  
The Academic Ranking of World Universities (ARWU)  
U.S. News Best Global Universities Rankings  

如果对您有用，麻烦狂击右上角 **☆Star** 收藏  
被跟踪的学校会每日自动更新，确保您随时可以获取到最新、最准确的排名信息，如果您有想跟踪的学校，请发邮件至: bh.huang@ieee.org, 我们将为您即时添加。  

可视化（Visualization）：  
即将更新，并且持续升级和优化中……    
  
技术细节（Tech Report）：  
即将更新，并且持续升级和优化中……  
"""

# 设置表格每列的对齐方式。
COLUMN_ALIGNMENTS = ['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'] 

# --- 内部配置---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zEXZ0IkwySOkKju9IctvcH8JuJ1qCa-o2t2wBs3ss0U/edit#gid=0"
WORKSHEET_NAME = "Rankings"
SERVICE_ACCOUNT_FILE = "service_account.json" 

# --- 2. 核心脚本逻辑 ---

def get_alignment_divider(num_columns, alignments):
    """根据配置生成 Markdown 表格的对齐分割线"""
    dividers = []
    default_alignment = 'left'
    for i in range(num_columns):
        # 如果 alignments 列表不够长，就使用默认对齐
        align = alignments[i] if i < len(alignments) else default_alignment
        if align == 'center':
            dividers.append(':---:')
        elif align == 'right':
            dividers.append('---:')
        else: # 'left'
            dividers.append('---')
    return "| " + " | ".join(dividers) + " |"

# 授权
print("🚀 正在授权 Google Sheets...")
try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    print("✅ 授权成功！")
except Exception as e:
    print(f"❌ 授权时发生错误: {e}")
    exit(1)

# 获取数据
print(f"📊 正在从工作表 '{WORKSHEET_NAME}' 获取数据...")
try:
    spreadsheet = gc.open_by_url(SHEET_URL)
    sheet = spreadsheet.worksheet(WORKSHEET_NAME)
    data = sheet.get_all_values()
    print(f"✅ 成功获取 {len(data)} 行数据。")
except gspread.exceptions.SpreadsheetNotFound:
    print(f"❌ 错误: 找不到电子表格。请检查 URL 和共享权限。")
    exit(1)
except gspread.exceptions.WorksheetNotFound:
    print(f"❌ 错误: 在电子表格中找不到名为 '{WORKSHEET_NAME}' 的工作表。")
    exit(1)
except Exception as e:
    print(f"❌ 获取数据时发生错误: {e}")
    exit(1)

# 生成 Markdown 内容
print("📝 正在生成 Markdown 内容...")
lines = []

# 添加自定义标题和文字
if README_TITLE:
    lines.append(README_TITLE)
if CUSTOM_TEXT_BEFORE_TABLE:
    lines.append(CUSTOM_TEXT_BEFORE_TABLE.strip())

# 仅在有数据时才添加表格
if data:
    # 添加一个空行以分隔文字和表格
    lines.append("") 
    
    num_columns = len(data[0])
    header = "| " + " | ".join(data[0]) + " |"
    divider = get_alignment_divider(num_columns, COLUMN_ALIGNMENTS)
    
    lines.append(header)
    lines.append(divider)
    
    for row in data[1:]:
        str_row = [str(cell) for cell in row]
        lines.append("| " + " | ".join(str_row) + " |")
else:
    lines.append("\n没有在表格中找到数据。")

# 写入 README.md
print("✍️ 正在写入 README.md...")
try:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("🎉 README.md 已成功更新！")
except Exception as e:
    print(f"❌ 写入 README.md 时发生错误: {e}")
    exit(1)
