from __future__ import annotations

from typing import Iterable, Sequence, Union, List, Dict, Tuple
from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("Calculator")

Number = Union[int, float]

# Basic arithmetic operations
@mcp.tool()
async def add(a: Number, b: Number, c: Number = 0, d: Number = 0, e: Number = 0) -> float:
    """Return the sum of up to 5 values.

    Args:
        a: First value (required).
        b: Second value (required).
        c: Third value (optional, default 0).
        d: Fourth value (optional, default 0).
        e: Fifth value (optional, default 0).

    Returns:
        The arithmetic sum of the supplied numbers as float.

    Example:
        >>> add(1, 2, 3)
        6.0
    """
    return float(a + b + c + d + e)


@mcp.tool()
async def subtract(minuend: Number, subtrahend: Number, additional1: Number = 0, 
                  additional2: Number = 0, additional3: Number = 0) -> float:
    """Subtract values from minuend sequentially.

    Args:
        minuend: The initial value.
        subtrahend: First value to subtract from minuend.
        additional1: Second value to subtract (optional, default 0).
        additional2: Third value to subtract (optional, default 0).
        additional3: Fourth value to subtract (optional, default 0).

    Returns:
        Result of the subtraction as float.

    Example:
        >>> subtract(10, 3, 2)
        5.0  # 10 - 3 - 2
    """
    result = float(minuend - subtrahend - additional1 - additional2 - additional3)
    return result


@mcp.tool()
async def multiply(a: Number, b: Number, c: Number = 1, d: Number = 1, e: Number = 1) -> float:
    """Return the product of up to 5 values.

    Args:
        a: First value (required).
        b: Second value (required).
        c: Third value (optional, default 1).
        d: Fourth value (optional, default 1).
        e: Fifth value (optional, default 1).

    Returns:
        Product as float.

    Example:
        >>> multiply(2, 3, 4)
        24.0
    """
    return float(a * b * c * d * e)


@mcp.tool()
async def divide(dividend: Number, divisor: Number) -> float:
    """Divide dividend by divisor.

    Args:
        dividend: Numerator.
        divisor: Denominator.

    Returns:
        Quotient as float.

    Raises:
        ZeroDivisionError: If divisor is zero.

    Example:
        >>> divide(10, 2)
        5.0
    """
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return float(dividend) / divisor


@mcp.tool()
async def power(base: Number, exponent: Number) -> float:
    """Calculate base raised to the power of exponent.

    Args:
        base: The base number.
        exponent: The power to raise the base to.

    Returns:
        Result of base^exponent as float.

    Example:
        >>> power(2, 3)
        8.0
    """
    return float(base ** exponent)


# Statistical operations
@mcp.tool()
async def percentage(part: Number, whole: Number, precision: int = 4) -> float:
    """Calculate what percentage part is of whole.

    Args:
        part: The subset value.
        whole: The total value.
        precision: Number of decimal places to round to (default: 4).

    Returns:
        Percentage value (0-100) rounded to precision decimal places.

    Example:
        >>> percentage(25, 200)
        12.5
    """
    if whole == 0:
        raise ZeroDivisionError("Whole cannot be zero when calculating percentage")
    pct = (part / whole) * 100
    return round(pct, precision)


@mcp.tool()
async def percentage_change(old: Number, new: Number, precision: int = 4) -> float:
    """Compute the percentage change from old to new value.

    Args:
        old: The initial value.
        new: The updated value.
        precision: Decimal places for rounding.

    Returns:
        Percentage change. Positive for increase, negative for decrease.

    Example:
        >>> percentage_change(100, 120)
        20.0
    """
    if old == 0:
        raise ZeroDivisionError("Old value cannot be zero when calculating percentage change")
    change = ((new - old) / old) * 100
    return round(change, precision)


@mcp.tool()
async def average_two(value1: Number, value2: Number, precision: int = 4) -> float:
    """Return the arithmetic mean of two values.

    Args:
        value1: First value.
        value2: Second value.
        precision: Decimal places for rounding.

    Returns:
        Average value rounded to precision places.

    Example:
        >>> average_two(10, 20)
        15.0
    """
    return round((value1 + value2) / 2, precision)


