from django.db import models


class Portfolio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    cash = models.FloatField(default=100000)
    owner = models.ForeignKey('auth.User', related_name='portfolios')

    def get_short_exposure(self):
        """
        Return the portfolio's short exposure.

        Returns:
            float: portfolio's short exposure. 0 if no shorts.
        """
        shorted_stocks = self.stocks.filter(quantity__lt=0)
        if len(shorted_stocks) == 0:
            return 0
        shorted_stocks_tickers = ",".join([stock.ticker for stock in shorted_stocks])
        shorted_stocks_quote = get_yahoo_quote(shorted_stocks_tickers)
        short_exposure = sum(
            [-stock.quantity * shorted_stocks_quote[stock.ticker]['price']
             for stock in shorted_stocks]
        )
        return short_exposure


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')


class Transaction(models.Model):
    ticker = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    price = models.FloatField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

# Must import after model definitions because of circular import error
from views import get_yahoo_quote
