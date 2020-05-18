from __future__ import division, print_function
"""
Author: Manish Jung Thapa, ETH Zurich
please leave the line above if you want to use or modify this code!
Performs simulations of COVID19 spread between cities in Nepal
Checkout 10.1103/PhysRevE.75.056107 for more details on the model
"""
__author__ = 'Manish J. Thapa'


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.special import erf
from itertools import count
import shapefile as shp
import seaborn as sns
from data_loader.road_data import Nodes, Links, Weights
# from nodesdata import Nodes
# from linksdata import Links

def sigmoid(x):
    return np.exp(x)/(1+np.exp(x))

class diseasespread():
    """parameters for the model"""
    def __init__(self, nlist, elist, label, pop_density, healthcare, weights, nc_tau=1, nc_M=1,): #one needs to find a good paramter such that ODEs become solvable, and yield physically reliable solutions
        self.elist=elist
        self.nlist=nlist
        self.label=label
        self.pop_density = pop_density
        self.healthcare = healthcare
        self.weights=weights.get_dist()
        self.nc_tau = nc_tau
        self.nc_M = nc_M
        self.graph=nx.Graph()
        self.graph.add_edges_from(self.elist)
        self.graph.add_nodes_from(self.nlist)

    def tau(self, node):
        return(self.nc_tau*14*self.healthcare[node])

    def neighbors(self, node):
        """returns the neighboring nodes"""
        return list(self.graph.neighbors(node))

    def M(self,node):
        """link strengths"""
        neighbors = self.neighbors(node)
        Mij=np.zeros_like(np.array(neighbors),dtype=float)
        for nbrid, nbr in enumerate(neighbors):
            # print(nbrid, nbr)
            Mij[nbrid]=1/(self.nc_M*self.weights[self.label[node]][self.label[nbr]])
        return Mij

    def nodeDegree(self,node):
        """returns node degree"""
        return len(list(self.graph.neighbors(node)))

    def evolve(self,t,x,y):
        """time-dynamics of all the nodes. time-delay is set to 0 for simplicity"""
        dxdt=np.zeros_like(x,dtype=float)
        for i in range(len(x)):
            if len(np.array(self.neighbors(i+1))-1)==0:
                dxdt[i] = -x[i] / self.tau(i+1)
            else:
                xj=x[np.array(self.neighbors(i+1))-1]
                dxdt[i] = -x[i] / self.tau(i+1) + (1-y[i])*np.sum(xj* self.M(i+1))/self.nodeDegree(i+1)
        return dxdt

    def evolve1(self,t,x,y,x_1):
        """time-dynamics of all the nodes. time-delay is set to 0 for simplicity"""
        dxdt=np.zeros_like(x,dtype=float)
        for i in range(len(x)):
            if len(np.array(self.neighbors(i+1))-1)==0:
                dxdt[i] = -x[i] / self.tau(i+1)
            else:
                xj=x_1[np.array(self.neighbors(i+1))-1]
                dxdt[i] = -x[i] / self.tau(i+1) + (1-y[i])*np.sum(xj* self.M(i+1))/self.nodeDegree(i+1)
        return dxdt

#create an object of Links
linkobject=Links()
elist=linkobject.linktuples
# print(elist)
# exit()
#create an object of Nodes
nodeobject=Nodes()
coord, labels=nodeobject.nodesdict()

weights=Weights()
pop_density = nodeobject.get_pop_density()
healthcare = nodeobject.get_healthcare()
# space = np.logspace(-1.3,0.7,100)
space_tau = [10]
space_M = [10]
healing_probability = 0.7

