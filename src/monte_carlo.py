import numpy as np 


#define functions 
def monte_carlo_option_price(S, K, T, r, sigma, option_type='call', n_simulations=100000, n_trading_days=252):
    """ 
    Price a European call or put option using Monte Carlo simulation.
    
    Parameters: 
        S: Current stock price
        K: Strike price
        T: Time to maturity (in years)
        r: Risk-free interest rate (annualized)
        sigma: Volatility of the underlying stock 
        option_type: 'call' or 'put'
        num_simulations: Number of Monte Carlo simulations to run
        n_trading_days: Number of trading days in a year (currently set to 252)
    Returns: 
        price: Estimated option price
    """
    dt = T / n_trading_days  # Time step
    random_shocks = np.random.standard_normal((n_simulations, n_trading_days))  # Generate random shocks

    drift = (r - 0.5 * sigma ** 2) * dt
    shock = sigma * np.sqrt(dt) * random_shocks
    daily_returns = np.exp(drift + shock)  
    price_paths = S * np.cumprod(daily_returns, axis = 1)

    final_prices = price_paths[:, -1] # only the last column 

    if option_type == "call":
        payoffs = np.maximum(final_prices - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - final_prices, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    #discount the average payoff back to present value
    price = np.exp(-r * T) * np.mean(payoffs)
    return price


if __name__ == "__main__":
    S = 150
    K = 155
    T = 0.5
    r = 0.05
    sigma = 0.25

    call_price = monte_carlo_option_price(S, K, T, r, sigma, "call")
    put_price = monte_carlo_option_price(S, K, T, r, sigma, "put")

    print("=" * 45)
    print("     MONTE CARLO OPTION PRICING")
    print("=" * 45)
    print(f"  Simulations       : 100,000")
    print(f"  Time Steps        : 252 trading days")
    print("-" * 45)
    print(f"  Call Price (MC)   : ${call_price:.4f}")
    print(f"  Put Price  (MC)   : ${put_price:.4f}")
    print("-" * 45)
    print(f"  Call Price (BS)   : $10.0299")
    print(f"  Put Price  (BS)   : $11.2029")
    print("=" * 45)