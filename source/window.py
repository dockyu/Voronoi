import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

root = tk.Tk()
root.title("Voronoi Diagram")
root.geometry("1200x1000")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="file", menu=file_menu)
file_menu.add_command(label="Import Input File", command=import_input_file)
file_menu.add_command(label="Import Output File", command=import_output_file)
file_menu.add_command(label="Export Output File", command=export_output_file)

run_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="run", menu=run_menu)
run_menu.add_command(label="Run", command=on_run_clicked)
run_menu.add_command(label="Step by Step", command=on_step_by_step_clicked)

# 在建立 run_menu 之後添加
clear_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="clear", menu=clear_menu)
clear_menu.add_command(label="Clear", command=on_clear_clicked)


canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

root.mainloop()
