import math
import random

# draw: [float] -> int
# pick an index from the given list of floats proportionally
# to the size of the entry (i.e. normalize to a probability
# distribution and draw according to the probabilities).
def draw(weights):
    choice = random.uniform(0, sum(weights))
    choiceIndex = 0

    for weight in weights:
        choice -= weight
        if choice <= 0:
            return choiceIndex

        choiceIndex += 1

# distr: [float] -> (float)
# Normalize a list of floats to a probability distribution.  Gamma is an
# egalitarianism factor, which tempers the distribtuion toward being uniform as
# it grows from zero to one.
def distr(weights, gamma=0.0):
    theSum = float(sum(weights))
    return tuple((1.0 - gamma) * (w / theSum) + (gamma / len(weights)) for w in weights)


# exp3: int, (int, int -> float), float -> generator
# perform the exp3 algorithm.
# numActions is the number of actions, indexed from 0
# rewards is a function (or callable) accepting as input the action and
# producing as output the reward for that action
# gamma is an egalitarianism factor
def exp3(numActions, reward, gamma, rewardMin = 0, rewardMax = 1):
   weights = [1.0] * numActions

   t = 0
   while True:
      probabilityDistribution = distr(weights, gamma)
      choice = draw(probabilityDistribution)
      theReward = reward(choice, t)

      for choice in range(numActions): # take into account all information
         rewardForUpdate = reward(choice, t)
         scaledReward = (rewardForUpdate - rewardMin) / (rewardMax - rewardMin) # rewards scaled to 0,1
         estimatedReward = 1.0 * scaledReward / probabilityDistribution[choice]
         weights[choice] *= math.exp(estimatedReward * gamma / numActions) # important that we use estimated reward here!

      yield choice, theReward, estimatedReward, weights
      t = t + 1
