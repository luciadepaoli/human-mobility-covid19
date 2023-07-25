import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime as dt
from scipy.integrate import odeint
from scipy.optimize import curve_fit
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import gamma
import sys
import geopandas as gpd
import datetime
from scipy import signal
import fathon

def shift(xs, n):
    if n > 0:
        return np.r_[np.full(n, np.nan), xs[:-n]]
    elif n==0:
        return xs
    else:
        return np.r_[xs[-n:], np.full(-n, np.nan)]
    
# R_t functions based on known parameters
def generation_time(x):
    return gamma.pdf(x, 1.88, scale=1./0.26)

def R_t(I, t):
    num = I[t]
    den = 0
    for s in range(0,t+1):
        den += I[t-s] * generation_time(s)
    return num/den

def normalized(x, factor = 1, normalized = True):
    if normalized:
        return (x-min(x))/(max(x)-min(x))*factor
    else:
        return x