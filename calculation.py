def purchase_price(currency_rate, budget):
    final_price = 1.05 * currency_rate
    count = round((budget / final_price), 2)
    profit = budget - (count * currency_rate)
    return count , profit


def cash_price(currency_rate, count):
    final_price = 0.93 * currency_rate
    amount = count * final_price
    return amount
