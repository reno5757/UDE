# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick


# %%
#Historical data downloaded on Yahoo Finance S&P 500 (TR) (^SP500TR)
TRspx = pd.read_csv('data/SP500TRsince1988.csv')
TRspx['Date']=pd.to_datetime(TRspx['Date'])
TRspx.set_index('Date',inplace=True)

#Recording last date of data
end_date = TRspx.index[-1].strftime('%d-%m-%Y')

#First day of data
start_date = TRspx.index[0]


# %%
#Historical data downloaded on Stooq https://stooq.com/q/d/?s=10yusy.b

gold = pd.read_csv('data/xauusd_d.csv')
gold['Date']=pd.to_datetime(gold['Date'])
gold.set_index('Date',inplace=True)

gold=gold[gold.index>=start_date].copy()

# %%
#Ratio Base 100 Janv 1988 (no data for SP500 Gross Return Before)
TRspx['Ratio']=TRspx['Close']/gold['Close']

val_base = TRspx.loc[(TRspx.index.month == 1) & (TRspx.index.year == 1988),'Ratio'].head(1).item()
TRspx['Ratio Base 100'] = TRspx['Ratio']/val_base * 100 
TRspx['Ratio Base 100'].ffill(inplace=True)

# %%
#SMA 7 year = 7*252 = 1764 days
TRspx['7SMA'] = TRspx['Ratio Base 100'].rolling(1764).mean()

# %%
TRspx

# %%
fig = plt.figure(figsize = (10, 6),dpi=100)

df = TRspx[TRspx.index.year>=1980]

labels = df.index.values
data1 = df['Ratio Base 100'].values
data2 = df['7SMA'].values
alpha = 1

ax = fig.add_subplot(111)

ax.plot(
    labels,
    data1,
    color="#339eff",
    alpha = alpha,
    linewidth=2,
    label="SP500 / Gold")


ax.plot(
    labels,
    data2,
    color="#D70040",
    alpha = alpha,
    linewidth=2,
    label="MM 7 ans")

ax.set_yscale('log')
ax.set_yticks(ticks=[25,50,100,200,400,800,1600],labels=[25,50,100,200,400,800,1600])
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(base=5))

plt.legend()
plt.title(f"Ratio SP500 / Gold - Dividendes Réinvestis\n Date du graph : {end_date}",size=15)

plt.grid(True, linestyle ='--')

plt.figtext(0.10, 0.01, "Base 100 au 04/01/1988", ha="center",fontsize=10,style="italic")


plt.show()


# %%


# %%



