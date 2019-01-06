import pandas as pd
import numpy as np
import pickle
import sys
import os
from modules.datamanager.picker import Picker


class ZigZag:

    def __init__(self, use_of_data='training'):
        picker = Picker(span='15min', use_of_data=use_of_data, coin='xrp')
        self.candlestick = picker.get_candlestick()
