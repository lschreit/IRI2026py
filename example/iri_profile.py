#!/usr/bin/env python3
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import iri2026.iri2026 as iri2026

first=True

for ut in np.linspace(0,24,7)[:-1]:

    # Location and time
    lat = 0.0
    lon = 0.0
    dt = datetime.datetime(2024, 5, 15, int(ut), 0, 0)
    
    # Altitude grid [km]
    hmin = 80.0
    hmax = 6000.0
    hstep = 10.0
    
    
    # IRI switches
    jf = np.ones(50, dtype=bool)
    
    for i in [4, 5, 6, 23, 30, 33, 35, 39, 40, 47]:
        jf[i - 1] = False
    
    # COR2
    jf[29 - 1] = True
    jf[30 - 1] = False
    
    # Ozhogin plasmasphere
    jf[49 - 1] = True
    
    # Plasmapause OFF
    jf[50 - 1] = True
    
    
    # IRI date/time format
    year = dt.year
    mmdd = dt.month * 100 + dt.day
    dhour = 25.0 + dt.hour + dt.minute / 60.0
    
    
    # Output arrays
    outf = np.zeros((20, 1000), dtype=np.float32, order="F")
    oar = np.zeros(100, dtype=np.float32, order="F")
    
    
    # Load IRI data
    cwd = os.getcwd()
    os.chdir(os.path.dirname(iri2026.__file__))
    if first:
        iri2026.read_ig_rz()
        iri2026.readapf107()
        first=False
        
    iri2026.iri_sub(
        jf,
        0,
        lat,
        lon,
        year,
        mmdd,
        dhour,
        hmin,
        hmax,
        hstep,
        outf,
        oar,
    )
    
    os.chdir(cwd)
    
    
    # Extract profile
    n = int((hmax - hmin) / hstep) + 1
    
    alt = hmin + np.arange(n) * hstep
    ne = outf[0, :n]          # m^-3
    
    
    # Plot
    # plt.figure(figsize=(7, 9))
    
    plt.semilogx(ne/1e6, alt, lw=2, label=f"UT = {ut}")
    
    plt.xlabel(r"$N_e$ [cm$^{-3}$]")
    plt.ylabel("Altitude [km]")
    plt.grid(True, which="both", alpha=0.3)
    
    plt.tight_layout()
    plt.show()
plt.legend()