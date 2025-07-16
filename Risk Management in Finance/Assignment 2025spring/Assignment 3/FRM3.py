import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def xls2csv():
    data = pd.read_excel('./NASDAQ.xlsx', sheet_name='Sheet1', index_col='Date')
    data.sort_index(inplace=True)

    close = data['NASDAQ Close'].values
    daily_return = close[1:] / close[:-1] - 1
    daily_return = np.array([0, *daily_return])
    data['return'] = daily_return
    data.to_csv('./NASDAQ.csv')
   
def historical_simulation():
    data = pd.read_csv('./NASDAQ.csv', index_col='Date')
    Return = data['return'].copy().iloc[1:]
    Return = Return.sort_values().to_numpy()
    print(f"VaR by historical simulation: {-Return[14] * 1e7:.02f}")
    print(f"ES by historical simulation: {-np.mean(Return[:15]) * 1e7:.02f}")
    print()
    # plt.hist(-Return, bins=50)
    # plt.axvline(-Return[14], c='r')
    # plt.xlabel("percentage")
    # plt.ylabel("quantity")
    # # plt.title("Daily Loss Rate Distribution")
    # plt.show()

def exponential_weighting():
    data = pd.read_csv('./NASDAQ.csv', index_col='Date')
    Return = data['return'].copy()
    Return = Return.iloc[1:] * 1e7

    lambda_ = 0.995
    n = len(Return)
    idx = np.arange(n)
    weight = lambda_**(n-idx) * (1 - lambda_) / (1 - lambda_**n)
    weightedReturn = pd.DataFrame({'return':Return, 'weight':weight}, index=Return.index)
    weightedReturn.sort_values('return', inplace=True)
    cumulated_weight = 0
    for i in range(n):
        cumulated_weight += weightedReturn.iloc[i, 1]
        if cumulated_weight > 0.01:
            idx = i
            break

    return_times_weight = weightedReturn['return'] * weightedReturn['weight']
    print(f"weights cumulated to 0.01 at {idx}th scenario")
    print(f"VaR by exponential weighting: {-weightedReturn.iloc[idx, 0]:.02f}")
    print(f"ES by exponential weighting: {-np.sum(weightedReturn.iloc[:idx+1, 0] * weightedReturn.iloc[:idx+1, 1])/0.01:.02f}")
    print()

def volatility_updating():
    data = pd.read_csv('./NASDAQ.csv', index_col='Date')
    Return = data['return'].copy()
    EWMA_sigma = np.empty(len(Return) - 1)
    EWMA_sigma[0] = Return.std()**2
    for i in range(1, len(Return) - 1):
        EWMA_sigma[i] = 0.94 * EWMA_sigma[i-1] + 0.06 * Return.iloc[i]**2
    EWMA_sigma = np.sqrt(EWMA_sigma)
    sigma_n = EWMA_sigma[-1]
    adjusted_return = Return[1:] * (sigma_n / EWMA_sigma)

    adjusted_return = np.sort(adjusted_return)
    VaR = -adjusted_return[14] * 1e7
    ES = -np.mean(adjusted_return[:15]) * 1e7
    print(f"max vol is {EWMA_sigma.max() * 100:.02f}%, and the min vol is {EWMA_sigma.min() * 100:.02f}%")
    print(f"the volatility of the stock at 2006-3-10 is {sigma_n * 100:.02f}%")
    print(f"VaR by volatility-updating: {VaR:.02f}")
    print(f"ES by volatility-updating: {ES:.02f}")
    print()
    # plt.plot(EWMA_sigma)
    # plt.xlabel("Date No.")
    # plt.ylabel("Volatility Estimated by EWMA")
    # plt.show()

def normal_distribution():
    data = pd.read_csv('./NASDAQ.csv', index_col='Date')
    Return = data['return'].copy()
    Return = Return.iloc[1:]

    norm_pdf = lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi)
    sigma = Return.std()
    VaR = sigma * 2.326 * 1e7# N^{-1}(0.99) aproximately equals to 2.326
    ES = sigma * norm_pdf(2.326) * 100 * 1e7
    print(f"the volatility of returns is {sigma * 100:.02f}%")
    print(f"VaR by normal distribution: {VaR:.02f}")
    print(f"ES by normal distribution: {ES:.02f}")
    print()

if __name__ == "__main__":
    # data preprocess
    try:
        xls2csv()                                             #请在运行时将这一行解除注释
    except FileNotFoundError as e:
        print('FileNotFoundError: ', e)
        print("请将NASDAQ.xls文件置于代码所在文件夹内（注意Excel文件名后缀）")
        exit(1)

    # Historical Simulation
    historical_simulation()

    # Exponential Weighting
    exponential_weighting()

    # volatility-updating
    volatility_updating()

    # normal distribution
    normal_distribution()