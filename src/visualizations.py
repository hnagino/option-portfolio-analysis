import matplotlib.pyplot as plt
import numpy as np


def plot_portfolio_payoff(stock_prices, payoff, title='Portfolio Payoff at Expiration'):
    """ 
    Function: plot the payoff of an option portfolio at expiration.
    
    Parameters:
        stock_prices: array of possible stock prices at expiration
        payoff: array of corresponding payoffs for the input stock prices
        title: title of the plot

    """

    stock_prices = np.array(stock_prices)
    payoff = np.array(payoff)

    plt.figure(figsize=(10, 6))
    plt.plot(stock_prices, payoff, label='Portfolio Payoff', color='blue')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.title(title)
    plt.xlabel('Stock Price at Expiration')
    plt.ylabel('Profit / Loss at Expiration')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_price_comparison(methods, prices, title='Option Price Comparison'):
    """ 
    Function: plot a comparison of option prices from different methods.
    
    Parameters:
        methods: list of method names (e.g., ['Black-Scholes', 'Monte Carlo'])
        prices: list of corresponding option prices for each method
        title: title of the plot

    """
    if len(methods) != len(prices):
        raise ValueError("Length of methods and prices must be the same")

    plt.figure(figsize=(8, 5))
    plt.bar(methods, prices)
    plt.title(title)
    plt.ylabel('Option Price')
    plt.grid(axis='y', linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()