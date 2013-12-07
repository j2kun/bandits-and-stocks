from random import choice

# group a list into successive pairs and apply a type constructor to each value
def pairs(L, typeCons):
   return [(typeCons(L[i]), typeCons(L[i+1])) for i in range(0, len(L) - 1, 2)]


def processLine(stockLine):
   tokens = stockLine.split(',')
   return [tokens[0]] + pairs(tokens[1:], float)


def transpose(A):
   column = lambda A,j: [row[j] for row in A]
   return [column(A, j) for j in range(len(A[0]))]


def readInStockTable(filename):
   with open(filename, 'r') as infile:
      lines = infile.readlines()

   headers = lines[0].strip().split(',')
   numericalTable = [[headers[0]] + pairs(headers[1:], str)] + [processLine(line) for line in lines[1:]]
   preDictTable = transpose(numericalTable)[1:]

   # convert to a dictionary {str: [(float, float)]}
   stockHistoryDict = {}
   for singleStockHistory in preDictTable:
      ticker = singleStockHistory[0][0].split('-')[0]
      stockHistoryDict[ticker] = singleStockHistory[1:]

   return stockHistoryDict


# Compute the payoff of buying 1$ worth of shares at the opening bell,
# and selling as the last trade of the day.
def payoff(stockTable, t, stock, amountToInvest=1.0):
   openPrice, closePrice = stockTable[stock][t]

   sharesBought = amountToInvest / openPrice
   amountAfterSale = sharesBought * closePrice

   return amountAfterSale - amountToInvest


def payoffGraph(table, tickers, cumulative=True):
   # have to run this with python 2.7 to get matplotlib :(

   from matplotlib import pyplot as plt
   import numpy

   numRounds = len(table[tickers[0]])
   numActions = len(tickers)

   reward = lambda choice, t: payoff(table, t, choice)
   singleActionRewards = lambda s: numpy.array([reward(s,t) for t in range(numRounds)])
   xs = numpy.array(list(range(numRounds)))

   ax1 = plt.subplot(111)

   if cumulative:
      plt.title("Cumulative stock rewards over time")
   else:
      plt.title("Stock rewards over time")

   plt.ylabel('Reward')
   plt.xlabel('Day')

   for ticker in tickers:
      if cumulative:
         ax1.plot(xs, numpy.cumsum(singleActionRewards(ticker)), label=ticker)
      else:
         ax1.plot(xs, singleActionRewards(ticker), label=ticker)

   plt.legend()
   plt.show()

