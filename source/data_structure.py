# 點類別
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 邊類別
class Edge:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

# 多邊形類別
class Polygon:
    def __init__(self, center):
        self.edges = []
        self.center = center  # 新增：多邊形的「中心點」

    def add_edge(self, edge):
        self.edges.append(edge)

# Voronoi Diagram類別
class VoronoiDiagram:
    def __init__(self):
        self.polygons = []
        self.convex_hull = []  # 初始化為空列表，往下是順時針儲存凸包多邊形的索引
        self.leftmost_point_index = None  # 最左點的索引
        self.rightmost_point_index = None  # 最右點的索引

    def add_polygon(self, polygon):
        self.polygons.append(polygon)
