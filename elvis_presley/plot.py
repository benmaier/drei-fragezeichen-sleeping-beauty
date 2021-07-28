import simplejson as json
import matplotlib.pyplot as pl
import numpy as np
from collections import Counter
import bfmplot as bp

with open('albums_with_tracks_and_popularities.json','r') as f:
    albums = json.load(f)

T = 1000
dt = 5
bins = np.linspace(0,T,int(T/dt)+1)
observations = [[] for i in range(bins.shape[0]-1) ]

fig, ax = pl.subplots(2,1,figsize=(5,6),sharex=True)

for album in albums:

    t = []
    pop = []

    for i, track in enumerate(album['tracks']):
        pop.append(track['popularity'])
        t.append(track['cum_duration_ms']/1000/60)

    pop = np.array(pop,dtype=float)
    popgauge = Counter(pop[:4]).most_common()[0][0]
    #popgauge = pop[0]
    pop -= popgauge
    t = np.array(t)
    for _t, _p in zip(t, pop):
        b = np.argwhere(_t<bins)[0][0]
        print(b)
        observations[b].append(_p)


    ax[0].plot(t, pop, '.', alpha=0.2, c='#888888')

mean_diff = np.zeros_like(bins)[:-1]
std_diff = np.zeros_like(bins)[:-1]
probability_lower_than_zero = np.zeros_like(bins)[:-1]
for i, obs in enumerate(observations):
    if len(obs)>0:
        mean_diff[i] = np.mean(obs)
    if len(obs)>1:
        std_diff[i] = np.std(obs)
    if len(obs)>6:
        probability_lower_than_zero[i] = np.count_nonzero(np.array(obs)<0)/len(obs)

mbins = 0.5*(bins[1:]+bins[:-1])
#mean_diff[1] = np.nan
#std_diff[1] = np.nan
#probability_lower_than_zero[1] = np.nan

ax[1].plot(mbins,probability_lower_than_zero)
ax[0].errorbar(mbins, mean_diff, std_diff, marker='s',ls='None')

ax[1].set_xlabel('time [min]')
ax[0].set_ylabel('difference of track popularity\nto album popularity') # difference to most common\ntrack popularity on first 12 tracks on album')
ax[1].set_ylabel('probability of track having\nlower popularity than album') # difference to most common\ntrack popularity on first 12 tracks on album')
ax[0].set_xlim([0,120])
#pl.ylim([0.95,1.05])
#ax[0].set_ylim([-2.5,1.5])
ax[1].set_ylim([0,1])
bp.strip_axis(ax[0])
bp.strip_axis(ax[1])



fig.tight_layout()
fig.savefig('popularity_over_time.png',dpi=300)

pl.show()