@mcp.tool()
async def average_three(value1: Number, value2: Number, value3: Number, precision: int = 4) -> float:
    """Return the arithmetic mean of three values.

    Args:
        value1: First value.
        value2: Second value.
        value3: Third value.
        precision: Decimal places for rounding.

    Returns:
        Average value rounded to precision places.

    Example:
        >>> average_three(10, 20, 30)
        20.0
    """
    return round((value1 + value2 + value3) / 3, precision)


@mcp.tool()
async def average_five(value1: Number, value2: Number, value3: Number, 
                      value4: Number, value5: Number, precision: int = 4) -> float:
    """Return the arithmetic mean of five values.

    Args:
        value1: First value.
        value2: Second value.
        value3: Third value.
        value4: Fourth value.
        value5: Fifth value.
        precision: Decimal places for rounding.

    Returns:
        Average value rounded to precision places.
    """
    return round((value1 + value2 + value3 + value4 + value5) / 5, precision)


@mcp.tool()
async def median_three(value1: Number, value2: Number, value3: Number) -> float:
    """Return the median value of three numbers.

    Args:
        value1: First value.
        value2: Second value.
        value3: Third value.

    Returns:
        The median value as float.

    Example:
        >>> median_three(1, 3, 2)
        2.0
    """
    values = sorted([value1, value2, value3])
    return float(values[1])


@mcp.tool()
async def median_five(value1: Number, value2: Number, value3: Number, 
                     value4: Number, value5: Number) -> float:
    """Return the median value of five numbers.

    Args:
        value1: First value.
        value2: Second value.
        value3: Third value.
        value4: Fourth value.
        value5: Fifth value.

    Returns:
        The median value as float.
    """
    values = sorted([value1, value2, value3, value4, value5])
    return float(values[2])


# Agricultural/Market-specific calculations
@mcp.tool()
async def unit_conversion(value: Number, from_unit: str, to_unit: str, precision: int = 4) -> float:
    """Convert agricultural units commonly used in crop trading.

    Args:
        value: The numeric value to convert.
        from_unit: Source unit.
        to_unit: Target unit.
        precision: Decimal places for rounding.

    Returns:
        Converted value rounded to precision places.

    Supported units: kg, ton, pound, bushel, quintal, cwt (hundredweight)
    """
    # Conversion factors to kg (base unit)
    to_kg = {
        'kg': 1.0,
        'ton': 1000.0,
        'tonne': 1000.0,
        'pound': 0.453592,
        'lb': 0.453592,
        'bushel': 27.216,  # average bushel weight for grains
        'quintal': 100.0,
        'cwt': 50.8023,  # hundredweight
        'gram': 0.001,
        'g': 0.001,
        'ounce': 0.0283495,
        'oz': 0.0283495
    }
    
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    if from_unit_lower not in to_kg or to_unit_lower not in to_kg:
        raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")
    
    # Convert to kg, then to target unit
    kg_value = value * to_kg[from_unit_lower]
    result = kg_value / to_kg[to_unit_lower]
    
    return round(result, precision)


@mcp.tool()
async def price_per_unit(total_price: Number, quantity: Number, precision: int = 4) -> float:
    """Calculate price per unit.

    Args:
        total_price: Total price for the quantity.
        quantity: Quantity of items.
        precision: Decimal places for rounding.

    Returns:
        Price per unit rounded to precision places.

    Example:
        >>> price_per_unit(1000, 50)
        20.0
    """
    if quantity == 0:
        raise ZeroDivisionError("Quantity cannot be zero")
    return round(total_price / quantity, precision)


@mcp.tool()
async def total_cost(price_per_unit: Number, quantity: Number, precision: int = 2) -> float:
    """Calculate total cost given price per unit and quantity.

    Args:
        price_per_unit: Price for one unit.
        quantity: Number of units.
        precision: Decimal places for rounding (default: 2 for currency).

    Returns:
        Total cost rounded to precision places.

    Example:
        >>> total_cost(25.5, 100)
        2550.0
    """
    return round(price_per_unit * quantity, precision)


