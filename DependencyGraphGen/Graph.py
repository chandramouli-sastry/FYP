class Graph:
    def __init__(self):
        '''

        '''
        self.graph_ds=dict()
        self.top_percentile_graph_ds = None

    def get_value(self,field1,field2):
        return self.graph_ds.get((field1,field2),0)

    def put_value(self,field1,field2,value):
        self.graph_ds[(field1,field2)] = value
        self.graph_ds[(field2,field1)] = value

    def obtain_list_of_all_values(self):
        return self.graph_ds.values()

    def obtain_top_percentile_threshold(self, percentile):
        l = self.obtain_list_of_all_values()
        l.sort(reverse=True)
        length = len(l)
        index = int((percentile / 100.0) * length)
        return l[index]

    def get(self,field1,field2):
        return self.top_percentile_graph_ds.get((field1,field2),False)

    def put(self,field1,field2):
        self.top_percentile_graph_ds[(field1,field2)] = True
        self.top_percentile_graph_ds[(field2,field1)] = True

    def compute_top_percentile_graph(self,percentile):
        thresh = self.obtain_top_percentile_threshold(percentile)
        self.top_percentile_graph_ds = dict()
        for i,j in self.graph_ds:
            if self.get_value(i,j)>=thresh:
                self.put(i,j)
