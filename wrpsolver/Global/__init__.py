import numpy as np
tolerance = 3
pic_size = 100
step = 1
threadNum = 24
def MyRound(num, tolerance):
    fmt = '.' + str(tolerance) + 'f'
    return float(format(num, fmt))

