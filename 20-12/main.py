import os
import sys
from util import RaceCondition

race_condition = RaceCondition("data.txt")
print(f"Part 1 : {race_condition.solution_one()}")
print(f"Part 2 : {race_condition.solution_two()}")
