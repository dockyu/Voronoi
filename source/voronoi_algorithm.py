import threading
from controller import canvas_draw_points
from data_structure import Point, Edge, Polygon, VoronoiDiagram
from convex_hull_algorithm import find_lower_tangents, find_upper_tangents, create_new_convex_hull

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
        voronoi.convex_hull.append(0) # 因為只有一個點，所以凸包Polygons中第一個多邊形的中心
        voronoi.leftmost_point_index = 0 # 因為只有一個點，所以最左點就是這個點
        voronoi.rightmost_point_index = 0 # 因為只有一個點，所以最右點就是這個點
        return voronoi

    def merge(self, VL, VR): # 合併VL和VR，得出V也就是S的Voronoi diagram
        # 初始化結果的VoronoiDiagram
        V = VoronoiDiagram()

        # STEP 1: 合併VL和VR的voronoi多邊形
        V.polygons = VL.polygons + VR.polygons

        # STEP 2: 找出VL和VR的切線（這個部分需要你根據具體算法來實現）
        upper_tangent_left, upper_tangent_right = find_upper_tangents(VL, VR)
        lower_tangent_left, lower_tangent_right = find_lower_tangents(VL, VR)
        # upper_tangent_left 是上切線在VL中的點的索引
        # upper_tangent_right 是上切線在VR中的點的索引
        # lower_tangent_left 是下切線在VL中的點的索引
        # lower_tangent_right 是下切線在VR中的點的索引
        # print(f"upper_tangent_left: {upper_tangent_left}")
        # print(f"upper_tangent_right: {upper_tangent_right}")
        # print(f"lower_tangent_left: {lower_tangent_left}")
        # print(f"lower_tangent_right: {lower_tangent_right}")

        # STEP 3: 利用切線創建新的凸包多邊形
        create_new_convex_hull(V, VL, VR, upper_tangent_left, upper_tangent_right, lower_tangent_left, lower_tangent_right)




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

        # 測試用，之後會刪掉
        # print(f"數量 of S: {len(S)}")
        # print(f"S 的座標: {S}")

        # 印出所有 polygon 的中心
        polygon_centers = [f"({polygon.center.x}, {polygon.center.y})" for polygon in V.polygons]
        print(f"Polygon Centers: {', '.join(polygon_centers)}")
        # 印出 convex hull 對應的中心的點
        convex_hull_centers = [f"({V.polygons[index].center.x}, {V.polygons[index].center.y})" for index in V.convex_hull]
        print(f"Convex Hull Centers: {', '.join(convex_hull_centers)}")
        # 印出 left 和 right 的座標
        left_point = "None"
        right_point = "None"
        if V.leftmost_point_index is not None:
            left_point = f"({V.polygons[V.leftmost_point_index].center.x}, {V.polygons[V.leftmost_point_index].center.y})"
        if V.rightmost_point_index is not None:
            right_point = f"({V.polygons[V.rightmost_point_index].center.x}, {V.polygons[V.rightmost_point_index].center.y})"
        print(f"Left: {left_point}, Right: {right_point}")
        return

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