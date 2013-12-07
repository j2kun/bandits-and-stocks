import math
import random


# upperBound: int, int -> float
# the size of the upper confidence bound for ucb1
def upperBound(step, numPlays):
   return math.sqrt(2.0 * math.log(step + 1) / numPlays)


# ucb1: int, (int, int -> float) -> generator
# perform the ucb1 bandit learning algorithm.  numActions is the number of
# actions, indexed from 0. reward is a function (or callable) accepting as
# input the action and producing as output the reward for that action
def ucb1(numActions, reward):
   payoffSums = [0.0] * numActions
   numPlays = [1] * numActions
   ucbs = [0.0] * numActions

   # initialize empirical sums
   for t in range(numActions):
      payoffSums[t] = reward(t,t)
      yield t, payoffSums[t], ucbs

   t = numActions

   while True:
      ucbs = [payoffSums[i] / numPlays[i] + upperBound(t, numPlays[i]) for i in range(numActions)]
      action = max(range(numActions), key=lambda i: ucbs[i])
      theReward = reward(action, t)

      for theAction in range(numActions):
         numPlays[theAction] += 1
         payoffSums[theAction] += reward(theAction, t)

      yield action, theReward, ucbs
      t = t + 1


