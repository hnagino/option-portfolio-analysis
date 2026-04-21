import numpy as np

from src.black_scholes import black_scholes_price, black_scholes_greeks  
from src.monte_carlo import monte_carlo_option_price
from src.portfolio import OptionPosition, OptionPortfolio
from src.visualizations import plot_portfolio_payoff, plot_price_comparison

def get_float_input(prompt, min_value=None): 
    while True:
        try: 
            value = float(input(prompt))
            if min_value is not None and value <= min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    


def get_option_type_input():
    while True:
        option_type = input("Enter option type ('call' or 'put'): ").strip().lower()
        if option_type in ['call', 'put']:
            return option_type
        else:
            print("Invalid input. Please enter 'call' or 'put'.")


def get_strategy_choice():
    """
    Prompt user to choose an example strategy.
    """
    print("\nChoose a portfolio strategy:")
    print("1. Bull Call Spread")
    print("2. Long Straddle")
    print("3. Single Option Position")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def build_strategy(choice, T):
    """
    Build an example option portfolio based on the user's strategy choice.
    """
    if choice == "1":
        print("\n--- Building Bull Call Spread ---")
        long_strike = get_float_input("Enter long call strike price: ", min_value=0)
        long_premium = get_float_input("Enter long call premium: ", min_value=-1)

        short_strike = get_float_input("Enter short call strike price: ", min_value=0)
        short_premium = get_float_input("Enter short call premium: ", min_value=-1)

        long_call = OptionPosition(
            option_type="call",
            strike_price=long_strike,
            premium=long_premium,
            time_to_maturity=T,
            quantity=1
        )

        short_call = OptionPosition(
            option_type="call",
            strike_price=short_strike,
            premium=short_premium,
            time_to_maturity=T,
            quantity=-1
        )

        return OptionPortfolio([long_call, short_call]), "Bull Call Spread"

    elif choice == "2":
        print("\n--- Building Long Straddle ---")
        strike = get_float_input("Enter strike price for both call and put: ", min_value=0)
        call_premium = get_float_input("Enter call premium: ", min_value=-1)
        put_premium = get_float_input("Enter put premium: ", min_value=-1)

        call_position = OptionPosition(
            option_type="call",
            strike_price=strike,
            premium=call_premium,
            time_to_maturity=T,
            quantity=1
        )

        put_position = OptionPosition(
            option_type="put",
            strike_price=strike,
            premium=put_premium,
            time_to_maturity=T,
            quantity=1
        )

        return OptionPortfolio([call_position, put_position]), "Long Straddle"

    else:
        print("\n--- Building Single Option Position ---")
        option_type = get_option_type()
        strike = get_float_input("Enter strike price: ", min_value=0)
        premium = get_float_input("Enter premium: ", min_value=-1)
        quantity = int(get_float_input("Enter quantity (positive for long, negative for short): "))

        position = OptionPosition(
            option_type=option_type,
            strike_price=strike,
            premium=premium,
            time_to_maturity=T,
            quantity=quantity
        )

        return OptionPortfolio([position]), "Single Option Position"



def main():
    double_line = "=" * 60
    single_line = "-" * 60
    print(double_line)
    print(f"|{'Option Pricing Summary':^58}|")
    print(double_line)


    # Market and option input 

    S = get_float_input("Enter current stock price (S): ", min_value=0)
    K = get_float_input("Enter strike price (K): ", min_value=0)    
    T = get_float_input("Enter time to maturity in years (T): ", min_value=0)
    r = get_float_input("Enter risk-free interest rate (r) as a decimal (e.g., 0.05 for 5%): ", min_value=-1)
    sigma = get_float_input("Enter volatility (sigma) as a decimal (e.g., 0.2 for 20%): ", min_value=0)
    option_type = get_option_type_input()

    # Price the option using Black-Scholes and Monte Carlo methods

    bs_price = black_scholes_price(S, K, T, r, sigma, option_type=option_type)
    mc_price = monte_carlo_option_price(S, K, T, r, sigma, option_type=option_type)
    option_greeks = black_scholes_greeks(S, K, T, r, sigma, option_type=option_type)


    # Print visual pricing summary 

    print(double_line)
    print(f"|{'Option Pricing Summary':^58}|")
    print(double_line)

    print("\nSingle Option Pricing Results ")
    print(single_line)
    print(f"|{'Option Type':<20}|{option_type.upper():>37}|")
    print(f"|{'Black-Scholes Price':<20}|${bs_price:>36.4f}|")
    print(f"|{'Monte Carlo Price':<20}|${mc_price:>36.4f}|")
    print(single_line)

    print("\nGreeks for the Option")
    print(single_line)
    for greek, value in option_greeks.items():
        print(f"|{greek:<20}|{value:>37}|")
    print(double_line)

    #build sample strategy

    strategy_choice = get_strategy_choice()
    portfolio, strategy_name = build_strategy(strategy_choice, T)

    print("\n" + portfolio.summary())


    #generate payoff profile 
    stock_price_range = np.linspace(0.5 * S, 1.5 * S, 200)
    portfolio_payoff = portfolio.total_payoff(stock_price_range)


    #Visualizations

    plot_portfolio_payoff(
        stock_prices=stock_price_range,
        payoff=portfolio_payoff,
        title=f"{strategy_name} Profit / Loss at Expiration"
    )

    plot_price_comparison(
        methods=["Black-Scholes", "Monte Carlo"],
        prices=[bs_price, mc_price],
        title=f"{option_type.capitalize()} Option Price Comparison"
    )


if __name__ == "__main__":
    main()