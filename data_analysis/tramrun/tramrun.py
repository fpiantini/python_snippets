#!/usr/bin/env python3
#
# References:
#   - https://realpython.com/python-matplotlib-guide/
#

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from plotutils import mplu_text, mplu_realcircle

POS_SAMPLING_PERIOD_MS = 4  # milliseconds
ODO_SAMPLING_PERIOD_MS = 128 # milliseconds, shall be a sample of POS_SAMPLING_PERIOD_MS
ODO_SAMPLING_FACTOR = ODO_SAMPLING_PERIOD_MS / POS_SAMPLING_PERIOD_MS

START_POS = 1000
START_ODO = 123456

# ---------------------------------------------------
# from: https://matplotlib.org/examples/showcase/anatomy.html
def circle(ax, x, y, radius=0.15):
    from matplotlib.patches import Ellipse
    from matplotlib.patheffects import withStroke


    # calculate asymmetry of x and y axes:
    x0, y0 = ax.transAxes.transform((-0.05, 995)) # lower left in pixels
    x1, y1 = ax.transAxes.transform((2.05, 1040)) # upper right in pixes
    dx = x1 - x0
    dy = y1 - y0
    maxd = max(dx, dy)
    width = radius * maxd / dx
    height = radius * maxd / dy

    print(f"(x0,y0) = ({x0},{y0}), (x1,y1) = ({x1},{y1})")
    print(f"width = {width}, height = {height}")
    circle = Ellipse((x, y), width, height, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)

def text(ax, x, y, text):
    ax.text(x, y, text, backgroundcolor="white",
            ha='center', va='top', weight='bold', color='blue')
# ---------------------------------------------------


# ---------------------------------------------------
def update_speed_constant(v, t, delta_t):
    return v

# ---------------------------------------------------
def update_speed_constant_until2_then_stop(v, t, delta_t):
    if t < 2000:
        return v
    return 0

# ---------------------------------------------------
def update_speed_constant_until2_then_soft_bracking(v, t, delta_t):
    if t < 2000:
        return v
    if v >= 1:
        return v - 0.05
    return 0

# ---------------------------------------------------
def update_pos(s0, v0, delta_t_ms):
    """
    Given the position and speed at time t0 (s0, v0),
    computes the new position at time t1 = t0 + delta_t
    """
    return s0 + (v0 * delta_t_ms / 1000)

# ---------------------------------------------------
def time_to_sampling_index(t_ms, sampling_time_ms):
    """
    Given a time in second and a sampling time in ms,
    return the index in the position array with the
    position at time t_ms
    """
    return t_ms // sampling_time_ms


# ---------------------------------------------------
def tag_checking(prev_real_pos, curr_real_pos, curr_avl_pos, tag_pos_list):
    for tag_pos in tag_pos_list:
        if prev_real_pos < tag_pos and tag_pos <= curr_real_pos:
            return tag_pos
    return curr_avl_pos

# ---------------------------------------------------
def odometer_delta(real_pos, t_ms, odo_delay_ms):
    if t_ms % ODO_SAMPLING_PERIOD_MS == 0:
        t_new_odo_ms = t_ms - odo_delay_ms
        t_prev_odo_ms = t_new_odo_ms - ODO_SAMPLING_PERIOD_MS
        if t_prev_odo_ms >= 0:
            return abs(real_pos[time_to_sampling_index(t_new_odo_ms, POS_SAMPLING_PERIOD_MS)] -
                       real_pos[time_to_sampling_index(t_prev_odo_ms, POS_SAMPLING_PERIOD_MS)])
    return 0

# ---------------------------------------------------
def tram_run_constant_speed_no_odo_delay_no_tag():
    t_start_ms = 0
    t_end_ms = 2000

    t_array = []
    real_pos = []
    odo = []
    avl_pos = []
    error = []
    t_ms = t_start_ms
    v_m_s = 19.4
    current_real_pos = START_POS
    current_avl_pos = START_POS

    current_odo = START_ODO

    while t_ms <= t_end_ms:

        t_array.append(t_ms / 1000)

        previous_real_pos = current_real_pos
        v_m_s = update_speed_constant(v_m_s, t_ms, POS_SAMPLING_PERIOD_MS)
        current_real_pos = update_pos(current_real_pos,v_m_s, POS_SAMPLING_PERIOD_MS)
        real_pos.append(current_real_pos)

        current_avl_pos = tag_checking(previous_real_pos, current_real_pos, current_avl_pos, ())
        current_avl_pos += odometer_delta(real_pos, t_ms, 0)
        avl_pos.append(current_avl_pos)

        error.append(current_real_pos - current_avl_pos)

        t_ms += POS_SAMPLING_PERIOD_MS

    fig, ax_err = plt.subplots()

    ax_err.set_xlabel('time (s)')

    # instantiate a second axes that shares the same x-axis
    ax_err.set_ylabel('Error (m)', color='blue')
    ax_err.plot(t_array, error, color='lightblue')
    ax_err.tick_params(axis='y', color='blue')
    ax_err.set_ylim([-5, 40])
    ax_err.fill_between(t_array, error, color='lightblue')

    ax = ax_err.twinx()
    ax.set_ylabel('Tram position (m)')
    ax.plot(t_array, real_pos, color='tab:green')
    ax.plot(t_array, avl_pos, color='firebrick')
    ax.tick_params(axis='y')
    ax.set_ylim([995, 1040])
    ax.set_title(f"Tram position sampling error (constant speed = {v_m_s} m/s)")

    ax.legend(['real pos', 'estimated pos'], loc=(0.05, 0.86))
    ax_err.legend(['error'], loc=(0.05,0.78))

