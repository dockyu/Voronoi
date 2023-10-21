import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from voronoi_algorithm import Voronoi
from controller import *


# 按鈕對應的function
def on_run_clicked(ax, canvas, points, voronoi): # run按鈕執行
    run_all(ax, canvas, points, voronoi)

def on_step_by_step_clicked(ax, canvas, points, voronoi): # step by step按鈕執行
    run_next(ax, canvas, points, voronoi)

def on_clear_clicked(ax, canvas, points, voronoi): # clear按鈕執行
    run_exit(voronoi) # 結束計算
    points.clear() # 清除所有點
    canvas_draw_points(ax, canvas, points) # 清除畫布並畫出所有點

def import_input_file():
    print("Imported Input File")

def import_output_file():
    print("Imported Output File")

def export_output_file():
    print("Exported Output File")

def on_canvas_click(event, ax, canvas, points): # 點擊畫布執行
    x, y = int(event.xdata), int(event.ydata)  # 取整數座標
    if x is not None and y is not None:  # 檢查是否點擊在軸（Axes）內
        print(f"Point added: ({x}, {y})")
        points.append((x, y))  # 將點座標加入到 points 列表中
        canvas_draw_points(ax, canvas, points)

def main():
    points = [(10,10),(21,31),(52,72),(153,43),(254,154),(165,365),(96,426),(267,367)]
    points.clear()
    voronoi = Voronoi()
    
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
    run_menu.add_command(label="Run", command=lambda: on_run_clicked(ax, canvas, points, voronoi)) # run按鈕
    run_menu.add_command(label="Step by Step", command=lambda: on_step_by_step_clicked(ax, canvas, points, voronoi)) # step by step按鈕

    clear_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="clear", menu=clear_menu) # clear選單
    clear_menu.add_command(label="Clear", command=lambda: on_clear_clicked(ax, canvas, points, voronoi)) # clear按鈕

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim([0, 600])
    ax.set_ylim([0, 600])

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    # 這裡加入監聽事件來新增點
    canvas.mpl_connect('button_press_event', lambda event, ax=ax, canvas=canvas, points=points: on_canvas_click(event, ax, canvas, points))

    root.mainloop()

if __name__ == '__main__':
    main()  # 或是任何你想執行的函式