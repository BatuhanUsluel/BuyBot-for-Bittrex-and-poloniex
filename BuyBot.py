#!/usr/bin/env python
#Imports
from poloniex import poloniex
from bittrex import bittrex
from time import sleep
import sys

#Print
print "-----------------------------------------"
print "PumpBot for quickly buying. Enter initial values, wait for coin anouncement and once coin is anounced enter coin name and press enter"
print "Press CTRL+C at any time to close and cancel the program"
print "Coded by Batuhan"
print "-----------------------------------------"

#Bittrex Api Keys
api = bittrex('APIKEY','APISECRET')

#Polo API Keys
conn= poloniex('APIKEY','APISECRET')
#Market to trade at
trade = 'BTC'

#----------------------------------------
#INPUTS
#----------------------------------------
#Poloniex or Bittrex
exchange=float(raw_input("Enter 1 for bittrex, 2 for poloniex:		"))
if (exchange!=1):
	if (exchange!=2):
		sys.exit('Exchange number {0} not valid. Please enter 1 for bittrex, 2 for poloniex'.format(exchange))
#Bitcoin to spend
bitcoin=float(raw_input("Bitcoin to Spend: "))

#Time to Wait
wait=int(raw_input("How many seconds to wait to check for sell order(incase the first time doesn't work(happens if the buy order isn't immediately filled)) in seconds(only integers):		"))

#BuyingMultiplier
buyingmultiplier=float(raw_input("Buy price multiplier: "))

#SellingMultiplier
sellingmultiplier=float(raw_input("Selling price multiplier: "))

#Coint to Buy
currency = raw_input("Coin: ")

#Bittrex market
market= '{0}-{1}'.format(trade,currency)

#Polo market
pair= '{0}_{1}'.format(trade,currency)

#Getting Current Price
if (exchange==1):
	summary=api.getmarketsummary(market)
	price = summary[0]['Last']
	print 'The price for {0} at bittrex is {1:.8f} {2}.'.format(currency, price, trade)
elif (exchange==2):
	currentValues = conn.api_query("returnTicker")
	price = float(currentValues[pair]["last"])
	print 'The price for {0} at poloniex is {1:.8f} {2}.'.format(currency, price, trade)
else:
	sys.exit('Exchange number {0} not valid. Please enter 1 for bittrex, 2 for poloniex'.format(exchange))

#Buying Multiplier
buyprice = round(price*buyingmultiplier, 8)

#Amount Calculation
amount=round(bitcoin/buyprice, 8)

#Buying
if (exchange==1):
	print 'Buying {0} {1} @ Bittrex for {2:.8f} {3}.'.format(amount, currency, buyprice, trade)
	api.buylimit(market, amount, buyprice)
elif (exchange==2):
	print 'Buying {0} {1} @ Poloniex for {2:.8f} {3}.'.format(amount, currency, buyprice, trade)
	orderNumber=conn.buy(pair, buyprice, amount)
else:
	sys.exit('Exchange number {0} not valid. Please enter 1 for bittrex, 2 for poloniex'.format(exchange))

#Multiplying the price by the multiplier
sellprice = round(price*sellingmultiplier, 8)

#Selling
if (exchange==1):
	print 'Selling {0} {1} @ Bittrex for {2:.8f} {3}.'.format(amount, currency, sellprice, trade)
	api.selllimit(market, amount, sellprice)
elif (exchange==2):
	print 'Selling {0} {1} @ Poloniex for {2:.8f} {3}.'.format(amount, currency, sellprice, trade)
	orderNumber=conn.sell(pair,sellprice,amount)
else:
	sys.exit('Exchange number {0} not valid. Please enter 1 for bittrex, 2 for poloniex'.format(exchange))

#RePlace sell order(incase first time doesn't work)
sleep(wait)
print 'Rechecking balance for {0} and placing sell order @ {1}'.format(currency, sellprice)
if (exchange==1):
	bittrexbalance = api.getbalance(currency)
	print 'Your Balance for {0} is {1}'.format(currency, bittrexbalance)
	print 'Placing sell order @ {0} {1} for {2} {3}'.format(sellprice, trade, bittrexbalance, currency)
	api.selllimit(market, bittrexbalance, sellprice)
elif (exchange==2):
	allpolobalance = conn.api_query('returnBalances')
	polobalance = allpolobalance[currency]
	print 'Your Balance for {0} is {1}'.format(currency, polobalance)
	print 'Placing sell order @ {0} {1} for {2} {3}'.format(sellprice, trade, polobalance, currency)
	orderNumber=conn.sell(pair, sellprice, polobalance)
else:
        sys.exit('Exchange number {0} not valid. Please enter 1 for bittrex, 2 for poloniex'.format(exchange))

