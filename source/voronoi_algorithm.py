import threading
from controller import canvas_draw_points

class ExitCommand(Exception):
    pass

class Voronoi:
    def __init__(self):
        self.condition = threading.Condition()
        self.step_by_step = False # 代表是否要一步一步執行
        self.divide_and_conquer_wait = False # 代表 divide_and_conquer 函式是否已被執行且正在等待
        self.exit_flag = False # 代表是否要結束程式

    def divide_and_conquer(self, ax, canvas, S, points): 
        # 用來建立thread
        # 用來找出集合S的Voronoi diagram

        if len(S) <= 1: # 如果集合S只有一個點，可以直接做出Voronoi diagram
            V = False
            pass
        else: # 如果集合S有兩個以上的點，則要先分割集合S
            SL, SR = self.devide(S) # 分割集合S為SL和SR
            VL = self.divide_and_conquer(ax, canvas, SL, points) # 找出SL的Voronoi diagram
            VR = self.divide_and_conquer(ax, canvas, SR, points) # 找出SR的Voronoi diagram

            V = self.merge(VL, VR) # 合併VL和VR，得出V也就是S的Voronoi diagram

            self.draw_Voronoi_diagram(ax, canvas, V, S, points) # 畫出Voronoi diagram

            if self.step_by_step:
                with self.condition:
                    if self.exit_flag: # wait前檢查是否要結束程式(exit() 被觸發)
                        raise ExitCommand() 
                    self.divide_and_conquer_wait = True
                    self.condition.wait()
                    self.divide_and_conquer_wait = False
                    if self.exit_flag: # 被喚醒後檢查是否要結束程式(exit() 被觸發)
                        raise ExitCommand() 
            

        return V

    def merge(self, VL, VR): # 合併VL和VR，得出V也就是S的Voronoi diagram
        pass

    def draw_Voronoi_diagram(self, ax, canvas, V, S, points): # 畫出Voronoi diagram
        canvas_draw_points(ax, canvas, points) # 清除畫布並畫出所有點
        print(f"數量 of S: {len(S)}")
        print(f"S 的座標: {S}")
        pass

    def trigger(self):
        with self.condition:
            self.condition.notify()
    
    def exit(self):
        with self.condition:
            self.exit_flag = True
            self.condition.notify_all()  # 喚醒所有等待的線程

    def devide(self, S):
        mid = len(S) // 2
        return S[:mid], S[mid:]

    def set_step_by_step(self, value): # 設置 step_by_step 屬性
        with self.condition:
            self.step_by_step = value

    def set_divide_and_conquer_wait(self, value): # 設置 divide_and_conquer_wait 屬性
        with self.condition:
            self.divide_and_conquer_wait = value