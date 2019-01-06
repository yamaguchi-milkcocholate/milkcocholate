import numpy as np
from modules.fitnessfunction.fitnessfunction import FitnessFunction


class ZigZagFunction(FitnessFunction):
    FITNESS_FUNCTION_ID = 7

    BUY = 1
    STAY = 2
    SELL = 3
