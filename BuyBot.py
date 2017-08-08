#!/usr/bin/env python
#Imports
from bittrex import bittrex
from time import sleep

#Print
print "-----------------------------------------"
print "PumpBot for quickly buying. Enter initial values, wait for coin anouncement and once coin is anounced enter coin name and press enter"
print "Press CTRL+C at any time to close and cancel the program"
print "Coded by Batuhan"
print "-----------------------------------------"

#ApiKeys
api = bittrex('bc3eb80b26694c0f8653c085ee9002f7','1de0219f7d8d4eafa68cbc33b08cf6e9')

#Market to trade at
trade = 'BTC'

#----------------------------------------
#INPUTS
#----------------------------------------
#Bitcoin to spend
bitcoin=float(raw_input("Bitcoin to Spend: "))

#BuyingMultiplier
buyingmultiplier=float(raw_input("Buy price multiplier: "))

#SellingMultiplier
sellingmultiplier=float(raw_input("Selling price multiplier: "))

#Coint to Buy
currency = raw_input("Coin: ")
market= '{0}-{1}'.format(trade,currency)

#Getting Current Price
summary=api.getmarketsummary(market)
price = summary[0]['Last']
print 'The price for {0} is {1:.8f} {2}.'.format(currency, price, trade)

#Getting Lowest Price of Day
#summary=api.getmarketsummary(market)
#price = summary[0]['Low']
#print 'The lowest price of the day for {0} is {1:.8f} {2}.'.format(currency, price, trade)

#Buying Multiplier
buyprice = round(price*buyingmultiplier, 8)

#Amount Calculation
amount=round(bitcoin/buyprice, 8)

#Buying
print 'Buying {0} {1} for {2:.8f} {3}.'.format(amount, currency, buyprice, trade)
api.buylimit(market, amount, buyprice)

#Multiplying the price by the multiplier
sellprice = round(price*sellingmultiplier, 8)

#Selling
print 'Selling {0} {1} for {2:.8f} {3}.'.format(amount, currency, sellprice, trade)
api.selllimit(market, amount, sellprice)
	
#Checking balance and reselling(Incase selling doesn't work)
sleep(3)
balance = api.getbalance(currency)
if balance>0:
	api.selllimit(market, balance, sellprice)
