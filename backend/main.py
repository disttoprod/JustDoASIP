from backend.fetch import get_buy_price, get_sell_price


def get_baseline(months: list[str], monthly_investment: float) -> list[float]:
    return [i * monthly_investment for i in range(len(months))]


def get_sip(
    ticker: str, months: list[str], monthly_investment: float
) -> list[float]:
    money_pool = 0
    stocks = []

    worths = []
    for date in months:
        money_pool += monthly_investment
        buy = get_buy_price(ticker, date)
        sell = get_sell_price(ticker, date)

        stock, money_pool = divmod(money_pool, buy)
        stocks.append(stock)

        worths.append(sum(stocks) * sell + money_pool)

    return worths


if __name__ == "__main__":
    from backend.util import get_months_between

    months = get_months_between("2023-01-01", "2024-05-21")
    print(get_baseline(months, 10000))
    print(get_sip("^NSEI", months, 10000))
