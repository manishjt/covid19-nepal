import numpy as np
import pandas as pd

class Nodes(object):
    def __init__(self):
        self.dictBook=dict()
        self.df = pd.read_csv("data/dist_data.csv").set_index("index")
        self.df = self.df.dropna()
        self.healthdata = pd.read_csv("data/healthcare.csv").set_index("Name of Government Unit")
        self.labels = {}
        self.pop_density = {}
        self.healthcare = {}
        count = 1
        for _, v in self.df.iterrows():
            self.dictBook.setdefault(count, np.array([float(v['longitude']), float(v['latitude'])]))
            self.labels[count] = v["Districts"]
            self.pop_density[count] = 0#v["density"]
            self.healthcare[count] = float(self.healthdata["Index"]["Province "+str(v["province"])])
            count += 1

    def nodesdict(self):
        return (self.dictBook, self.labels)

    def get_pop_density(self,):
        return self.pop_density

    def get_healthcare(self,):
        return self.healthcare
# t = Nodes()
# coord, labels = t.nodesdict()
# print(t.nodesdict())

class Links(object):
    def __init__(self):
        self.linktuples = []
        for i in range(77):
            for j in range(38):
                if not i == j:
                    self.linktuples.append((i+1,j+1))

class Weights():
    def __init__(self):
        self.wts = pd.read_csv("data/dist_matrix.csv").set_index("Districts")
        max_dist = 0
        for i in self.wts:
            temp = self.wts[i].max()
            if temp > max_dist:
                max_dist = temp
        # print(max_dist)
        for i in self.wts:
            self.wts[i] /= max_dist

    def get_dist(self):
        return self.wts

    def return_dist(self, city1, city2):
        return self.wts[city1][city2]

# w = Weights()
# print(w.return_dist("Janakpur","Kathmandu"))