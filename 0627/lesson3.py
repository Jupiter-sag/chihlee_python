import os
import pandas as pd
import tkinter as tk
from tkinter import ttk

# ============================================================
# 1. 資料處理
# ============================================================

# 取得目前程式所在目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '各鄉鎮市區人口密度.csv')

# 讀取 CSV 檔案，第一列作為欄位名稱（header=0 為 pandas 預設行為）
df = pd.read_csv(CSV_PATH, header=0)

# 將英文欄位名稱重新命名為中文
df.rename(columns={
    'site_id': '區域別',
    'people_total': '人口數',
    'area': '土地面積'
}, inplace=True)

# 僅保留需要的三個欄位
df = df[['區域別', '人口數', '土地面積']]

# 移除第二列（中文標題列：'統計年,區域別,年底人口數,土地面積,人口密度'）
df = df[df['區域別'] != '區域別']

# 移除最後 5 列尾部說明資訊
df = df[:-5]

# 將人口數與土地面積轉換為數值型態，無法轉換者設為 NaN
df['人口數'] = pd.to_numeric(df['人口數'], errors='coerce')
df['土地面積'] = pd.to_numeric(df['土地面積'], errors='coerce')

# 移除含有空值（NaN）的列
df = df.dropna()

# 新增人口密度欄位（四捨五入至小數點後兩位）
df['人口密度'] = (df['人口數'] / df['土地面積']).round(2)

# 人口數顯示為整數
df['人口數'] = df['人口數'].astype(int)

# ============================================================
# 2. GUI 介面
# ============================================================

class PopulationQuerySystem:
    """台灣鄉鎮市區人口密度查詢系統"""

    def __init__(self, data):
        """初始化視窗與元件"""
        self.data = data
        self.window = tk.Tk()
        self.window.title('台灣鄉鎮市區人口密度查詢系統')
        self.window.geometry('900x600')

        # --- 上方控制區 ---
        control_frame = ttk.Frame(self.window, padding=10)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text='輸入區域名稱：').pack(side=tk.LEFT)
        self.keyword_entry = ttk.Entry(control_frame, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)
        self.keyword_entry.bind('<Return>', lambda e: self.filter_data())

        ttk.Button(control_frame, text='查詢', command=self.filter_data).pack(side=tk.LEFT, padx=5)

        # --- 下方表格區 ---
        table_frame = ttk.Frame(self.window, padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('區域別', '人口數', '土地面積', '人口密度')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)

        # 設定各欄位標題、寬度與置中對齊
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, width=180, anchor=tk.CENTER)

        # 加入垂直與水平捲軸
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # 程式啟動時顯示所有資料
        self.update_table(self.data)

    def filter_data(self):
        """依關鍵字篩選資料並更新表格"""
        keyword = self.keyword_entry.get().strip()
        if keyword:
            filtered = self.data[self.data['區域別'].str.contains(keyword)]
        else:
            filtered = self.data
        self.update_table(filtered)

    def update_table(self, data):
        """清除表格並重新填入指定資料"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in data.iterrows():
            self.tree.insert('', tk.END, values=(
                row['區域別'],
                row['人口數'],
                row['土地面積'],
                row['人口密度']
            ))

    def run(self):
        """啟動主視窗"""
        self.window.mainloop()

# ============================================================
# 3. 啟動程式
# ============================================================

if __name__ == '__main__':
    app = PopulationQuerySystem(df)
    app.run()
