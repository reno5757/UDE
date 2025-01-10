# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick
import yfinance as yf



# %%
def monthly_return_based_on_yield(yield_p_month,yield_month,maturity):
     Total_Return = yield_p_month/12 + (yield_p_month/yield_month)*(1-1/((1+yield_month/2)**(2*(maturity-1/12))))+1/((1+yield_month/2)**(2*(maturity-1/12)))-1
     return Total_Return

#Formule provenant de : 
#https://doi.org/10.25397/eur.8152748
#https://doi.org/10.3390/data4030091


# %%
#Not sure about values before 1950, so not using them
start_date = pd.to_datetime('01-01-1950')


# %%
#Historical data downloaded on YFinance CBOE Interest Rate 10 Year T No (^TNX)
tenY = pd.read_csv('data/10ysince1962.csv')
tenY['Date']=pd.to_datetime(tenY['Date'])
tenY.set_index('Date',inplace=True)

#Recording last date of data
end_date = tenY.index[-1].strftime('%d-%m-%Y')


#Resample Monthly
tenY_month = tenY[tenY.index.date >= start_date.date()].resample(rule="M").first().ffill()[['Close']]
tenY_month['PValue']=tenY_month['Close'].shift(1)

#Calculate Montly Return
tenY_month['Monthly Return'] = tenY_month.apply(lambda x: monthly_return_based_on_yield(x['PValue']/100,x['Close']/100, 10), axis=1)
tenY_month['Cumul Monthly Returns']=(1+tenY_month['Monthly Return']).cumprod()


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
#Ratio Base 100 Jan. 1972
gold_month['Ratio']=gold_month['Cumul Monthly Returns']/tenY_month['Cumul Monthly Returns']

val_base = gold_month.loc[(gold_month.index.month == 1) & (gold_month.index.year == 1972),'Ratio'].item()
gold_month['Ratio Base 100'] = gold_month['Ratio']/val_base * 100 

# %%
#SMA 7 year = 7*12 = 84 months
gold_month['7SMA'] = gold_month['Ratio Base 100'].rolling(window=84).mean()

# %%
fig = plt.figure(figsize = (10, 6),dpi=100)

df = gold_month[gold_month.index.year>=1970]

labels = df.index.values
data1 = df['Ratio Base 100'].values
data2 = df['7SMA'].values
alpha = 1

ax = fig.add_subplot(111)

ax.plot(
    labels,
    data1,
    color="#AA4A44",
    alpha = alpha,
    linewidth=3,
    label="Gold / US10Y")


ax.plot(
    labels,
    data2,
    color="#3368ff",

    alpha = alpha,
    linewidth=3,
    label="MM 7 ans")

ax.set_yscale('log')
ax.set_yticks(ticks=[25,50,100,200,400,800,1600],labels=[25,50,100,200,400,800,1600])
ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(base=5))

plt.legend()
plt.title(f"Ratio Gold / US10Y\n Date du graph : {end_date}",size=15)

plt.grid(True, linestyle ='--')
plt.figtext(0.10, 0.01, "Base 100 au 03/01/1972", ha="center",fontsize=10,style="italic")


plt.show()


# %%


# %%



