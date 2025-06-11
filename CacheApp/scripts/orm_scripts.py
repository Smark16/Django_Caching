import itertools

def run():
    count = itertools.count(start=1)
    print('first five numbers')

    for i in range(5):
     print(f'10 * {next(count)}', (10 * next(count)) - 10)