# ---------------------------------------------------
def tram_run_constant_speed_no_odo_delay_with_tag():
    t_start_ms = 0
    t_end_ms = 2000

    t_array = []
    real_pos = []
    odo = []
    avl_pos = []
    error = []
    t_ms = t_start_ms
    current_real_pos = START_POS
    current_avl_pos = START_POS
    v_m_s = 19.4

    current_odo = START_ODO

    while t_ms <= t_end_ms:

        t_array.append(t_ms / 1000)

        previous_real_pos = current_real_pos
        v_m_s = update_speed_constant(v_m_s, t_ms, POS_SAMPLING_PERIOD_MS)
        current_real_pos = update_pos(current_real_pos, v_m_s, POS_SAMPLING_PERIOD_MS)
        real_pos.append(current_real_pos)

        current_avl_pos = tag_checking(previous_real_pos, current_real_pos, current_avl_pos, (1019,))
        current_avl_pos += odometer_delta(real_pos, t_ms, 0)
        avl_pos.append(current_avl_pos)

        error.append(current_real_pos - current_avl_pos)

        t_ms += POS_SAMPLING_PERIOD_MS

    fig, ax_err = plt.subplots()

    ax_err.set_xlabel('time (s)')

    # instantiate a second axes that shares the same x-axis
    ax_err.set_ylabel('Error (m)', color='blue')
    ax_err.plot(t_array, error, color='lightblue')
    ax_err.tick_params(axis='y', color='blue')
    ax_err.set_ylim([-5, 40])
    ax_err.fill_between(t_array, error, color='lightblue')

    ax = ax_err.twinx()
    ax.set_ylabel('Tram position (m)')
    ax.plot(t_array, real_pos, color='tab:green')
    ax.plot(t_array, avl_pos, color='firebrick')
    ax.tick_params(axis='y')
    ax.set_ylim([995, 1040])
    ax.set_title(f"Tram position, sampling error after tag reading (constant speed = {v_m_s} m/s)")

    ax.legend(['real pos', 'estimated pos'], loc=(0.05, 0.86))
    ax_err.legend(['error'], loc=(0.05,0.78))

    mplu_realcircle(ax, 0.975, 1017.5, 0.03)
    mplu_text(ax, 1.24, 1017.5, "tag reading")

# ---------------------------------------------------
def tram_run_constant_speed_odo_delay_with_tag():
    t_start_ms = 0
    t_end_ms = 2000

    t_array = []
    real_pos = []
    odo = []
    avl_pos = []
    error = []
    t_ms = t_start_ms
    current_real_pos = START_POS
    current_avl_pos = START_POS
    v_m_s = 19.4

    current_odo = START_ODO

    while t_ms <= t_end_ms:

        t_array.append(t_ms / 1000)

        previous_real_pos = current_real_pos
        v_m_s = update_speed_constant(v_m_s, t_ms, POS_SAMPLING_PERIOD_MS)
        current_real_pos = update_pos(current_real_pos, v_m_s, POS_SAMPLING_PERIOD_MS)
        real_pos.append(current_real_pos)

        current_avl_pos = tag_checking(previous_real_pos, current_real_pos, current_avl_pos, (1019,))
        current_avl_pos += odometer_delta(real_pos, t_ms, 256)
        avl_pos.append(current_avl_pos)

        error.append(current_real_pos - current_avl_pos)

        t_ms += POS_SAMPLING_PERIOD_MS

    fig, ax_err = plt.subplots()

    ax_err.set_xlabel('time (s)')

    # instantiate a second axes that shares the same x-axis
    ax_err.set_ylabel('Error (m)', color='blue')
    ax_err.plot(t_array, error, color='lightblue')
    ax_err.tick_params(axis='y', color='blue')
    ax_err.set_ylim([-5, 40])
    ax_err.fill_between(t_array, error, color='lightblue')

    ax = ax_err.twinx()
    ax.set_ylabel('Tram position (m)')
    ax.plot(t_array, real_pos, color='tab:green')
    ax.plot(t_array, avl_pos, color='firebrick')
    ax.tick_params(axis='y')
    ax.set_ylim([995, 1040])
    ax.set_title(f"Tram position, with odometer delay (constant speed = {v_m_s} m/s)")

    ax.legend(['real pos', 'estimated pos'], loc=(0.05, 0.86))
    ax_err.legend(['error'], loc=(0.05,0.78))

    mplu_realcircle(ax, 0.975, 1012.5, 0.03)
    mplu_text(ax, 1.24, 1012, "tag reading")

