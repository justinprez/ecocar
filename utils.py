'''
This file contains a bunch of helper functions
'''

import random
import cruise_control
from car import Car

# Defining some constants
BRAKE = -10.04
ACCEL = 3.3
GREY = (159, 163, 168)
LANESUPERPOSITIONS = [180, 280, 380]

def update_velocity(initial_velocity, target_velocity, elapsed_time):
    '''
    This is a function that will be called to show the acceleration and deceleration of the
    car smoothly
    Input:
        initial_velocity (float) - The initial velocity for the car
        target_velocity (float) - The target velocity for the car
        elapsed_time (float) - The time that has passed since the car started accelerating
    Output:
        A double representing the updated speed of the car
    '''
    initial = kmh_to_ms(initial_velocity)
    target = kmh_to_ms(target_velocity)
    if target > initial:
        return ms_to_kmh(ACCEL * elapsed_time + initial)
    return ms_to_kmh(BRAKE * elapsed_time + initial)


def calculate_time(initial_velocity, target_velocity):
    '''
    This is a function that will be called to get the time it will take to update
    the velocity of the car to the desired speed
    Input:
        initial_velocity (double) - The current velocity of the car
        target_velocity (double) - The desired velocity of the car
    Output:
        The time it will take in seconds to get to our desired speed
    '''
    cur = kmh_to_ms(initial_velocity)
    target = kmh_to_ms(target_velocity)
    if cur > target:
        return (target - cur) / BRAKE
    return (target - cur) / ACCEL

def kmh_to_ms(velocity):
    '''
    Function to convert from km/h to m/s
    Input:
        velocity (double) - The velocity of the car in km/h
    Output:
        A double representing the velocity of the car in m/s
    '''
    return velocity * (5 / 18)


def ms_to_kmh(velocity):
    '''
    Function to convert from m/s to km/h
    Input:
        velocity (double) - The velocity of the car in m/s
    Output:
        A double representing the velocity of the car in km/h
    '''
    return velocity * (18 / 5)

def is_int(string):
    '''
    Method to check if a given string is an integer
    '''
    try:
        int(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def ms_to_sec(milli):
    '''
    Function to convert from milliseconds to seconds
    Input:
        milli (double)
    Output:
        The time inputted in seconds
    '''
    return milli / 1000

def lane_change(player, buttons, cars_on_road):
    '''
    This function checks if a button has been pressed for a lane change, if yes it will
    then complete the lane change
    Input:
        player (Car obj) - The main car that we are moving
        buttons (dict of buttons) - The left and right lane change buttons
        cars_on_road (dict of Car objs) - All of the cars currently on the road
    Output:
        A boolean value denoting whether or not a lange change has occured
    '''
    change = False

    if buttons['left'].pressed and player.x_pos != LANESUPERPOSITIONS[0]:
        change = cruise_control.check_lane_change(0, player, cars_on_road)
        if change and player.x_pos > LANESUPERPOSITIONS[player.cur_lane - 1]:
            player.x_pos -= 2

        if player.x_pos <= LANESUPERPOSITIONS[player.cur_lane - 1]:
            buttons['left'].pressed = False
            player.cur_lane -= 1
            player.x_pos = LANESUPERPOSITIONS[player.cur_lane]
            buttons['left'].colour = GREY
            return True
    else:
        buttons['left'].colour = GREY

    if buttons['right'].pressed and player.x_pos != LANESUPERPOSITIONS[2]:
        change = cruise_control.check_lane_change(1, player, cars_on_road)
        if change and player.x_pos < LANESUPERPOSITIONS[player.cur_lane + 1]:
            player.x_pos += 2

        if player.x_pos >= LANESUPERPOSITIONS[player.cur_lane + 1]:
            buttons['right'].pressed = False
            player.cur_lane += 1
            player.x_pos = LANESUPERPOSITIONS[player.cur_lane]
            buttons['right'].colour = GREY
            return True
    else:
        buttons['right'].colour = GREY

    return False

def car_spwan(spawn_button, cars_on_road, cars_on_screen):
    '''
    This function spawns a car with a random speed and lane
    Input:
        spawn_button (button obj) - The button that when pressed will spawn a car
        cars_on_road (set Car objs) - A set containing all of the cars on screen
        cars_on_screen (int) - A value denoting how many cars are on the screen
    Output:
        - None if the button is not pressed or the screen is full
        - Otherwise a car object is returned for the car to be created
    '''
    if spawn_button.pressed and cars_on_screen < 10:
        # Set the button back to its unpressed state and change colour back to GREY
        spawn_button.pressed = not spawn_button.pressed
        spawn_button.colour = GREY

        # Randomly generate the x and y positions of the new car
        lane =  1 #random.randint(0, 2)
        y_pos = 200 #random.randint(0, 600)
        x_pos = LANESUPERPOSITIONS[lane]

        # Randomly generate the speed of the new car
        velocity = random.randint(50, 100)
        print(velocity)

        # Checking if the car overlaps with any other cars
        for car in cars_on_road:
            while cruise_control.check_collision(x_pos, y_pos, car.x_pos, car.y_pos):
                lane = random.choice([0, 2])
                y_pos = random.randint(0, 800)
                x_pos = LANESUPERPOSITIONS[lane]

        return Car(x_pos, y_pos, lane, velocity)
