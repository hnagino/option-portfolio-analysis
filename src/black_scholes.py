import numpy as np
from scipy.stats import norm


#define functions 
def black_scholes_price(S, K, T, r, sigma, option_type='call'):

    """ 
    Calculate the theoretical price of a European call or put option using the Black-Scholes formula.
    Parameters: 
        S: Current stock price
        K: Strike price
        T: Time to maturity (in years)
        r: Risk-free interest rate (annualized)
        sigma: Volatility of the underlying stock (annualized)
        option_type: 'call' or 'put'

    Returns:
        Theoretical price of the option

    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        # Calculate call option price
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        # Calculate put option price
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    #end if 

    return price
#function ends here


def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    """ 
    Calculate the Greeks (Delta, Gamma, Vega, Theta, Rho) for a European call or put option using the Black-Scholes formula.
    Parameters: 
        S: Current stock price
        K: Strike price
        T: Time to maturity (in years)
        r: Risk-free interest rate (annualized)
        sigma: Volatility of the underlying stock (annualized)
        option_type: 'call' or 'put'

    Returns:
        A dictionary containing the Greeks (Delta, Gamma, Vega, Theta, Rho)
    
    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01 

    if option_type == 'call':
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) * 0.01
        delta = norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    elif option_type == 'put':
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) * 0.01
        delta = norm.cdf(d1) - 1
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    #end if 
    
    return {
        'Delta': round(delta, 4),
        'Gamma': round(gamma, 4),
        'Vega': round(vega, 4),
        'Theta': round(theta, 4),
        'Rho': round(rho, 4)
    }
#end function


if __name__ == "__main__":
    S = 150
    K = 155
    T = 0.5
    r = 0.05
    sigma = 0.25

    call_price = black_scholes_price(S, K, T, r, sigma, "call")
    put_price = black_scholes_price(S, K, T, r, sigma, "put")

    print(f"Call Price: ${call_price:.4f}")
    print(f"Put Price:  ${put_price:.4f}")

    print("\n--- CALL GREEKS ---")
    call_greeks = black_scholes_greeks(S, K, T, r, sigma, "call")
    for key, value in call_greeks.items():
        print(f"  {key:10}: {value}")

    print("\n--- PUT GREEKS ---")
    put_greeks = black_scholes_greeks(S, K, T, r, sigma, "put")
    for key, value in put_greeks.items():
        print(f"  {key:10}: {value}")