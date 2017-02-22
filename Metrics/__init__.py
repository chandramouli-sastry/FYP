import Deviation, QuartileDeviation

"""
1. Pure Statistical... Field1..take all values... compute metric on the list of values-1 column: 4 metrics
2. Semantic+Statistical Interestingness: statistics on tree... Education:Primary,Secondary...#subset,aggregation:across rows and columns..hold
3. Ratios: number of hospitals/households... property correlation graph...


Phase 1: Generate different kinds of facts: 1, 2 or 3
Phase 2: Combine same kinds of facts: based on similarity or uniqueness
Phase 3: Combine across 1,2 and 3
**********this was discussion phase 1*******
the theory.. now, the practicals :P
that is, what we just discussed...state=karnataka...
by the end of wednesday, we'll have 1 class of facts ready
they'll be like... (3)..they'll find interesting ratios and tell us...
once, we've done that, we must be able to find common fields
TODO:
 1. How to combine facts.-medium priority..
 2. How to find filters.-high priority
30 villages showing some ratio x...find cause...fuzzy intersection of all 30 villages
"""
"""
Metrics:
    i. On a list of values -> Gives value for each data point : We will do this now...
    ii. On a list of values -> Gives 1 value for the list : Maybe we can use for combining
metric properties:
    1. it'll take a list of values and assign interestingness(or some such related measure) to each of the point
    2. would be good if you can give a place where details can be found...or rather...start implementing...

1. Add 4 metrics.(ANOVA-analysis of variance,Peculiarity)
2. Property Correlation Graph & enumerate
3. Using those 4 metrics, throw facts based on ratios.
4. Now, find filters and throw more interesting facts.
By Sunday Afternoon(3PM):  Populate DB; Sample 20k villages; save to hard-disk; generate pair-wise correlations; generate top 20% of the correlations.
By Sunday Night(10PM): Finalize 4 metrics...this we must do now :P
Monday Night: Take some 4 ratios; apply each of the metrics and take norm; visualize villages vs norm[4 lines we'll have];see how useful it is...
Tuesday Night: Decide on general format for a fact and generate fact in that format (21st- turning point)
Wednesday Night: Analyze data to take fuzzy intersection... Phase 1 complete
"""
class Metric:
    def __init__(self,module):
        self.compute_func = module.compute

    def quantify(self,values):
        set_values = zip(set(values),range(len(set(values))))
        map = {i:v for i,v in set_values}
        new_values = [map[i] for i in values]
        return new_values

    def compute(self,values):
        if type(values[0])==str:
            values = self.quantify(values)
        return self.compute_func(values)

Deviation = Metric(Deviation)
QuartileDeviation = Metric(QuartileDeviation)