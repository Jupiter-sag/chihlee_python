import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from pathlib import Path
import os

class ScoreDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("分數分佈分析系統")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # 設定中文字體
        self.setup_chinese_font()
        
        # 設定風格
        self.setup_style()
        
        # 資料
        self.df = None
        self.subjects = []
        
        # 建立主介面
        self.create_widgets()
    
    def setup_chinese_font(self):
        """設定中文字體以支援中文顯示"""
        # 嘗試多個中文字體
        font_paths = [
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/SimHei.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        ]
        
        for font_path in font_paths:
            if Path(font_path).exists():
                try:
                    self.chinese_font = FontProperties(fname=font_path)
                    plt.rcParams['font.sans-serif'] = ['STHeiti Medium']
                    plt.rcParams['axes.unicode_minus'] = False
                    return
                except:
                    continue
        
        # 如果找不到中文字體，使用預設
        self.chinese_font = FontProperties()
        
    def setup_style(self):
        """設定視覺風格"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 定義顏色
        self.bg_color = "#f0f0f0"
        self.btn_bg = "#4CAF50"
        self.btn_fg = "white"
        self.header_bg = "#2c3e50"
        self.header_fg = "white"
        
    def create_widgets(self):
        """建立主要控制項"""
        
        # 頂部面板：檔案操作
        top_frame = tk.Frame(self.root, bg=self.header_bg, height=80)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        top_frame.pack_propagate(False)
        
        # 標題
        title_label = tk.Label(
            top_frame, 
            text="📊 分數分佈分析系統",
            font=("Arial", 18, "bold"),
            bg=self.header_bg,
            fg=self.header_fg
        )
        title_label.pack(pady=10)
        
        # 按鈕框架
        button_frame = tk.Frame(top_frame, bg=self.header_bg)
        button_frame.pack(pady=5)
        
        # 打開檔案按鈕
        open_btn = tk.Button(
            button_frame,
            text="📁 打開分數檔案",
            command=self.open_file,
            bg=self.btn_bg,
            fg=self.btn_fg,
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        open_btn.pack(side=tk.LEFT, padx=10)
        
        # 預設檔案按鈕
        default_btn = tk.Button(
            button_frame,
            text="📄 使用預設檔案",
            command=self.load_default_file,
            bg="#2196F3",
            fg=self.btn_fg,
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        default_btn.pack(side=tk.LEFT, padx=10)
        
        # 檔案路徑顯示
        self.file_label = tk.Label(
            button_frame,
            text="未載入檔案",
            font=("Arial", 10),
            bg=self.header_bg,
            fg="#ffeb3b"
        )
        self.file_label.pack(side=tk.LEFT, padx=20)
        
        # 主內容框架
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左側：統計信息
        left_frame = tk.Frame(main_frame, bg="white", relief=tk.SUNKEN, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        # 統計標題
        stat_title = tk.Label(
            left_frame,
            text="📈 統計信息",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.header_bg
        )
        stat_title.pack(pady=10)
        
        # 統計內容框
        self.stat_frame = tk.Frame(left_frame, bg="white")
        self.stat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 右側：圖表
        right_frame = tk.Frame(main_frame, bg="white", relief=tk.SUNKEN, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 圖表標題
        chart_title = tk.Label(
            right_frame,
            text="📊 分數分佈圖表",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.header_bg
        )
        chart_title.pack(pady=10)
        
        # 科目選擇下拉菜單
        subject_frame = tk.Frame(right_frame, bg="white")
        subject_frame.pack(padx=10, pady=5)
        
        tk.Label(subject_frame, text="選擇科目：", font=("Arial", 10), bg="white").pack(side=tk.LEFT)
        
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(
            subject_frame,
            textvariable=self.subject_var,
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        self.subject_combo.pack(side=tk.LEFT, padx=10)
        self.subject_combo.bind("<<ComboboxSelected>>", lambda e: self.update_chart())
        
        # 圖表容器
        self.canvas_frame = tk.Frame(right_frame, bg="white")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def open_file(self):
        """打開檔案對話框"""
        file_path = filedialog.askopenfilename(
            title="選擇分數檔案",
            filetypes=[("CSV 檔案", "*.csv"), ("所有檔案", "*.*")],
            initialdir=str(Path.home())
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_default_file(self):
        """載入預設檔案"""
        default_path = Path(__file__).parent / "考試分數_3年6班.csv"
        if default_path.exists():
            self.load_file(str(default_path))
        else:
            messagebox.showerror("錯誤", "找不到預設檔案：考試分數_3年6班.csv")
    
    def load_file(self, file_path):
        """載入 CSV 檔案"""
        try:
            # 嘗試多種編碼
            for encoding in ["utf-8", "cp950", "big5"]:
                try:
                    self.df = pd.read_csv(file_path, encoding=encoding)
                    break
                except:
                    continue
            
            if self.df is None:
                messagebox.showerror("錯誤", "無法讀取檔案")
                return
            
            # 更新檔案標籤
            self.file_label.config(text=f"✓ {Path(file_path).name}")
            
            # 取得科目列表（排除非數值列）
            self.subjects = [col for col in self.df.columns if col != "學生姓名" and pd.api.types.is_numeric_dtype(self.df[col])]
            
            # 更新下拉菜單
            self.subject_combo["values"] = self.subjects
            if self.subjects:
                self.subject_combo.set(self.subjects[0])
                self.update_statistics()
                self.update_chart()
            
        except Exception as e:
            messagebox.showerror("錯誤", f"載入檔案失敗：{str(e)}")
    
    def update_statistics(self):
        """更新統計信息"""
        if self.df is None or not self.subjects:
            return
        
        # 清除舊內容
        for widget in self.stat_frame.winfo_children():
            widget.destroy()
        
        # 為每個科目顯示統計
        for subject in self.subjects:
            scores = self.df[subject]
            
            # 科目標題
            subject_label = tk.Label(
                self.stat_frame,
                text=f"\n🔹 {subject}",
                font=("Arial", 11, "bold"),
                bg="white",
                fg=self.header_bg
            )
            subject_label.pack(anchor=tk.W, padx=5, pady=(10, 5))
            
            # 統計數據
            stats_text = f"""
