# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick


# %%
#Source https://www.imf.org/external/datamapper/PPPEX@WEO/OEMDC/ADVEC/WEOWORLD/JPN
#Historical Data Parité Pouvoir Achat Japon
dfPPP = pd.read_csv('data/imf-dm-export-20241018.csv',sep=',',index_col=0)
dfPPP=dfPPP.T
dfPPP.index = dfPPP.index.astype(int)


# %%
#Historical Data USDJPY Hebdo

df_usdjpy = pd.read_csv('data/usdjpy_w.csv')
df_usdjpy['Date'] = pd.to_datetime(df_usdjpy['Date'])
df_usdjpy.set_index('Date',inplace=True)


# %%
#Insertion de la valeur de la parité des pouvoir d'achat dans le dataframe USDJPY
df_usdjpy['PPP Val'] = np.NaN

for date in df_usdjpy.index:
    year_to_consider = date.year
    if (year_to_consider >= dfPPP.index[0]) & (year_to_consider <= dfPPP.index[-1]): 
        PPP_Val = dfPPP.loc[year_to_consider,'Japan'].item()
        df_usdjpy.loc[date, 'PPP Val' ]=PPP_Val

df_usdjpy.dropna(inplace=True)    

# %%
#On calcule l'écart en valeur absolue entre le taux de change et le taux éguivalent à la partité des pouvoir d'achat
df_usdjpy['Abs Var to PPP'] = df_usdjpy['Close']-df_usdjpy['PPP Val']

#La distribution des écart est normale, donc on peut calculer la médianne et l'écart type, et centrer les sur la médiane
median_abs_var = df_usdjpy['Abs Var to PPP'].median()
std_abs_var = df_usdjpy['Abs Var to PPP'].std()
df_usdjpy['Abs Var to PPP Centered']=df_usdjpy['Abs Var to PPP']-median_abs_var


# %%

fig = plt.figure(figsize = (10, 6),dpi=100)

labels = df_usdjpy.index.values
data1 = df_usdjpy['Abs Var to PPP Centered']
alpha = 1

ax = fig.add_subplot(111)

ax.plot(
    labels,
    data1,
    color="#36454F",
    alpha = alpha,
    linewidth=2,
    )


ax.axhline(y=0,color = '#7393B3',linewidth=4)
ax.axhspan(ymin=std_abs_var, ymax=-std_abs_var, facecolor="#7393B3", alpha=0.5)

ax.set_yticks(ticks=np.arange(-75,125,25),labels=np.arange(-75,125,25))
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(base=5))

plt.title(f"Parité Pouvoir d'achat JPY/USD\n Date du graph : 18-10-2024",size=15)

plt.grid(True, linestyle ='--')


plt.show()



