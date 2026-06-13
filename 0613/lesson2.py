import pandas as pd
import requests
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    REPORTLAB_AVAILABLE = True
    
    # 註冊中文字體（macOS 系統字體）
    try:
        # 嘗試使用 macOS 系統中文字體
        font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
        pdfmetrics.registerFont(TTFont("STHeiti", font_path))
        CHINESE_FONT = "STHeiti"
    except:
        try:
            # 備用方案：使用其他 macOS 中文字體
            font_path = "/Library/Fonts/Microsoft YaHei.ttf"
            pdfmetrics.registerFont(TTFont("MSYaHei", font_path))
            CHINESE_FONT = "MSYaHei"
        except:
            CHINESE_FONT = "Helvetica"
            
except ImportError:
    REPORTLAB_AVAILABLE = False


def export_pdf(df: pd.DataFrame, filename: str = "YouBike_Live_Report.pdf", max_rows: int = 30):
    """Export the DataFrame to a simple PDF file using reportlab with Chinese font support."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # 建立支援中文的標題樣式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=CHINESE_FONT,
        fontSize=16,
        textColor=colors.HexColor('#000000')
    )
    
    elements = [Paragraph("YouBike 2.0 即時資料報表", title_style), Spacer(1, 12)]

    rows = [list(df.columns)] + df.head(max_rows).astype(str).values.tolist()
    table = Table(rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), CHINESE_FONT),
                ("FONTNAME", (0, 1), (-1, -1), CHINESE_FONT),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    elements.append(table)
    doc.build(elements)


def main():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    print("正在獲取 YouBike 2.0 即時資料...")
    response = requests.get(url)
    response.raise_for_status()

    # 將 JSON 轉為 Pandas DataFrame 表格
    df = pd.DataFrame(response.json())

    # 1. 定義中文欄位映射表
    rename_dict = {
        "sarea": "行政區",
        "sna": "站點名稱",
        "available_rent_bikes": "可借車輛",
        "available_return_bikes": "可還空位",
        "Quantity": "總車位數",
        "act": "營運狀態",
        "ar": "地址",
        "mday": "更新時間",
    }

    # 只取目前 API 回傳的欄位，避免因欄位變動而出錯
    available_columns = [col for col in rename_dict.keys() if col in df.columns]
    df_table = df[available_columns].rename(columns={k: rename_dict[k] for k in available_columns})

    # 2. 資料清洗：精簡站點名稱、將狀態碼轉為文字
    df_table["站點名稱"] = df_table["站點名稱"].str.replace("YouBike2.0_", "")
    df_table["營運狀態"] = df_table["營運狀態"].apply(
        lambda x: "正常營運" if str(x) == "1" else "暫停營運"
    )

    # 3. 轉換型態確保數字計算正確
    df_table["可借車輛"] = pd.to_numeric(df_table["可借車輛"])
    df_table["可還空位"] = pd.to_numeric(df_table["可還空位"])
    df_table["總車位數"] = pd.to_numeric(df_table["總車位數"])

    # 4. 格式化時間（讓日期更好讀）
    # API 時間格式通常為 20260606143000 -> 轉為常用格式
    df_table["更新時間"] = pd.to_datetime(
        df_table["更新時間"], format="%Y%m%d%H%M%S", errors="coerce"
    )

    # 印出前 5 筆在終端機檢查表格
    print("\n--- 資料表預覽 ---")
    print(df_table.head().to_string(index=False))

    # 5. 匯出為 Excel 檔案，若 openpyxl 不可用則改寫 CSV
    output_filename = "YouBike_Live_Report.xlsx"
    try:
        df_table.to_excel(output_filename, index=False)
        print(f"\n成功！表格已儲存至: {output_filename}")
    except ModuleNotFoundError as e:
        if "openpyxl" in str(e):
            fallback_filename = "YouBike_Live_Report.csv"
            df_table.to_csv(fallback_filename, index=False, encoding="utf-8-sig")
            print(f"\n警告：未安裝 openpyxl，已改為儲存 CSV：{fallback_filename}")
        else:
            raise

    # 6. 匯出為 PDF 檔案（需安裝 reportlab）
    if REPORTLAB_AVAILABLE:
        pdf_filename = "YouBike_Live_Report.pdf"
        export_pdf(df_table, pdf_filename)
        print(f"成功！PDF 已儲存至: {pdf_filename}")
    else:
        print("若要匯出 PDF，請先安裝 reportlab：")
        print("  /Users/sophiewang/Documents/GitHub/chihlee_python/.venv/bin/python3 -m pip install reportlab")


if __name__ == "__main__":
    main()
