# Sean A
# Bear Fish River
# Using our knowledge of 2D arrays, make a bear vs. fish survival simulation

from ecosystem import *
from time import sleep

DAYS_SIMULATED =  30 # default 30
RIVER_SIZE = 15  # default 15
START_BEARS = 10
START_FISH = 10


def BearFishRiver():
    r = River(RIVER_SIZE, START_BEARS, START_FISH)
    day = 0
    done = False
    for day in range(DAYS_SIMULATED):
        if done is not True:
            print(f"\n\nDay: {day + 1}")
            print(r)
            print(f"\nStarting Poplation: {r.population} animals")
            done = r.new_day()
            print(f"Ending Poplation: {r.population} animals")
            print(r)
            day += 1
            sleep(2)
        else:
            break
    print("The simulation has ended.")


if __name__ == "__main__":
    BearFishRiver()
