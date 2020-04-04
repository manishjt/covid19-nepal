import numpy as np
import pandas as pd



class Nodes(object):
    def __init__(self):
        self.dictBook=dict()
        self.df = pd.read_csv("district_data1.csv")
        self.df = self.df.dropna()
        self.df['Length'] = self.df['Length'].max()

    def nodesdict(self):
        labels={}
        self.weight_dict={}
        count = 1
        print(len(self.df))
        for i,v in self.df.iterrows():
            self.dictBook.setdefault(count, np.array([float(v['long']), float(v['lat'])]))
            temp = '$'+v['District']+'$'
            labels[count] = "%r"%temp
            self.weight_dict[count] = float(v['Length'])
            if v['District'] == 'Kathmandu':
                print(count)
            count += 1

        coord = self.dictBook
        return coord, labels

    def weights(self):
        return self.weight_dict

# t = Nodes()
# t.nodesdict()

class Links(object):
    def __init__(self):
        self.linktuples = []
        for i in range(31):
            self.linktuples.append((i+1,12))
            self.linktuples.append((12,1+1))
