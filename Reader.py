
class Reader:
    def query(self,conditons):
        #self.iterator property...
        pass
    def extract(self,type):
        #depending on "type", return data...
        pass

'''
r = Reader()
r.query("populuation>5k,district=xyz...)
r.extract("Education,Allopathic Health,Pre-Primary School..")
'''

'''
* Property dependency
* Statistic Metric
Property dependency will have dependencies between properties at a universal level.
Statistic Metric Filtered Data
------------------
We will combine facts based on what the statistical metric and property dependency directs us...OK?
* field = 'Education'
* now, look at dependency graph and nature of the chosen data
* now, choose field2 based on whats there in dependency graph and what the statistical metric tells us..
We may even choose to choose another item to compare with...
* now join...Evaluate...Continue
{Education:x,y,z,a,b,c}
A village
A village, chose x: Edn , now: choose one of y:Hospitals ,z: Crop grown,a: etc..,b,c using prop dep and statistical metric
 | edc : (0.8)  hosp : (0.9) | >> interestingness ?

In x% of villages,
 Similarity vs Diversity... 2..
'''