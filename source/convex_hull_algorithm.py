

def calculate_slope(point1, point2):
    if point1.x == point2.x:
        return float('inf')  # 垂直線
    return (point2.y - point1.y) / (point2.x - point1.x)


def find_upper_tangents(VL, VR):
    upper_tangent_left = VL.rightmost_point_index
    upper_tangent_right = VR.leftmost_point_index
    left_moved = True
    right_moved = True
    
    while left_moved or right_moved:
        left_moved = False
        right_moved = False
        
        # 計算上一個左側點的索引
        next_left_index = (upper_tangent_left - 1 + len(VL.convex_hull)) % len(VL.convex_hull)
        # 計算斜率
        slope_left = calculate_slope(VL.polygons[upper_tangent_left].center, VR.polygons[upper_tangent_right].center)
        slope_next_left = calculate_slope(VL.polygons[next_left_index].center, VR.polygons[upper_tangent_right].center)
        
        if slope_next_left < slope_left:
            upper_tangent_left = next_left_index
            left_moved = True # 此次有左邊有移動
            
        # 計算下一個右側點的索引
        next_right_index = (upper_tangent_right + 1) % len(VR.convex_hull)
        # 計算斜率
        slope_right = calculate_slope(VL.polygons[upper_tangent_left].center, VR.polygons[upper_tangent_right].center)
        slope_next_right = calculate_slope(VL.polygons[upper_tangent_left].center, VR.polygons[next_right_index].center)
        
        if slope_next_right > slope_right:
            upper_tangent_right = next_right_index
            right_moved = True
            
    return upper_tangent_left, upper_tangent_right

def find_lower_tangents(VL, VR):
    lower_tangent_left = VL.rightmost_point_index  # 初始化為 VL 的最右點
    lower_tangent_right = VR.leftmost_point_index  # 初始化為 VR 的最左點
    left_moved = True
    right_moved = True
    
    while left_moved or right_moved:
        left_moved = False
        right_moved = False
        
        # 計算下一個左側點的索引
        next_left_index = (lower_tangent_left + 1) % len(VL.convex_hull)  # 這裡改為 +1
        # 計算斜率
        slope_left = calculate_slope(VL.polygons[lower_tangent_left].center, VR.polygons[lower_tangent_right].center)
        slope_next_left = calculate_slope(VL.polygons[next_left_index].center, VR.polygons[lower_tangent_right].center)
        
        if slope_next_left > slope_left:
            lower_tangent_left = next_left_index
            left_moved = True
            
        # 計算上一個右側點的索引
        next_right_index = (lower_tangent_right - 1 + len(VR.convex_hull)) % len(VR.convex_hull)  # 這裡改為 -1
        # 計算斜率
        slope_right = calculate_slope(VL.polygons[lower_tangent_left].center, VR.polygons[lower_tangent_right].center)
        slope_next_right = calculate_slope(VL.polygons[lower_tangent_left].center, VR.polygons[next_right_index].center)
        
        if slope_next_right < slope_right:
            lower_tangent_right = next_right_index
            right_moved = True
            
    return lower_tangent_left, lower_tangent_right

def create_new_convex_hull(V, VL, VR, upper_tangent_left, upper_tangent_right, lower_tangent_left, lower_tangent_right):
    # 第一步：創建新的 convex_hull
    new_convex_hull = []
    
    # 從 VR 的上切線開始，順時針走到下切線
    i = upper_tangent_right
    while True:
        new_convex_hull.append(i + len(VL.polygons))  # 注意要加 len(VL.polygons)
        if i == lower_tangent_right:
            break
        i = (i + 1) % len(VR.convex_hull)
    
    # 從 VL 的下切線開始，順時針走到上切線
    i = lower_tangent_left
    while True:
        new_convex_hull.append(i)
        if i == upper_tangent_left:
            break
        i = (i + 1) % len(VL.convex_hull)
    
    V.convex_hull = new_convex_hull

    # 第二步：設置新的 leftmost 和 rightmost 索引
    V.leftmost_point_index = VL.leftmost_point_index
    V.rightmost_point_index = VR.rightmost_point_index + len(VL.polygons)