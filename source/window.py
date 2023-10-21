import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from voronoi_algorithm import Voronoi
from controller import *


# 按鈕對應的function
def on_run_clicked(ax, canvas, test_data, voronoi): # run按鈕執行
    if voronoi.finish: # 如果上一個測資已做完，刪除上一個測資
        test_data.pop(0)
    if not test_data: # 如果沒有測資，則不執行
        return
    points=test_data[0] # 取得測資
    run_all(ax, canvas, points, voronoi) # 執行到結束

def on_step_by_step_clicked(ax, canvas, test_data, voronoi): # step by step按鈕執行
    if voronoi.finish: # 如果上一個測資已做完，刪除上一個測資
        test_data.pop(0)
    points=test_data[0]
    run_next(ax, canvas, points, voronoi) # 如果是新的側資，則開始執行到下一步，否則繼續執行到下一步

def on_clear_clicked(ax, canvas, test_data, voronoi): # clear按鈕執行
    run_exit(voronoi) # 結束計算，並設定成結束一筆測資
    points=[]
    canvas_draw_points(ax, canvas, points) # 清除畫布並畫出0個點

def import_input_file(ax, canvas, test_data, voronoi):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filename:  # 使用者取消了選擇
        return
    with open(filename, 'r') as file:
        test_data.clear()
        while True:
            num_points = file.readline().strip()
            if not num_points:  # 檢查是否到達檔案末尾
                break
            if num_points == '0':  # 如果遇到 0，代表測試結束
                break
            num_points = int(num_points)
            point_list = []
            for _ in range(num_points):
                x, y = map(int, file.readline().strip().split())
                point_list.append((x, y))
            test_data.append(point_list)
    canvas_draw_points(ax, canvas, test_data[0])  # 更新畫布

def import_output_file():
    print("Imported Output File")

def export_output_file():
    print("Exported Output File")

def on_canvas_click(event, ax, canvas, test_data, voronoi): # 點擊畫布執行
    if voronoi.finish: # 如果上一個測資已做完，刪除上一個測資
        test_data.pop(0)
        voronoi.set_finish(False) # 設置程式未完成
    x, y = int(event.xdata), int(event.ydata)  # 取整數座標
    if x is not None and y is not None:  # 檢查是否點擊在軸（Axes）內
        print(f"Point added: ({x}, {y})")
        if len(test_data) > 0:  # 檢查 test_data 是否為空
            test_data[0].append((x, y))  # 將點座標加入到第一筆測試資料中
        else:
            test_data.append([(x, y)])  # 如果 test_data 是空的，創建新的測試資料
        canvas_draw_points(ax, canvas, test_data[0])  # 更新畫布

def main():
    test_data = []  # 清空目前的資料
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
    file_menu.add_command(label="Import Input File", command=lambda: import_input_file(ax, canvas, test_data, voronoi)) # import input file按鈕
    file_menu.add_command(label="Import Output File", command=lambda: import_output_file) # import output file按鈕
    file_menu.add_command(label="Export Output File", command=lambda: export_output_file) # export output file按鈕

    run_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="run", menu=run_menu) # run選單
    run_menu.add_command(label="Run", command=lambda: on_run_clicked(ax, canvas, test_data, voronoi)) # run按鈕
    run_menu.add_command(label="Step by Step", command=lambda: on_step_by_step_clicked(ax, canvas, test_data, voronoi)) # step by step按鈕

    clear_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="clear", menu=clear_menu) # clear選單
    clear_menu.add_command(label="Clear", command=lambda: on_clear_clicked(ax, canvas, test_data, voronoi)) # clear按鈕

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim([0, 600])
    ax.set_ylim([0, 600])

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    # 這裡加入監聽事件來新增點
    canvas.mpl_connect('button_press_event', lambda event, ax=ax, canvas=canvas, test_data=test_data: on_canvas_click(event, ax, canvas, test_data, voronoi))

    root.mainloop()

if __name__ == '__main__':
    main()  # 或是任何你想執行的函式