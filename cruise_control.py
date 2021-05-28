'''
This file contains the logic for the cruise control algorithms
'''

import utils

# Defining some constants
BRAKE = -10.04
ACCEL = 3.3
LANESUPERPOSITIONS = [180, 280, 380]

def check_collision(player_x, player_y, car_x, car_y):
    '''
    Function to check if two cars have crashed (coordinates overlap)
    Input:
        player_x (int) - The x coordinate of the main car on the screen
        player_y (int) - The y coordinate of the main car on the screen
        car_x (int) - The x coordinate of the secondary car on the screen
        car_y (int) - The y coordinate of the secondary car on the screen
    Output:
        A boolean value denoting if there has been a collosion between the two
        given cars(inputs)
    '''

    return bool((player_x + 42 + 10 > car_x) and (player_x < car_x + 42 + 10) and \
                (player_y < car_y + 60 + 10) and (player_y + 60 + 10 > car_y))

def acc_scenario_1(car_1, car_2, dist):
    '''
    This is the function that handles the first acc scenario (dealing with cruise control
    for a car that is in our lane)
    Input:
        car_1 (Car obj) - This is the main car that is reacting to the speed of car_2
        car_2 (Car obj) - This is the lead car
        dist (string) - This will either be "short", "mid", or "far" indicating the
                        distance at which car_1 will be following car_2
    Output:
        The time in seconds (float) for deceleration
    '''
    # The following distances below represent the time in seconds the main car should be
    # behind the lead car
    follow_dist = dict()
    follow_dist['short'] = 2
    follow_dist['mid'] = 3
    follow_dist['long'] = 4

    # Getting the velocities in m/s rather than km/h
    car_1_vel = utils.kmh_to_ms(car_1.velocity)
    car_2_vel = utils.kmh_to_ms(car_2.velocity)

    # If car1 is moving slower than car2 we don't have to do anything
    if car_1_vel < car_2_vel:
        return 0.0

    # Calculating the time it takes to slow down
    # note that the 12 used below is to convert from meters to pixels
    time = utils.calculate_time(car_1.velocity, car_2.velocity)
    delta_d = ((car_1_vel - car_2_vel) / 2) * time * 12

    if car_1.x_pos == car_2.x_pos and \
       abs(car_1.y_pos - car_2.y_pos) <= (follow_dist[dist] * delta_d):
        return time

    # This is the case where the lead car is moving slower then the main car, but the
    # the lead car is not close enough to do anything about it
    return 0.0

def check_lane_change(direction, car_1, cars_on_road):
    '''
    This function that will validate whether a lane change requested by the user
    is safe to perform
    Input:
        direction (int) - A 0 (for left) or 1 (for right) to indicate the direction
        car_1 (Car obj) - The main car on the road
        cars_on_road (dict of Car objs) - All of the cars currently on the road
    Output:
        A boolean value denoting if the lane change requested by the user is safe
        to perform
    '''
    player_vel = utils.kmh_to_ms(car_1.velocity)

    # Get all of the cars in the left, middle, and right lanes
    left_cars = set()
    middle_cars = set()
    right_cars = set()
    cars = [left_cars, middle_cars, right_cars]

    # Adding the cars to their respective lane set
    for car in cars_on_road:
        cars[car.cur_lane].add(car)

    # This first check is accounting for the case when the cars try to turn off the road
    if (car_1.x_pos == LANESUPERPOSITIONS[0] and direction == 0) or \
        (car_1.x_pos == LANESUPERPOSITIONS[2] and direction == 1):
        return False

    # All of the following scenarios will follow the same general set of guidelines:
    # 1. The car will only be allowed to change lanes if there is no car in the zone
    #    (+- 2 car lengths in size) in the direction they wish to turn
    # 2. The cars behind the main car in the adjacent lane they wish to turn to are not
    #    going more than 20m/s faster than the main car (so they have time to slow down)

    lower = car_1.y_pos - 3 * car_1.height
    upper = car_1.y_pos + 3 * car_1.height

    # The car wants to make a right turn from the left or left turn from the right
    if car_1.x_pos in range(180, 281) and direction == 1 or \
        car_1.x_pos in range(280, 381) and direction == 0:
        for car in middle_cars:
            car_vel = utils.kmh_to_ms(car.velocity)
            relative_vel = car_vel - player_vel
            if int (car.y_pos) in range(lower, upper) or \
                (relative_vel > 20 and car.y_pos < car_1.y_pos):
                return False

    # The car wants to make a right turn from the middle lane
    elif car_1.x_pos in range(280, 381) and direction == 1:
        for car in right_cars:
            car_vel = utils.kmh_to_ms(car.velocity)
            relative_vel = car_vel - player_vel
            if int (car.y_pos) in range(lower, upper) or \
                (relative_vel > 20 and car.y_pos < car_1.y_pos):
                return False

    # The car wants to make a left turn from the middle lane
    elif car_1.x_pos in range(180, 280) and direction == 0:
        for car in left_cars:
            car_vel = utils.kmh_to_ms(car.velocity)
            relative_vel = car_vel - player_vel
            if int (car.y_pos ) in range(lower, upper) or \
                (relative_vel > 20 and car.y_pos < car_1.y_pos):
                return False

    # If all checks pass then we are safe to make the lane change
    return True