平均分：{scores.mean():.2f}
最高分：{scores.max():.0f}
最低分：{scores.min():.0f}
標準差：{scores.std():.2f}
中位數：{scores.median():.2f}
"""
            stats_info = tk.Label(
                self.stat_frame,
                text=stats_text.strip(),
                font=("Arial", 9),
                bg="white",
                fg="#333333",
                justify=tk.LEFT
            )
            stats_info.pack(anchor=tk.W, padx=15)
    
    def update_chart(self):
        """更新圖表"""
        if self.df is None or not self.subject_var.get():
            return
        
        # 清除舊圖表
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        subject = self.subject_var.get()
        scores = self.df[subject]
        
        # 建立圖表
        fig = Figure(figsize=(6, 5), dpi=80, facecolor="white")
        ax = fig.add_subplot(111)
        
        # 繪製直方圖
        n, bins, patches = ax.hist(scores, bins=10, color="#4CAF50", edgecolor="black", alpha=0.7)
        
        # 繪製平均線
        mean_val = scores.mean()
        ax.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"平均：{mean_val:.2f}")
        
        # 設定標籤和標題（使用中文字體）
        ax.set_xlabel("分數", fontproperties=self.chinese_font, fontsize=11)
        ax.set_ylabel("人數", fontproperties=self.chinese_font, fontsize=11)
        ax.set_title(f"{subject} 分數分佈", fontproperties=self.chinese_font, fontsize=13, fontweight="bold")
        ax.legend(fontsize=10, prop=self.chinese_font)
        ax.grid(axis="y", alpha=0.3)
        
        # 嵌入 tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = ScoreDistributionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
