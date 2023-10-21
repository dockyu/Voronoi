import threading
from controller import canvas_draw_points
from data_structure import Point, Edge, Polygon, VoronoiDiagram
class ExitCommand(Exception):
    pass

class Voronoi:
    def __init__(self):
        self.condition = threading.Condition()
        self.step_by_step = False # 代表是否要一步一步執行
        self.divide_and_conquer_wait = False # 代表 divide_and_conquer 函式是否已被執行且正在等待
        self.exit_flag = False # 代表是否要結束程式
        self.finish = False # 代表是否執行完畢

    def divide_and_conquer(self, ax, canvas, S, points, level=0): 
        # 用來建立thread
        # 用來找出集合S的Voronoi diagram
        if self.exit_flag and level == 0: # 如果要結束程式，則結束程式
            self.set_exit_flag(False)
            return
        if self.exit_flag: # 如果要結束程式，則結束程式
            return

        self.set_finish(False) # 設置程式未完成

        if len(S) <= 1: # 如果集合S只有一個點，可以直接做出Voronoi diagram
            point = S[0]
            x = point[0]
            y = point[1]
            V = self.create_single_point_voronoi(x, y)


        else: # 如果集合S有兩個以上的點，則要先分割集合S
            SL, SR = self.devide(S) # 分割集合S為SL和SR
            VL = self.divide_and_conquer(ax, canvas, SL, points, level+1) # 找出SL的Voronoi diagram
            VR = self.divide_and_conquer(ax, canvas, SR, points, level+1) # 找出SR的Voronoi diagram
            if self.exit_flag: # 如果要結束程式，則結束程式
                return
            V = self.merge(VL, VR) # 合併VL和VR，得出V也就是S的Voronoi diagram

            self.draw_Voronoi_diagram(ax, canvas, V, S, points) # 畫出Voronoi diagram

            if self.step_by_step:
                with self.condition:
                    # if self.exit_flag: # wait前檢查是否要結束程式(exit() 被觸發)
                    #     self.exit = True
                    #     raise ExitCommand() 
                    self.divide_and_conquer_wait = True
                    self.condition.wait()
                    self.divide_and_conquer_wait = False
            if level == 0:
                self.set_finish(True) # 設置程式已完成

        return V
    
    def create_single_point_voronoi(self, x, y):
        point = Point(x, y)
        polygon = Polygon(center=point)  # 設定多邊形的「中心點」
        voronoi = VoronoiDiagram()
        voronoi.add_polygon(polygon)
        return voronoi

    def merge(self, VL, VR): # 合併VL和VR，得出V也就是S的Voronoi diagram
        # 初始化結果的VoronoiDiagram
        V = VoronoiDiagram()

        # 測試用
        for polygon in VL.polygons:
            V.add_polygon(polygon)
        for polygon in VR.polygons:
            V.add_polygon(polygon)

        # STEP 1: 找出VL和VR的切線（這個部分需要你根據具體算法來實現）
        # upper_tangent, lower_tangent = find_tangents(VL, VR)

        # STEP 2: 從上切線的中垂線開始
        # mid_line = compute_mid_line(upper_tangent)

        # STEP 3: 確定起始多邊形
        # start_polygon_left, start_polygon_right = find_start_polygons(mid_line, VL, VR)

        # STEP 4: 遍歷並合併多邊形
        # 這個步驟你需要根據具體算法來一步步實現
        # 例如：遍歷左右兩邊的多邊形，根據中垂線和邊的交點來決定如何合併
        
        # STEP 5: 將合併後的多邊形加入到V中
        # V.add_polygon(merged_polygon)

        # 返回合併後的VoronoiDiagram
        return V

    def draw_Voronoi_diagram(self, ax, canvas, V, S, points): # 畫出Voronoi diagram
        # S是目前Voronoi diagram 正常會有的點的集合，只用來輸出測試，之後會刪掉
        # points是所有點的集合，用來輸出測試，並且用來畫出所有點，包含不在Voronoi diagram中的點
        canvas_draw_points(ax, canvas, points) # 清除畫布並畫出所有點
        print(f"數量 of S: {len(S)}")
        print(f"S 的座標: {S}")

        # 印出所有Voronoi多邊形的中心
        # 印出所有多邊形中心座標
        centers = []
        for polygon in V.polygons:
            center = polygon.center
            centers.append(f"({center.x}, {center.y})")
        print("所有多邊形的中心座標: ", ", ".join(centers))

    def trigger(self):
        with self.condition:
            self.condition.notify()
    
    def exit(self):
        with self.condition:
            self.set_exit_flag(True)
            self.condition.notify()  # 喚醒所有等待的線程

    def devide(self, S):
        mid = len(S) // 2
        return S[:mid], S[mid:]

    def set_step_by_step(self, value): # 設置 step_by_step 屬性
        with self.condition:
            self.step_by_step = value
    def set_finish(self, value): # 設置 finish 屬性
        with self.condition:
            self.finish = value
    def set_exit_flag(self, value): # 設置 exit_flag 屬性
        with self.condition:
            self.exit_flag = value

    def set_divide_and_conquer_wait(self, value): # 設置 divide_and_conquer_wait 屬性
        with self.condition:
            self.divide_and_conquer_wait = value