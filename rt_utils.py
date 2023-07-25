import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime as dt
from scipy.integrate import odeint
from scipy.optimize import curve_fit
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import gamma

def deriv_SIR(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def deriv_SEIR(y, t, N, beta,sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt

# SIR: Predict S, I, R given S0, I0, R0, beta, gamma
def SIR_predict(y0, t, beta, gamma):
    ret = odeint(deriv_SIR, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    return S, I, R

# SIR: Used to find I0, beta, gamma via curve_fit
def SIR_first(t, I0, beta, gamma):
    S0 = N - I0 - R0
    y0 = np.array([S0, I0, R0])
    ret = odeint(deriv_SIR, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    return I

# SEIR: Predict S, E, I, R given S0, I0, R0, beta, gamma
def SEIR_predict(y0, t, beta, sigma, gamma):
    ret = odeint(deriv_SEIR, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = ret.T
    return S, E, I, R

# Used to find beta, gamma via curve_fit
def SEIR(t, beta, sigma, gamma):
    ret = odeint(deriv_SEIR, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = ret.T
    return I

def R_0(beta, gamma):
    return beta / gamma

# # Used to find beta, gamma via curve_fit
# def SIR(t, beta, gamma):
#     ret = odeint(deriv_SIR, y0, t, args=(N, beta, gamma))
#     S, I, R = ret.T
#     return I

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

# Percentual variation
def percentual_change(x, media = 7):
    perc = [0]
    day = [0]
    for i in range(0,len(x)-1, media):
        var1 = x[i:i+media].mean()
        var2 = x[i+media:i+media*2].mean()
        ch = (var2 - var1)
        perc.append(ch)
        day.append(int(i+media/2))
    return perc, day

def fit_SIR_first(tmin, tmax, y0):
    print('Start: ', xdata[tmin])
    print('End: ', xdata[tmax])
    t = np.arange(tmin, tmax)
    
    # This part is to predict R0 and I0 at the beginning of the epidemic
    p0 = [400, 0.8, 1./10]
    popt,_ = curve_fit(SIR_first, t, np.array(I[tmin:tmax]), p0) # the outputs are I0, beta, gamma fitted
    print('Rt = ', R_0(popt[1], popt[2]))
    R_0_list.append(R_0(popt[1], popt[2]))
    
    # This part is to estimate s, i, r at the end of the time lapse
    I0, R0 = int(popt[0]), R[tmax]
    S0 = N - I0 - R0
    y0 = S0, I0, R0
    s, i, r = SIR_predict(y0, t, popt[1], popt[2])
    i_list.append(i)
    return s, i, r

def fit_SEIR(tmin, tmax, y0, append = True):
    if append:
        print('Start: ', xdata[tmin])
        print('End: ', xdata[tmax])
    t = np.arange(tmin, tmax)
    
    # This part is to predict R0
    popt, _ = curve_fit(SEIR, t, np.array(I[tmin:tmax]), bounds = (0, [3., 3., 1.]))
    if append:
        R_0_list.append(R_0(popt[0], popt[2]))
        print('Rt = ', R_0(popt[0], popt[2]))
        
    # This part is to estimate s, e, i, r at the end of the time lapse
    s, e, i, r = SEIR_predict(y0, t, popt[0], popt[1], popt[2])
    if append:
        i_list.append(i)
    return s, e, i, r