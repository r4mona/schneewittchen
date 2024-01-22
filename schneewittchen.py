import requests
import address_for_currencies


# search rune get_balance api
# search tron market_enquiry api
# get balance in USDT
# get balanc in bnb
# addressen in sep .py file


def get_json(url):
	request = requests.get(url)
	# request.status_code - gibt den status im Terminal aus (nr. <400 = alles i.o, >400 = error)
	if request.status_code >= 400:
		print(url)
		print(request.status_code, "error")
		return dict()
	data = request.json() #=dictionary
	return data


def get_chain_from_address(address):
	if address[:4] == "TKiv":
		return "trx"
	if address[:4] == "bnb1":
		return "bnb"
	if address[:2] == "0x":
		return "bsc"
	else:
		return "not identified"

	
def get_balance(addresses):
	balances = list()
	for address in addresses:
		chain = get_chain_from_address(address)
		if chain == "not identified":
			return -1

	
		if chain == "bsc":
			url = "https://api.bscscan.com/api?module=account&action=balance&address=%s" % (address)		
			normaliser = 10**18
			data = get_json(url)
			balance_field = float(data.get("result"))/normaliser
			balances.append((chain, balance_field))
		
		if chain == "trx":
			url = "https://apilist.tronscan.org/api/account?address=%s" % (address)
			data = get_json(url)
			data = data.get("balances")
			normaliser = 10**6
			for token in data:
				balance_field = float(token.get("balance"))/ normaliser
				quote = token.get("tokenName")
				balances.append((quote, balance_field))
				
		if chain == "bnb":
			url = "https://dex.binance.org/api/v1/account/%s" % (address)
			data = get_json(url)
			tokenlist = data.get("balances")
			normaliser = 1
			for token in tokenlist:
				balance_field = float(token.get("free"))/normaliser
				quote = token.get("symbol")
				quote = quote.split("-")
				quote = quote[0].lower()
				balances.append((quote, balance_field))
	return balances	


def market_enquiry(pair):
	url = "https://api.hitbtc.com/api/3/public/ticker/%s" % (pair) 
	data = get_json(url)
	return float(data.get("last", "-111"))


def my_balance_in_x(addressesdict, quote):
	balance_in_usdt = 0
	for chain, address in addressesdict.items():
		balance = get_balance(address)
		if chain == quote:
			price = 1
		else:
			if chain == "bsc":
				chain = "bnb"
			price = market_enquiry(chain + quote)
		balance_in_usdt += balance * price
	return balance_in_usdt

#print(my_balanc_in_usdt(address_for_currencies.addresses, "usdt"))

def my_balance_in_quote(addressesdict, quote):
	balance_in_quote = my_balance_in_x(addressesdict, "usdt") / market_enquiry(quote + "usdt")
	return balance_in_quote


print(my_balance_in_quote(address_for_currencies.addresses, "bnb"))



