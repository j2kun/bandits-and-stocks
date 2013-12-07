
def mean(aList):
   theSum = 0
   count = 0

   for x in aList:
      theSum += x
      count += 1

   return 0 if count == 0 else float(theSum) / count


def stats(aList):
   vals = [x for x in aList]
   avg = mean(vals)
   devs = [(x-avg)*(x-avg) for x in vals]
   return (avg, mean(devs))

