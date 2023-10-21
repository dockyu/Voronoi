# 功能function
import threading

def run_all(ax, canvas, points, voronoi): # 執行到結束
    voronoi.set_step_by_step(False)
    if voronoi.divide_and_conquer_wait:
        voronoi.trigger()
    else:
        threading.Thread(target=voronoi.divide_and_conquer, args=(ax, canvas, points, points)).start()

def run_next(ax, canvas, points, voronoi): # 執行到下一步
    voronoi.set_step_by_step(True)
    if voronoi.divide_and_conquer_wait:
        voronoi.trigger()
    else:
        threading.Thread(target=voronoi.divide_and_conquer, args=(ax, canvas, points, points)).start()

    
def run_exit(voronoi): # 結束程式
    voronoi.exit()
    voronoi.set_finish(True) # 設置一筆測資已完成


def canvas_draw_points(ax, canvas, points):  # 畫出點
    ax.clear()  # 先清除原先的圖形
    ax.set_xlim([0, 600])  # 設定 x 軸範圍
    ax.set_ylim([0, 600])  # 設定 y 軸範圍

    for x, y in points:  # 畫出所有點
        ax.plot(x, y, marker='o', color='black')  # 畫點
        ax.text(x, y + 5, f"({x}, {y})", fontsize=12, ha='center')  # 在點的上方寫出座標

    canvas.draw()  # 更新畫布
