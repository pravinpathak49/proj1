import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(num_records=1000):
    items = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch']
    prices = [1000, 800, 300, 150, 200]
    costs = [700, 500, 200, 100, 120]

    data = []
    start_date = datetime.now() - timedelta(days=365)

    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 365))
        item_index = random.randint(0, len(items) - 1)
        item = items[item_index]
        price = prices[item_index]
        cost = costs[item_index]
        profit = price - cost
        data.append([date, item, price, cost, profit])

    df = pd.DataFrame(data, columns=['Date', 'Item', 'Price', 'Cost', 'Profit'])
    df.to_csv('sales_data.csv', index=False)

if __name__ == "__main__":
    generate_sales_data()