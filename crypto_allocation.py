'''
crypto_allocation.py
Cryptocurrency Index Fund Allocation Calculator

Takes in a # of currencies as an arg and outputs the allocation based on market cap

Options
number - Sets number of currencies in the portfolio
ignore - Sets currencies to be ignored
max - Sets max allocation of an individual currency

Basic Usage:
allocation.py --number 5
-Generates a portfolio with the top 5 currencies

More advanced usage:
allocation.py --number 10 --ignore 'Bitcoin Cash','Ethereum Classic' --max 20
-Generates a portfolio with the top 10 currencies
-Ignore 'Bitcoin Cash' and 'Ethereum Classic' currencies
-Sets max portfolio allocation to 20 percent
'''

import argparse
import json
import urllib3

urllib3.disable_warnings()

class crypto_allocation():


	def __init__(self, currencies, ignore, max_allocation):
		'''
		Initialization routine parses args
		'''
		#self.get_args()
		self.currencies = currencies
		self.ignore = ignore
		self.max_allocation = max_allocation
		self.data_parsed = None


	def run(self):
		'''
		primary routine to calculatate allocation
		'''
		self.wrong_sum, self.data_parsed= self.main()



	def print_output(self):
		'''
		Data output
		'''
		wrong_sum = self.wrong_sum
		data_parsed = self.data_parsed
		#output data
		if wrong_sum == 1:
			print('Note: Sum does not equal 100 percent due to Max Allocation limit')

		for currency in data_parsed:
			print('#' + currency[0] + ' - Allocation:' + str(round(float(currency[1])*100,1)) + '% - Name:' + \
				currency[2] + ' - USD Market Cap:$' + "{:,}".format(float(currency[3])))


	def main(self):
		'''
		main calculation routine, gets data from coin market cap and calls parse_data to parse the data
		'''
		data_parsed = []
		wrong_sum = 0
		currencies = self.currencies
		ignore = self.ignore
		max_allocation = self.max_allocation

		#adjust ignore if empty to work with the rest of the program
		if ignore == None:
			ignore = ''
		if max_allocation != None:
			max_allocation = max_allocation / 100.0

		#Get data from coinmarketcap.com
		currency_to_get = currencies + len(ignore)
		http = urllib3.PoolManager()
		r = http.request('GET', 'https://api.coinmarketcap.com/v1/ticker/?limit='+str(currency_to_get))
		data = json.loads(r.data.decode('utf-8'))
		data_parsed, wrong_sum = self.parse_data(data,ignore,currencies,max_allocation)
		return wrong_sum, data_parsed


	def parse_data(self,data,ignore,currencies,max_allocation):
		'''
		remove and references to the ignore currencies and then create a list of the requested length
		'''
		data_post_ignore = []
		allocation_modified = [] #used with max_allocation
		data_parsed = []
		list_length = 0
		flag = 0
		total_cap = 0.0
		wrong_sum = 0
		
		for currency in data:
			flag = 0
			for name in ignore:
				if currency['name'] == name:
					flag = 1

			if flag == 0 and list_length < currencies:
				data_post_ignore.append(currency)
				list_length = list_length + 1

		for currency in data_post_ignore:
			total_cap = total_cap + float(currency['market_cap_usd'])

		#Initial Allocation Run Through
		rank=1
		for currency in data_post_ignore:
			allocation = float(currency['market_cap_usd']) / total_cap 
			allocation_modified.append(allocation)
			data_parsed.append([str(rank),str(allocation),currency['name'],currency['market_cap_usd'],currency['price_usd']])
			#print('Currency: ' + currency['Name'] + ' - Market Cap %')
			rank = rank+1

		#Apply max_allocation value
		if max_allocation != None:
			temp = 0
			temp_market_cap = 0
			for i in range(0,len(data_parsed)):
				#print (allocation_modified)
				if allocation_modified[i] > max_allocation:
					temp = allocation_modified[i] - max_allocation
					allocation_modified[i] = max_allocation
					if i < len(data_parsed):
						temp_market_cap = 0
						for j in range(i+1,len(data_parsed)):
							temp_market_cap = temp_market_cap + allocation_modified[j]
						
						for j in range(i+1,len(data_parsed)):
							allocation_modified[j] = allocation_modified[j] + allocation_modified[j]/temp_market_cap*temp

			#update data_parsed with modified allocations
			for i in range(0,len(data_parsed)):
				data_parsed[i][1] = allocation_modified[i]

			wrong_sum = 0 #flag variable to see if max allocation was hit, used for formatting
			if sum(allocation_modified)<.98: #leave a little error room
				wrong_sum = 1
				
		return data_parsed, wrong_sum


	def get_data_parsed(self):
		return self.data_parsed

#----------------------------------------- Command Line Access -------------------------------

def csv_list(string):
	'''
	input type used in arg parser
	'''
	return string.split(',')


def get_args():
	'''
	setup parser, parse args and return parsed args
	'''
	parser = argparse.ArgumentParser(description='Calculate Cryptocurrency portfolio allocation')
	parser.add_argument('--number', type=int, help='number of crypto currencies you want', dest='currencies', required=True)
	parser.add_argument('--ignore', type=csv_list, help='currencies you want to ignore', dest='ignore', required=False)
	parser.add_argument('--max', type=float, help='size of maximum position in percentage', dest='max_allocation', required=False)
	args = parser.parse_args()

	return args


if __name__ == '__main__':
	args = get_args()
	crypto_allocation = crypto_allocation(args.currencies, args.ignore, args.max_allocation)
	crypto_allocation.run()
	crypto_allocation.print_output()
