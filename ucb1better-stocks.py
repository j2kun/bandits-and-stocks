from ucb1.ucb1better import ucb1
from stats import stats
from stocks import *
from random import shuffle

def ucb1Stocks(stockTable):
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
   ucb1Generator = ucb1(numActions, reward)
   for (chosenAction, reward, ucbs) in ucb1Generator:
      cumulativeReward += reward
      t += 1
      if t == numRounds:
         break

   return cumulativeReward, bestActionCumulativeReward, ucbs, tickers[bestAction]


prettyList = lambda L: ', '.join(['%.3f' % x for x in L])
payoffStats = lambda data: stats(ucb1Stocks(data)[0] for _ in range(1000))


def runExperiment(table):
   print("(Expected payoff, variance) over 1000 trials is %r" % (payoffStats(table),))
   reward, bestActionReward, ucbs, bestStock = ucb1Stocks(table)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (bestActionReward - reward))
   print("Best stock was %s at %.2f" % (bestStock, bestActionReward))
   print("ucbs: %r" % prettyList(ucbs))


if __name__ == "__main__":
   table = readInStockTable('stocks/fortune-500.csv')
   runExperiment(table)
   # payoffGraph(table, list(sorted(table.keys())), cumulative=True)

   print()

   table2 = readInStockTable('stocks/random-stocks.csv')
   runExperiment(table2)
   # payoffGraph(table2, list(sorted(table2.keys())), cumulative=True)

