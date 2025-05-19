def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']

    if not all_wheels_on_track or is_offtrack or is_reversed:
        return 1e-3

    reward = 1.0

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        return 1e-3

    SPEED_THRESHOLD = 3.0
    if speed >= SPEED_THRESHOLD:
        reward += 1.0
    else:
        reward += speed / SPEED_THRESHOLD

    if steps > 0:
        progress_reward = progress / steps
        reward += progress_reward * 2.0

    TOTAL_STEPS_THRESHOLD = 300
    if progress == 100 and steps < TOTAL_STEPS_THRESHOLD:
        reward += 10.0

    return float(reward)