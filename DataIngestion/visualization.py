import matplotlib.pylot as plt
import matplotlib.pylot as TwoSlopeNorm
import numpy as np


def heatmap(timestamps, signal, periods_in_hours, coefficients, coi_mask):
    fig, axs = plt.subplots(2,1, sharex=True, gridspec_kw={'height_ratios': [1,3]})
    axs[0].plot(timestamps, signal)

    limit = np.max(np.abs(coefficients))

    axs[1].pcolormesh(timestamps, periods_in_hours, coefficients, cmap = 'RdBu_r', norm=TwoSlopeNorm(vcenter=0), vMin = -1*limit, vMax = limit)
    axs[1].set_yscale('log')
    danger_zone_only = np.ma.masked_where(coi_mask == False, coi_mask)
    axs[1].pcolormesh(timestamps, periods_in_hours, danger_zone_only, 
              cmap='gray', shading='auto', alpha=0.6)
    
    fig.set_title("CS2 Momentum CWT with COI Blackout")
    fig.set_xlabel("Time (Hours)")
    fig.set_ylabel("Wavelet Width (Hours)")

    axs.set_ylim(periods_in_hours.max(), periods_in_hours.min())
    plt.show()
    

