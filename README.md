# crypto-allocation

Basic Crypto Index fund allocation tool

Takes in a # of currencies as an arg and outputs the allocation based on market cap

# Options
--number - Sets number of currencies in the portfolio<br />
--ignore - Sets currencies to be ignored<br />
--max - Sets max allocation of an individual currency<br />

# Basic Usage:
allocation.py --number 5<br />
-Generates a portfolio with the top 5 currencies<br />

# More advanced usage:
allocation.py --number 10 --ignore 'Bitcoin Cash','Ethereum Classic' --max 20<br />
-Generates a portfolio with the top 10 currencies<br />
-Ignore 'Bitcoin Cash' and 'Ethereum Classic' currencies<br />
-Sets max portfolio allocation to 20 percent<br />