if __name__ == "__main__":
    N=77
    assert N == len(coord)
    nlist=np.arange(N,dtype=int)+1
    nlist=nlist.tolist()
    # taulist=np.ones(N)*5 #keep identical healing rates for all the nodes
    x0=np.ones(N)*0 #at t=0, all other cities are normal
    y0=x0
    x0[24]=0.1 #at t=0, Kathmandu is diseased
    samples=100
    simuwindow=100 #the evolution is distinctly observed at longer times, so keep the simulation window large
    cnt = 0
    for i in space_tau:
        for j in space_M:
            print("normalization tau = "+str(i)+", M = "+str(j))
            spread=diseasespread(nlist,elist,labels,pop_density,healthcare,weights,nc_tau=i,nc_M=j)
            t=np.linspace(0,simuwindow,samples)
            xt=odeint(spread.evolve,x0,t,tfirst=True,args=tuple([y0]))
            print(xt.shape)
            print("x = ",np.sum(xt, axis=1))
            
            x_stepwise = np.zeros_like(xt,dtype=float)
            x_stepwise[0]=x0
            for k in range(simuwindow-1):
                if k >= 14:
                    y0 = x_stepwise[k-14]*healing_probability
                print("Day, ",k+1)
                print("healed = ",np.sum(y0))#,x_stepwise[k-14])
                t_temp = np.linspace(k,k+1,2,endpoint=True)
                x_stepwise[k+1] = sigmoid(odeint(spread.evolve1,x_stepwise[k],t_temp,tfirst=True,args=tuple([y0,x_stepwise[k-1]]))[1])
                print("New infections = ",np.sum(x_stepwise[k+1]))
            print("x_stepwise = ",np.sum(x_stepwise, axis=1))

            if 1:
                # plt.plot(t,np.sum(xt, axis=1), color="black", label="total")
                plt.plot(t,np.sum(x_stepwise, axis=1)/N, color="red", label="total1")
                # print(np.sum(xt,axis=1).shape)
                # plt.plot(t,np.sum(np.array(spread.firstpart), axis=1),color="green", label="recovered")
                # plt.plot(t,np.sum(np.array(spread.secondpart), axis=1),color="red", label="new")
                plt.title("Simple equation, delay = 0, yt = 0, nor tau = "+str(i)+", M = "+str(j))
                plt.xlabel("Total Infections")
                plt.ylabel("Time (Days)")
                # plt.title("Using sigmoid, normalization tau = "+10+", M = "+str(j))
                plt.savefig("results/district_road/plot/plot_"+str(cnt)+".png")
                plt.show()
                plt.clf()
                cnt+=1
            # else:
                for day in range(int(simuwindow)):
                    nodelist=[]
                    for i in range(N):
                        dictBook = dict()
                        dictBook.setdefault('health', xt[:,i][int(day)])
                        nodelist.append((i+1,dictBook.copy()))

                    linklist=elist

                    plt.figure(figsize=(22, 12))
                    G = nx.Graph()
                    G.add_nodes_from(nodelist)
                    G.add_edges_from(linklist)
                    groups = set(nx.get_node_attributes(G,'health').values())
                    mapping = dict(zip(sorted(groups),count()))
                    nodes = G.nodes()
                    colors = [mapping[G.node[nid]['health']] for nid in nodes]
                    # neplinks = nx.draw_networkx_edges(G, coord, edge_colors='k', style='dashed', edge_size=1, alpha=0.6)
                    nepnodes = nx.draw_networkx_nodes(G, coord, nodelist=nodes, node_color=colors, alpha=0.5,with_labels=True, node_size=500, cmap=plt.cm.jet)
                    nx.draw_networkx_labels(G, coord, labels, font_size=16)
                    plt.colorbar(nepnodes)
                    plt.axis('off')

                    #draw map of Nepal, need the .shp file
                    sns.set(style="whitegrid", color_codes=True)
                    sns.mpl.rc("figure", figsize=(10,6))
                    pathshp = "shapefiles/nepal_data/npl_admbnda_districts_nd_20190430.shp"
                    # pathshp = "npl_admbnda_adm0_nd_20190430.shp"
                    shapef = shp.Reader(pathshp)

                    def country_map(shapef):
                        for shape in shapef.shapeRecords():
                            xcoord = [xpt[0] for xpt in shape.shape.points[:]]
                            ycoord = [ypt[1] for ypt in shape.shape.points[:]]
                            plt.plot(xcoord, ycoord, 'k')
                    country_map(shapef)
                    print('Time - ',day)
                    plt.title('delay = 0, yt = 0, Time- '+str(int(int(day))),fontsize=24)
                    plt.savefig('results/district_road/map/covid'+str(int(int(day)))+'.png')

    #ffmpeg -r 0.5 -f image2 -s 1920x1080 -i covid%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p covidlatest.mp4 #run from the terminal