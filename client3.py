################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server requests
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2  # Calculate the average price
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None  # Avoid division by zero
    return price_a / price_b

# Main
if __name__ == "__main__":
    # Initialize variables for stock A and stock B
    stock_A_data = None
    stock_B_data = None

    # Query the price once every N seconds.
    for _ in range(N):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        # Find data for Stock A and Stock B
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            if stock == 'stockA':
                stock_A_data = (stock, bid_price, ask_price, price)
            elif stock == 'stockB':
                stock_B_data = (stock, bid_price, ask_price, price)

        # Calculate and print the ratio if both stock data is available
        if stock_A_data and stock_B_data:
            stock_A_name, stock_A_bid, stock_A_ask, stock_A_price = stock_A_data
            stock_B_name, stock_B_bid, stock_B_ask, stock_B_price = stock_B_data
            ratio = getRatio(stock_A_price, stock_B_price)

            print(f"Stock A Info: {stock_A_name} (bid:{stock_A_bid}, ask:{stock_A_ask}, price:{stock_A_price})")
            print(f"Stock B Info: {stock_B_name} (bid:{stock_B_bid}, ask:{stock_B_ask}, price:{stock_B_price})")
            if ratio is not None:
                print(f"Price Ratio (Stock A / Stock B): {ratio}")
            else:
                print("Price Ratio (Stock A / Stock B): Cannot be calculated (Stock B price is zero)")

            # Reset the stock data
            stock_A_data = None
            stock_B_data = None

