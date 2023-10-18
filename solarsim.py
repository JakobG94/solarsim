#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 12:51:57 2023

@author: jakob
"""

import rebound
from matplotlib import pyplot as plt
#import numpy as np


eccentricity = [0.0, 0.2, 0.5]
timestep = [0.1, 0.05, 0.01]
k=0.01720209895

Time = 365.25*100


for i in eccentricity:
    for j in timestep:
        
        sim = rebound.Simulation()
        sim.G=k*k
        sim.add(m=1.)
        sim.add(m=3e-6, a=1., e=i)
        sim.integrator='leapfrog'
        sim.dt=j
        sim.move_to_com()
        
        Angular_Momentum = []
        Energy = []
        time = []
        n = 0
        
        
        while n < Time:
            
            #print(sim.t)
            sim.step()
            
            temp = sim.angular_momentum()
            
            Angular_Momentum.append(temp[2])
            Energy.append(sim.energy())
            time.append(sim.t)
            
            n = n + sim.dt
            
        
        if i > 0:
            op=rebound.OrbitPlot(sim, unitlabel='[AU]', color=True, periastron=True)
        else:
            op=rebound.OrbitPlot(sim, unitlabel='[AU]', color=True, periastron=False)
        
        op.fig.savefig('Orbit_e=' + str(i) + '_dt=' + str(j) + '.png')
        
        Energy_upper_lim = 2*max(Energy)-min(Energy)
        Energy_lower_lim = 2*min(Energy)-max(Energy)

        
        plt.figure()
        plt.plot(time, Angular_Momentum)
        plt.title('Angular Momentum with e=' + str(i) + ' and dt=' + str(j))
        plt.yscale('log')
        plt.xlabel('Time [days]')
        plt.ylabel('Angular Momentum')
        plt.savefig('Angular_Momentum_e=' + str(i) + ' and dt=' + str(j) + '.png')
        plt.show()
        
        plt.figure()
        plt.plot(time, Energy)
        plt.title('Energy with e=' + str(i) + 
                  ', dt=' + str(j) + 
                  ', and a difference between \n highest and lowest Energy of dE=' +
                  str(max(Energy) - min(Energy))[:5] +
                  str(max(Energy) - min(Energy))[-4:])       
        plt.xlabel('Time [days]')
        plt.ylim((Energy_lower_lim, Energy_upper_lim))
        plt.ylabel('Energy')
        plt.savefig('Energy_e=' + str(i) + ' and dt=' + str(j) + '.png')
        plt.show()
        
        for p in sim.particles:
            if p.m < 1:
                print(p.calculate_orbit())



