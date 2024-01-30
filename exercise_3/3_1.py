import csv
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
        
    def cost(self):
        return self.shares * self.price
    
    def sell(self,amount):
        self.shares -= amount
        


def read_portfolio(filepath):
    portfolio = []
    with open(filepath) as file:
        rows = csv.reader(file)
        headers = next(rows)
        for line in rows:
            name, shares, price = line
            portfolio.append(Stock(name, int(shares), float(price)))
    return portfolio

def print_portfolio(portfolio):
    print('%10s %10s %10s' % ('Name', 'Shares', 'Price'))
    print(('-'*10 + ' ')*3)
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))

print_portfolio(read_portfolio('../Data/portfolio.csv'))