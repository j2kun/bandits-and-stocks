from stats import stats
from stocks import *
from random import shuffle, choice


def randomBandit(numActions, reward):
   t = 0

   while True:
      i = choice(range(numActions))
      yield i, reward(i, t)
      t += 1


def randomBanditStocks(stockTable):
   tickers = list(stockTable.keys())
   shuffle(tickers) # note that this makes the algorithm SO unstable
   numRounds = len(stockTable[tickers[0]])
   numActions = len(tickers)

   reward = lambda choice, t: payoff(stockTable, t, tickers[choice])
   singleActionReward = lambda j: sum([reward(j,t) for t in range(numRounds)])

   bestAction = max(range(numActions), key=singleActionReward)
   bestActionCumulativeReward = singleActionReward(bestAction)

   cumulativeReward = 0
   t = 0
   randomGenerator = randomBandit(numActions, reward)
   for (chosenAction, reward) in randomGenerator:
      cumulativeReward += reward
      t += 1
      if t == numRounds:
         break

   return cumulativeReward, bestActionCumulativeReward, tickers[bestAction]


prettyList = lambda L: ', '.join(['%.3f' % x for x in L])
payoffStats = lambda data: stats(randomBanditStocks(data)[0] for _ in range(1000))


def runExperiment(table):
   print("(Expected payoff, variance) over 1000 trials is %r" % (payoffStats(table),))
   reward, bestActionReward, bestStock = randomBanditStocks(table)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (bestActionReward - reward))
   print("Best stock was %s at %.2f" % (bestStock, bestActionReward))


if __name__ == "__main__":
   table = readInStockTable('stocks/fortune-500.csv')
   runExperiment(table)

   print()

   table2 = readInStockTable('stocks/random-stocks.csv')
   runExperiment(table2)

