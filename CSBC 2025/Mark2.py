import math

def reward_function(params):

    if not params['all_wheels_on_track']:
        return 1e-3 
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    progress = params['progress']
    steering = abs(params['steering_angle'])
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    MARKER_1 = 0.1 * track_width
    MARKER_2 = 0.25 * track_width
    MARKER_3 = 0.5 * track_width

    if distance_from_center <= MARKER_1:
        reward = 1.0
    elif distance_from_center <= MARKER_2:
        reward = 0.5
    elif distance_from_center <= MARKER_3:
        reward = 0.1
    else:
        return 1e-3  
    
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.degrees(math.atan2(
        next_point[1] - prev_point[1],
        next_point[0] - prev_point[0]))

    direction_diff = abs(track_direction - heading) % 360
    if direction_diff > 180:
        direction_diff = 360 - direction_diff 

    CURVE_THRESHOLD = 15.0  
    is_curve = direction_diff > CURVE_THRESHOLD

    if is_curve and steering < CURVE_THRESHOLD:
        reward *= 0.5  

    MAX_SPEED = 4.0
    MIN_SPEED = 0.5
    if not is_curve and speed >= MAX_SPEED * 0.9: 
        reward += 1.0  

    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.8  

    STRAIGHT_THRESHOLD = 5.0
    if steering > STRAIGHT_THRESHOLD and not is_curve:
        reward *= 0.9  

    reward += (progress / 100.0) ** 2  
    
    return float(max(reward, 1e-3))