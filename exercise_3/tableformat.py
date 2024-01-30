def print_table(portfolio, attribute_names):
    for name in attribute_names:
        print(f'{name:>10s}', end=' ')
    print()
    print(('-'*10 + ' ')*len(attribute_names))
    print()
    for stock in portfolio:

        print(' '.join('%10s' % getattr(stock, fieldname) for fieldname in attribute_names))
