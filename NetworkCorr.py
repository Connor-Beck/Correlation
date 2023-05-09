# -*- coding: utf-8 -*-
"""
Finalized May 9 2023

@author: Connor Beck
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats

#Section Used for generating signals to correlate:
#---------------------------------------------------------
#Set signal parameters for simulating sinusoidal wave
class Parameters:
    N=30000  #total step count
    fs=1/0.1   #time step (1/ms)
    Period=5000 #steps
    L=N*fs; #time
    f=1/Period;  #Frequency
    nCycl=N*f;  #Total number of cycles
    
P=Parameters()

#Create sine waves with a small bit of random noise
t=np.linspace(0,P.nCycl/P.f,num=P.N)
t_shift=np.linspace(P.Period/2,P.Period/2+P.N,num=P.N);
x=t/P.fs

randnoise=0.3
randA=np.sin(2*np.pi*P.f*20*t)*randnoise*np.random.rand(P.N)
randB=np.sin(2*np.pi*P.f*20*t_shift)*randnoise*np.random.rand(P.N)

A=np.sin(2*np.pi*P.f*t) + randA;  
B=np.sin(2*np.pi*P.f*t_shift) + randB;
#---------------------------------------------------------------------
#Use function below for correlation
#I ran this with the parameter set before, you can tune this as you please.

class Parameters:
    N=30000  #total step count
    fs=1/0.1   #time step (1/ms)
    Period=5000 #steps
    L=N*fs; #time
    f=1/Period;  #Frequency
        
P=Parameters()

def NetworkCorr(A,B,P):
    
    #Use cross correlation to detect the peak corrlation based on phase shift
    corr = signal.correlate(A, B)
    lags = signal.correlation_lags(len(B), len(A))

    peak_corr=max(corr)
    peak_index=np.where(corr==peak_corr)

    #Compute the phase shift
    if len(peak_index[0])>1:
        print("Multiple correlation peaks")
        peak_t=np.random.randint(0, len(peak_index)+1)
        phase=peak_index[0][peak_t]/Period-N
    else:
        phase=int(peak_index[0]-P.N)
        phase_radians=phase*2*np.pi/P.Period
        phase_degrees=phase*360/P.Period
    
    #create extended arrays with zero padding

    zPad=np.zeros(abs(phase));
    
    A_zPad=np.concatenate((zPad,A,zPad))
    B_zPad=np.concatenate((zPad,B,zPad))
    
    B_rolled=np.roll(B_zPad,phase)

    t_start=abs(phase)+phase
    t_finish=P.N-(abs(phase)+phase)

    t_ext=np.linspace(0,t_finish-t_start,num=(t_finish-t_start))


    A_compressed=A_zPad[t_start:t_finish]
    B_compressed=B_rolled[t_start:t_finish]

    pearsonsR=stats.pearsonr(A_compressed,B_compressed);

        
    return phase,phase_degrees,pearsonsR

  
phase, phase_degrees, pearsonsR = NetworkCorr(A,B,P)
  