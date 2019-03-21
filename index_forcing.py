import numpy as np

def index_forcing(precip0, 
                  temp0, 
                  h0,
                  precip1, 
                  temp1, 
                  h1,
                  h, 
                  index, 
                  temp_lapse_rate, 
                  precip_decay_rate, 
                  precip_thresh_height):

    temp_cur = computeT(temp0, temp1, h0, h1, h, index, temp_lapse_rate)
    precip_cur = computeP(precip0, precip1, h0, h1, h, index, precip_decay_rate, precip_thresh_height)

    return [temp_cur, precip_cur]


def computeT(temp0, temp1, h0, h1, h, index, temp_lapse_rate):
    T0_sl = applyLapseRateT(temp0, h0, 0.0, temp_lapse_rate)
    T1_sl = applyLapseRateT(temp1, h1, 0.0, temp_lapse_rate)
    T_sl = (T1_sl - T0_sl) * index + T0_sl
    T = applyLapseRateT(T_sl, 0.0, h, temp_lapse_rate);

    return T


def computeP(precip0, precip1, h0, h1, h, index, precip_decay_rate, precip_thresh_height):
    P = applyLapseRateP((precip0 + (precip1 - precip0) * index), 0.0, h, precip_decay_rate, precip_thresh_height) # href is ignored anyway

    P[P < 0.0] = 0.0

    return P

def applyLapseRateT(T, h_ref, h, temp_lapse_rate):
    result = T - temp_lapse_rate * (h - h_ref)

    return result

def applyLapseRateP(P, h_ref, h, precip_decay_rate, precip_thresh_height):
    delta_h = h - precip_thresh_height
    delta_h[delta_h < 0.0] = 0.0

    result = P * np.exp(-1.0 * precip_decay_rate * delta_h)

    return result