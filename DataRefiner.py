import numpy as np
def getWMkt(cap: list):
    return (np.array(cap) / np.sum(cap,axis=1)[0])[0]