# ---------------------------------------------------
def tram_run_constant_speed_then_hard_stop_odo_delay_with_tag():
    t_start_ms = 0
    t_end_ms = 2500

    t_array = []
    real_pos = []
    odo = []
    avl_pos = []
    error = []
    t_ms = t_start_ms
    current_real_pos = START_POS
    current_avl_pos = START_POS
    v_m_s = 19.4

    current_odo = START_ODO

    while t_ms <= t_end_ms:

        t_array.append(t_ms / 1000)

        previous_real_pos = current_real_pos
        v_m_s = update_speed_constant_until2_then_stop(v_m_s, t_ms, POS_SAMPLING_PERIOD_MS)
        current_real_pos = update_pos(current_real_pos, v_m_s, POS_SAMPLING_PERIOD_MS)
        real_pos.append(current_real_pos)

        current_avl_pos = tag_checking(previous_real_pos, current_real_pos, current_avl_pos, (1019,))
        current_avl_pos += odometer_delta(real_pos, t_ms, 256)
        avl_pos.append(current_avl_pos)

        error.append(current_real_pos - current_avl_pos)

        t_ms += POS_SAMPLING_PERIOD_MS

    fig, ax_err = plt.subplots()

    ax_err.set_xlabel('time (s)')

    # instantiate a second axes that shares the same x-axis
    ax_err.set_ylabel('Error (m)', color='blue')
    ax_err.plot(t_array, error, color='lightblue')
    ax_err.tick_params(axis='y', color='blue')
    ax_err.set_ylim([-10, 45])
    ax_err.fill_between(t_array, error, color='lightblue')

    ax = ax_err.twinx()
    ax.set_ylabel('Tram position (m)')
    ax.plot(t_array, real_pos, color='tab:green')
    ax.plot(t_array, avl_pos, color='firebrick')
    ax.tick_params(axis='y')
    ax.set_ylim([995, 1050])
    ax.set_title(f"Tram position, with odometer delay (constant speed + hard bracking)")

    ax.legend(['real pos', 'estimated pos'], loc=(0.05, 0.86))
    ax_err.legend(['error'], loc=(0.05,0.78))

    mplu_realcircle(ax, 0.975, 1012.5, 0.03)
    mplu_text(ax, 1.24, 1012, "tag reading")

# ---------------------------------------------------
def tram_run_constant_speed_then_soft_stop_odo_delay_with_tag():
    t_start_ms = 0
    t_end_ms = 5000

    t_array = []
    real_pos = []
    odo = []
    avl_pos = []
    error = []
    t_ms = t_start_ms
    current_real_pos = START_POS
    current_avl_pos = START_POS
    v_m_s = 19.4

    current_odo = START_ODO

    while t_ms <= t_end_ms:

        t_array.append(t_ms / 1000)

        previous_real_pos = current_real_pos
        v_m_s = update_speed_constant_until2_then_soft_bracking(v_m_s, t_ms, POS_SAMPLING_PERIOD_MS)
        current_real_pos = update_pos(current_real_pos, v_m_s, POS_SAMPLING_PERIOD_MS)
        real_pos.append(current_real_pos)

        current_avl_pos = tag_checking(previous_real_pos, current_real_pos, current_avl_pos, (1019,))
        current_avl_pos += odometer_delta(real_pos, t_ms, 256)
        avl_pos.append(current_avl_pos)

        error.append(current_real_pos - current_avl_pos)

        t_ms += POS_SAMPLING_PERIOD_MS

    fig, ax_err = plt.subplots()

    ax_err.set_xlabel('time (s)')

    # instantiate a second axes that shares the same x-axis
    ax_err.set_ylabel('Error (m)', color='blue')
    ax_err.plot(t_array, error, color='lightblue')
    ax_err.tick_params(axis='y', color='blue')
    ax_err.set_ylim([-10, 60])
    ax_err.fill_between(t_array, error, color='lightblue')

    ax = ax_err.twinx()
    ax.set_ylabel('Tram position (m)')
    ax.plot(t_array, real_pos, color='tab:green')
    ax.plot(t_array, avl_pos, color='firebrick')
    ax.tick_params(axis='y')
    ax.set_ylim([995, 1065])
    ax.set_title(f"Tram position, with odometer delay (constant speed + soft braking)")

    ax.legend(['real pos', 'estimated pos'], loc=(0.05, 0.86))
    ax_err.legend(['error'], loc=(0.05,0.78))

# ---------------------------------------------------
def main():
    sns.set_style('darkgrid')
    tram_run_constant_speed_no_odo_delay_no_tag()
    tram_run_constant_speed_no_odo_delay_with_tag()
    tram_run_constant_speed_odo_delay_with_tag()
    tram_run_constant_speed_then_hard_stop_odo_delay_with_tag()
    tram_run_constant_speed_then_soft_stop_odo_delay_with_tag()
    plt.show()



if __name__ == '__main__':
    main()

