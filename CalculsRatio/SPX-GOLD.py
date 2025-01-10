# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick



# %%
#Not sure about values before 1900, so not using them
start_date = pd.to_datetime('01-01-1900')


# %%
#Historical data downloaded on Stooq https://stooq.com/q/?s=^spx
spx = pd.read_csv('data/spx_d.csv')
spx['Date']=pd.to_datetime(spx['Date'])
spx.set_index('Date',inplace=True)

#Recording last date of data
end_date = spx.index[-1].strftime('%d-%m-%Y')


#Resample Monthly+Calculate Monthly Returns
spx_month = spx[spx.index.date >= start_date.date()].resample(rule="M").first().ffill()[['Close']]

#Calculate Montly Return
spx_month['Monthly Change']=spx_month.Close.pct_change()
spx_month['Cumul Monthly Returns']=(1+spx_month['Monthly Change']).cumprod()

# %%
#Historical data downloaded on Stooq https://stooq.com/q/d/?s=10yusy.b

gold = pd.read_csv('data/xauusd_d.csv')
gold['Date']=pd.to_datetime(gold['Date'])
gold.set_index('Date',inplace=True)

#Resample Monthly+Calculate Monthly Returns
gold_month = gold[gold.index.date >= start_date.date()].resample(rule="M").first().ffill()[['Close']]
gold_month['Monthly Change']=gold_month.Close.pct_change()
gold_month['Cumul Monthly Returns']=(1+gold_month['Monthly Change']).cumprod()

# %%
#Ratio Base 100 Jan. 1920
gold_month['Ratio']=spx_month['Cumul Monthly Returns']/gold_month['Cumul Monthly Returns']

val_base = gold_month.loc[(gold_month.index.month == 1) & (gold_month.index.year == 1920),'Ratio'].item()
gold_month['Ratio Base 100'] = gold_month['Ratio']/val_base * 100 

# %%
#SMA 7 year = 7*12 = 84 months
gold_month['7SMA'] = gold_month['Ratio Base 100'].rolling(window=84).mean()

# %%
fig = plt.figure(figsize = (10, 6),dpi=100)

df = gold_month[gold_month.index.year>=1920]

labels = df.index.values
data1 = df['Ratio Base 100'].values
data2 = df['7SMA'].values
alpha = 1

ax = fig.add_subplot(111)

ax.plot(
    labels,
    data1,
    color="#4169E1",
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
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(base=10))

plt.legend()
plt.title(f"Ratio SP500 / Gold - Dividendes Non Réinvestis\n Date du graph : {end_date}",size=15)

plt.grid(True, linestyle ='--')

plt.figtext(0.10, 0.01, "Base 100 au 01/01/1920", ha="center",fontsize=10,style="italic")

plt.show()


# %%


# %%



