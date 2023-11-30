import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl
import pandas as pd 
import geopandas as gpd 
import os
from pathlib import Path

PATH = Path(__file__).parent
ROOT = os.path.abspath(__file__ + '/../../')

# Read in results
results_dir = os.path.join(ROOT, "src/Ethanol_Plants.csv")
df2 = pd.read_csv(results_dir)

# Convert lat, long to numeric values
df2["Latitude"] = pd.to_numeric(df2["Latitude"], errors='coerce')
df2["Longitude"] = pd.to_numeric(df2["Longitude"], errors='coerce')
df2.head()

# Get the max and min LCOH for the run
min = df2.loc[df2["Cap_Mmgal"].idxmin()]

max = df2.loc[df2["Cap_Mmgal"].idxmax()]

#print(min)
#Site: {min['Ethanol Site']}
min_info = f'''Min Prod.: {min["Cap_Mmgal"]:.0f} Mmgal
  State: {min["State"]}
  Latitude: {min["Latitude"]:.2f}
  Longitude: {min["Longitude"]:.2f}'''

max_info = f'''Max Prod.: {max["Cap_Mmgal"]:.0f} Mmgal
  State: {max["State"]}
  Latitude: {max["Latitude"]:.2f}
  Longitude: {max["Longitude"]:.2f}'''

# Create shape points for ploting using geopandas
df_geo = gpd.GeoDataFrame(df2, 
            geometry = gpd.points_from_xy(
                    df2.Longitude,
                    df2.Latitude
            ))

# Read in base map (United States)
path = os.path.join(ROOT, "post-process/tl_2022_us_state.shp")
df = gpd.read_file(path, crs=4326)
df.crs
fig, ax = plt.subplots(figsize=[9,9])

# Reduce map to continental US
non_continental = ['HI','VI','MP','GU','AK','AS','PR']
us49 = df
for n in non_continental:
    us49 = us49[us49.STUSPS != n]

cmap = (mpl.colors.ListedColormap(['royalblue','lightblue','chartreuse','yellow','gold','orange','orangered'])\
        .with_extremes(over='red', under='blue'))
bounds = [5,6,7,10,11,12,15,20]
bounds = np.linspace(1,400, 8)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=[24,24])
us49.boundary.plot(ax=ax, alpha=0.5, edgecolor='k')
sc = ax.scatter(x=df_geo['Longitude'],y=df_geo['Latitude'], 
                #s=50,
                c=df_geo['Cap_Mmgal'],
                cmap=cmap,
                norm=norm,
                #vmin=4.5, vmax=15 #Use to modify colorbar range
                )
mpl.rcParams.update({'font.size': 22})


plt.colorbar(sc,
             extend='both',
             orientation='horizontal',
             label='Cap_Mmgal',
             pad=0.05)

fig.savefig(ROOT+'/src/figures/capacity_map_discrete.png',dpi=200,bbox_inches='tight')

cmap2 = mpl.cm.jet
#norm2 = mpl.colors.Normalize(vmin=5, vmax=20)
norm2 = mpl.colors.CenteredNorm(vcenter=200)

fig2, ax2 = plt.subplots(figsize=[24,24])
us49.boundary.plot(ax=ax2, alpha=0.5, edgecolor='k')
sc2 = ax2.scatter(x=df_geo['Longitude'],y=df_geo['Latitude'], 
                #s=50,
                c=df_geo['Cap_Mmgal'],
                cmap=cmap2,
                norm=norm2,
                #vmin=4.5, vmax=15 #Use to modify colorbar range
                )
ax2.text(-75,25,min_info, fontsize=20,
        bbox={'facecolor':'lightgray', 'alpha':0.5,'pad':10})
ax2.text(-125,25,max_info, fontsize=20,
        bbox={'facecolor':'lightgray', 'alpha':0.5,'pad':10})
ax2.annotate('Max', xy=(max['Longitude']-.05,max['Latitude']-.05), 
            xytext=(max['Longitude']-2,max['Latitude']-2), fontsize=12,
            bbox={'facecolor':'lightgray', 'alpha':0.5},
            arrowprops=dict(facecolor='black',shrink=0.05))
ax2.annotate('Min', xy=(min['Longitude']-.05,min['Latitude']-.05), 
            xytext=(min['Longitude']-2,min['Latitude']-2), fontsize=12,
            bbox={'facecolor':'lightgray', 'alpha':0.5},
            arrowprops=dict(facecolor='black',shrink=0.05))

plt.colorbar(sc2,
             extend='both',
             orientation='horizontal',
             label='Cap_Mmgal',
             pad=0.05)

mpl.rcParams.update({'font.size': 22})

fig2.savefig(ROOT+'/src/figures/capacity_map_continuous.png',dpi=200,bbox_inches='tight')