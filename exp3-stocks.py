from exp3.exp3 import exp3, distr
from stats import stats

from stocks import *
from random import shuffle


def exp3Stocks(stockTable, gamma):
   tickers = list(stockTable.keys())
   shuffle(tickers)
   #print(tickers)
   numRounds = len(stockTable[tickers[0]])
   numActions = len(tickers)

   reward = lambda choice, t: payoff(stockTable, t, tickers[choice])
   singleActionReward = lambda j: sum([reward(j,t) for t in range(numRounds)])

   bestAction = max(range(numActions), key=singleActionReward)
   bestActionCumulativeReward = singleActionReward(bestAction)

   cumulativeReward = 0
   t = 0
   expGenerator = exp3(numActions, reward, gamma, rewardMin = -1, rewardMax = 1.0)
   for (choice, reward, estReward, weights) in expGenerator:
      cumulativeReward += reward
      t += 1
      if t == numRounds:
         break

   return cumulativeReward, bestActionCumulativeReward, weights, tickers[bestAction], tickers


prettyList = lambda L: ', '.join(['%.2f' % x for x in L])
payoffStats = lambda data, gamma: stats(exp3Stocks(data, gamma)[0] for _ in range(1000))


def runExperiment(table, gamma):
   print("(Expected payoff, variance) over 1000 trials is %r" % (payoffStats(table, gamma),))
   reward, Gmax, weights, bestStock, tickers = exp3Stocks(table, gamma)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (Gmax - reward))
   print("Best stock was %s at %.2f" % (bestStock, Gmax))
   print("weights: %r" % (prettyList(distr(weights)),))


def weightsStats(table, gamma):
   weightDs = [] # dictionaries of final weights across all rounds

   for i in range(1000):
      reward, Gmax, weights, bestStock, tickers = exp3Stocks(table, gamma)
      weightDs.append(dict(zip(tickers, distr(weights))))

   weightMatrix = []
   for key in tickers:
      print("weight stats for %s: %r" % (key, prettyList(stats(d[key] for d in weightDs))))


def bestGamma(table):
   return max(range(1, 100, 5), key=lambda g: payoffStats(table, g / 100.0)[0]) / 100.0


if __name__ == "__main__":
   table = readInStockTable('stocks/fortune-500.csv')
   gamma = .33
   # print("Gamma used: %.2f, best gamma is %.2f" % (gamma, bestGamma(table)))
   runExperiment(table, gamma)
   # payoffGraph(table, list(sorted(table.keys())), cumulative=True)

   print()

   table2 = readInStockTable('stocks/random-stocks.csv')
   gamma = .33
   # print("Gamma used: %.2f, best gamma is %.2f" % (gamma, bestGamma(table2)))
   runExperiment(table2, gamma)
   # payoffGraph(table2, list(sorted(table2.keys())), cumulative=True)

   #print(weightsStats(table2, 0.33))
