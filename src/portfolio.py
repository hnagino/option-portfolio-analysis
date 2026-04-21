import numpy as np 


class OptionPosition: 

    """
    represent single option position in a portfolio

    Class attributes:
        option_type: 'call' or 'put'
        strike_price: strike price of the option
        premium: premium paid for the option
        time_to_maturity: time to maturity in years
        quantity: number of contracts (positive for long, negative for short)

    """

    def __init__(self, option_type, strike_price, premium, time_to_maturity, quantity=1):
        if option_type not in ['call', 'put']:
            raise ValueError("option_type must be 'call' or 'put'")
        if strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if premium < 0:
            raise ValueError("Premium cannot be negative")
        if time_to_maturity <= 0:
            raise ValueError("Time to maturity must be positive")
        if quantity == 0:
            raise ValueError("Quantity cannot be zero")
        
        self.option_type = option_type
        self.strike_price = strike_price
        self.premium = premium
        self.time_to_maturity = time_to_maturity
        self.quantity = quantity

    def __repr__(self):
        if self.quantity > 0:
            position_type = 'Long'
        else:            
            position_type = 'Short'
        return (
            f"{position_type} {abs(self.quantity)} {self.option_type.upper()} "
            f"@ {self.strike_price} "
            f"(Premium: {self.premium}, Time to Maturity: {self.time_to_maturity} years)"
        )
    
    def payoff_at_expiration(self, stock_prices):
        """ 
        
        Calculate the payoff at expiration 
        
        Parameters:
            stock_prices: array of possible stock prices at expiration
            
        Returns:
            Array of payoffs corresponding to the input stock prices

        """

        stock_prices = np.array(stock_prices)

        if self.option_type == 'call':
            intrinsic_value = np.maximum(stock_prices - self.strike_price, 0)
        else:  
            intrinsic_value = np.maximum(self.strike_price - stock_prices, 0)

        total_payoff = self.quantity * (intrinsic_value - self.premium)
        return total_payoff
    


class OptionPortfolio:
    """
    Represents a portfolio of option positions
    
    Attributes:
        positions: list of OptionPosition objects

    """

    def __init__(self,positions=None):
        if positions is None:
            positions = []
        for position in positions:
            if not isinstance(position, OptionPosition):
                raise TypeError("All positions must be OptionPosition instances")
        self.positions = positions

    def add_position(self,position):
        if not isinstance(position, OptionPosition):
            raise TypeError("position must be an instance of OptionPosition")
        self.positions.append(position)

    def total_payoff(self, stock_prices):
        stock_prices = np.array(stock_prices)
        total_payoff = np.zeros_like(stock_prices, dtype=float)
        
        for position in self.positions:
            total_payoff += position.payoff_at_expiration(stock_prices)
        
        return total_payoff
    
    def summary(self):
        opt_lines = ["Option Portfolio Summary:"]
        for pos in self.positions:
            opt_lines.append(str(pos))
        return "\n".join(opt_lines)