@mcp.tool()
async def profit_loss_calculation(selling_price: Number, buying_price: Number, 
                                quantity: Number, precision: int = 2) -> Dict[str, float]:
    """Calculate profit or loss for a crop transaction.

    Args:
        selling_price: Price per unit when selling.
        buying_price: Price per unit when buying.
        quantity: Quantity traded.
        precision: Decimal places for rounding.

    Returns:
        Dictionary with total_profit_loss, profit_loss_per_unit, and profit_margin_percentage.

    Example:
        >>> profit_loss_calculation(30, 25, 100)
        {'total_profit_loss': 500.0, 'profit_loss_per_unit': 5.0, 'profit_margin_percentage': 20.0}
    """
    profit_loss_per_unit = round(selling_price - buying_price, precision)
    total_profit_loss = round(profit_loss_per_unit * quantity, precision)
    
    # Calculate profit margin percentage
    if buying_price != 0:
        profit_margin_pct = round(((selling_price - buying_price) / buying_price) * 100, 2)
    else:
        profit_margin_pct = 0.0
    
    return {
        'total_profit_loss': total_profit_loss,
        'profit_loss_per_unit': profit_loss_per_unit,
        'profit_margin_percentage': profit_margin_pct
    }


@mcp.tool()
async def breakeven_price(cost_per_unit: Number, desired_profit_margin: Number, precision: int = 4) -> float:
    """Calculate breakeven selling price given cost and desired profit margin.

    Args:
        cost_per_unit: Cost per unit of the crop.
        desired_profit_margin: Desired profit margin as percentage (e.g., 20 for 20%).
        precision: Decimal places for rounding.

    Returns:
        Minimum selling price to achieve desired profit margin.

    Example:
        >>> breakeven_price(100, 20)
        120.0
    """
    return round(cost_per_unit * (1 + desired_profit_margin / 100), precision)


@mcp.tool()
async def price_range_analysis_three(price1: Number, price2: Number, price3: Number, precision: int = 4) -> Dict[str, float]:
    """Analyze a range of three prices and return statistical summary.

    Args:
        price1: First price value.
        price2: Second price value.
        price3: Third price value.
        precision: Decimal places for rounding.

    Returns:
        Dictionary with min, max, average, median, and price_spread statistics.
    """
    prices = [price1, price2, price3]
    min_price = round(min(prices), precision)
    max_price = round(max(prices), precision)
    avg_price = round(sum(prices) / len(prices), precision)
    median_price = round(sorted(prices)[1], precision)
    price_spread = round(max_price - min_price, precision)
    
    return {
        'min': min_price,
        'max': max_price,
        'average': avg_price,
        'median': median_price,
        'price_spread': price_spread
    }


@mcp.tool()
async def price_range_analysis_five(price1: Number, price2: Number, price3: Number, 
                                   price4: Number, price5: Number, precision: int = 4) -> Dict[str, float]:
    """Analyze a range of five prices and return statistical summary.

    Args:
        price1: First price value.
        price2: Second price value.
        price3: Third price value.
        price4: Fourth price value.
        price5: Fifth price value.
        precision: Decimal places for rounding.

    Returns:
        Dictionary with min, max, average, median, and price_spread statistics.
    """
    prices = [price1, price2, price3, price4, price5]
    min_price = round(min(prices), precision)
    max_price = round(max(prices), precision)
    avg_price = round(sum(prices) / len(prices), precision)
    median_price = round(sorted(prices)[2], precision)  # Middle element for 5 values
    price_spread = round(max_price - min_price, precision)
    
    return {
        'min': min_price,
        'max': max_price,
        'average': avg_price,
        'median': median_price,
        'price_spread': price_spread
    }


@mcp.tool()
async def compound_interest(principal: Number, rate: Number, time: Number, 
                          compounding_frequency: int = 1, precision: int = 2) -> float:
    """Calculate compound interest (useful for storage cost calculations).

    Args:
        principal: Initial amount.
        rate: Interest rate as percentage (e.g., 5 for 5%).
        time: Time period.
        compounding_frequency: How many times interest is compounded per time period.
        precision: Decimal places for rounding.

    Returns:
        Final amount after compound interest.

    Example:
        >>> compound_interest(1000, 5, 2, 12)
        1104.89
    """
    rate_decimal = rate / 100
    amount = principal * (1 + rate_decimal / compounding_frequency) ** (compounding_frequency * time)
    return round(amount, precision)


