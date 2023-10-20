import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# 按鈕對應的function
def on_run_clicked():
    print("Run button clicked")

def on_step_by_step_clicked():
    print("Step by Step button clicked")

def on_clear_clicked():
    ax.clear()  # 清除 matplotlib 畫布
    canvas.draw()  # 重新繪制畫布

def import_input_file():
    print("Imported Input File")

def import_output_file():
    print("Imported Output File")

def export_output_file():
    print("Exported Output File")

# 測試按鈕對應的function
def on_test_clicked():
    print("Test button clicked")
    draw_test()

# 功能function
def draw_test():
    ax.clear()  # 先清除原先的圖形
    ax.set_xlim([0, 600])  # 設定 x 軸範圍
    ax.set_ylim([0, 600])  # 設定 y 軸範圍

    # 畫出三個點：(5, 20), (150, 300), 和 (500, 260)
    x_values = [5, 150, 500]
    y_values = [20, 300, 260]
    ax.scatter(x_values, y_values, color='red')

    # 更新畫布
    canvas.draw()

# 建立視窗
root = tk.Tk()
root.title("Voronoi Diagram")
root.geometry("1200x1000")

# 建立工作列
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 建立工作列的選單
file_menu = tk.Menu(menu_bar, tearoff=0) # tearoff=0表示選單不能被拖出來
menu_bar.add_cascade(label="file", menu=file_menu) # file選單
file_menu.add_command(label="Import Input File", command=import_input_file) # import input file按鈕
file_menu.add_command(label="Import Output File", command=import_output_file) # import output file按鈕
file_menu.add_command(label="Export Output File", command=export_output_file) # export output file按鈕

run_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="run", menu=run_menu) # run選單
run_menu.add_command(label="Run", command=on_run_clicked) # run按鈕
run_menu.add_command(label="Step by Step", command=on_step_by_step_clicked) # step by step按鈕

clear_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="clear", menu=clear_menu) # clear選單
clear_menu.add_command(label="Clear", command=on_clear_clicked) # clear按鈕

# 測試按鈕
clear_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="test", menu=clear_menu) # clear選單
clear_menu.add_command(label="draw test", command=on_test_clicked) # clear按鈕

canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim([0, 600])  # 設定 x 軸範圍
ax.set_ylim([0, 600])  # 設定 y 軸範圍

canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

root.mainloop()
