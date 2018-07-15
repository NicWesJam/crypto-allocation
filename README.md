# crypto-allocation

Basic Crypto Index fund allocation tool

Takes in a # of currencies as an arg and outputs the allocation based on market cap

# Options
--number - Sets number of currencies in the portfolio
--ignore - Sets currencies to be ignored
--max - Sets max allocation of an individual currency

# Basic Usage:
allocation.py --number 5
-Generates a portfolio with the top 5 currencies

# More advanced usage:
allocation.py --number 10 --ignore 'Bitcoin Cash','Ethereum Classic' --max 20
-Generates a portfolio with the top 10 currencies
-Ignore 'Bitcoin Cash' and 'Ethereum Classic' currencies
-Sets max portfolio allocation to 20 percent