@mcp.tool()
async def storage_cost_calculation(base_price: Number, storage_rate_per_month: Number, 
                                 months: int, precision: int = 2) -> Dict[str, float]:
    """Calculate storage costs and total value after storage.

    Args:
        base_price: Initial price per unit.
        storage_rate_per_month: Storage cost per unit per month.
        months: Number of months in storage.
        precision: Decimal places for rounding.

    Returns:
        Dictionary with total_storage_cost, cost_per_unit_after_storage, and total_cost_per_unit.

    Example:
        >>> storage_cost_calculation(100, 2, 6)
        {'total_storage_cost': 12.0, 'cost_per_unit_after_storage': 112.0, 'months_stored': 6}
    """
    total_storage_cost = round(storage_rate_per_month * months, precision)
    cost_per_unit_after_storage = round(base_price + total_storage_cost, precision)
    
    return {
        'total_storage_cost': total_storage_cost,
        'cost_per_unit_after_storage': cost_per_unit_after_storage,
        'months_stored': months
    }


@mcp.tool()
async def yield_per_acre_value(yield_per_acre: Number, price_per_unit: Number, precision: int = 2) -> float:
    """Calculate total value per acre based on yield and price.

    Args:
        yield_per_acre: Quantity of crop produced per acre.
        price_per_unit: Price per unit of the crop.
        precision: Decimal places for rounding.

    Returns:
        Total value per acre.

    Example:
        >>> yield_per_acre_value(50, 25)
        1250.0
    """
    return round(yield_per_acre * price_per_unit, precision)


@mcp.tool()
async def currency_conversion_simple(amount: Number, exchange_rate: Number, precision: int = 2) -> float:
    """Simple currency conversion (multiply by exchange rate).

    Args:
        amount: Amount in base currency.
        exchange_rate: Exchange rate to target currency.
        precision: Decimal places for rounding.

    Returns:
        Converted amount.

    Example:
        >>> currency_conversion_simple(100, 82.5)  # USD to INR
        8250.0
    """
    return round(amount * exchange_rate, precision)


# Additional utility functions
@mcp.tool()
async def round_to_precision(value: Number, precision: int = 2) -> float:
    """Round a value to specified precision.

    Args:
        value: Number to round.
        precision: Number of decimal places.

    Returns:
        Rounded value.
    """
    return round(float(value), precision)


@mcp.tool()
async def min_two(value1: Number, value2: Number) -> float:
    """Return the minimum value from two numbers.

    Args:
        value1: First numeric value.
        value2: Second numeric value.

    Returns:
        Minimum value as float.
    """
    return float(min(value1, value2))


@mcp.tool()
async def min_three(value1: Number, value2: Number, value3: Number) -> float:
    """Return the minimum value from three numbers.

    Args:
        value1: First numeric value.
        value2: Second numeric value.
        value3: Third numeric value.

    Returns:
        Minimum value as float.
    """
    return float(min(value1, value2, value3))


@mcp.tool()
async def max_two(value1: Number, value2: Number) -> float:
    """Return the maximum value from two numbers.

    Args:
        value1: First numeric value.
        value2: Second numeric value.

    Returns:
        Maximum value as float.
    """
    return float(max(value1, value2))


@mcp.tool()
async def max_three(value1: Number, value2: Number, value3: Number) -> float:
    """Return the maximum value from three numbers.

    Args:
        value1: First numeric value.
        value2: Second numeric value.
        value3: Third numeric value.

    Returns:
        Maximum value as float.
    """
    return float(max(value1, value2, value3))


@mcp.tool()
async def absolute_value(value: Number) -> float:
    """Return the absolute value of a number.

    Args:
        value: Input number.

    Returns:
        Absolute value as float.
    """
    return float(abs(value))


if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        sys.exit(1)