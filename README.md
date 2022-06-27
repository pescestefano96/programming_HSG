# Stock Screener

This project is part of the "Introduction to Programming" and "Programming with Advanced Computer Languages" courses at the University of St. Gallen (HSG) held in the spring semester of 2022. The purpose is to construct a so-called stock screener in Python following the stock trend following strategy of Marvini (2013).

Subsequently, the theoretical background and code structure will be explained.

### Context

A stock screener is a tool that allows investors to swiftly sort through the numerous stocks or other financial instruments  (egg, the rising exchange-traded funds) available depending on the investor's own criteria. Stock screening tools allow investors to use their own methods for determining what makes a stock valuable (long-term investors) or to spot a potential trading opportunity (short-term traders). Both technical and fundamental traders, as well as seasoned and novice investors, can benefit from these tools.

The wide range of financial securities can be narrowed down by investors using stock screening tools and their own set of criteria. Based on their individual needs, users choose certain investment parameters to begin the process. A fundamental investor, for example, might be more interested in market capitalization, earnings per share (EPS), operating cash flow, dividend yield, or similar factors. Instead, moving average levels, relative strength index (RSI) levels, average directional index (ADX) readings, and chart patterns, among others, would be of more interest to a technical trader.

### Building a stock screener in Python

1.	Identify the set of financial instruments to be sorted (e.g., an index such as the S&P500).

2.	Identify the desired period of analysis.

3.  Select the conditions under which to sort the instruments. These depend on the specific investment strategy adopted by the user.

4.	Calculate the metrics needed to implement the desired conditions for each financial instrument.

5.	Collect all instruments that meet the conditions into a list.

### Mark Minervini's Stock Trend Following System
Mark Minervini is a technical analyst, acclaimed author, instructor and considered one of the most successful independent stock traders in the U.S.

He is the author of the best-selling book Trade Like a Stock Market Wizard (2013), in which he explains his stock trend following strategy, which is essentially a momentum trading approach. Accordingly, an investor should buy a stock when:
- The current stock price is above both the 150-day (30-week) and 200-day (40-week) moving average price ranges.
- The 150-day moving average is above the 200-day moving average.
- The 200-day moving average line has been in an upward trend for at least 1 month (preferably 4-5 months minimum in most cases).
- The 50-day (10-week) moving average is above the 150-day and 200-day moving averages.
- The current price of the stock is trading above the 50-day moving average.
- The current price of the stock is at least 30 percent above its 52-week low.
- The current price of the stock is at least 25% of its 52-week high (the closer to a new high, the better).

As part of this project, we followed Minervini's trading strategy and implemented the above mentioned conditions. Moreover, we augmented the set of conditions with two additional key indices widely used by financial professionals:
- The price-to-earnings (PE) ratio must be lower than 20.
- The price/earnings-to-growth (PEG) ratio must be lower than 4.

### How to use
1. Make sure that you have installed all the necessary modules.
2. ...

### Expected outcome
...

### Credits
The project is inspired by and took part of the code from:
- https://www.screener.in/screens/
- https://github.com/hackingthemarkets/stockscreener
- https://gist.github.com/shashankvemuri/50ed514a0ed41599ac29cc297efc3c05
- Trade Like a Stock Market Wizard (2013)

### Authors
- Arvid Huwiler
- Joel Cohen
- Oliver Koch
- Stefano Pesce
- Urs Hurni

### Enjoy 😊📈
