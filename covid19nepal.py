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
from road_data import Nodes, Links
# from nodesdata import Nodes
# from linksdata import Links

class diseasespread():
    """parameters for the model"""
    def __init__(self, nlist, elist, tau, weights, sigma=25, alpha=0.1,beta=0.01,theta=10,a=4.0,b=3.0): #one needs to find a good paramter such that ODEs become solvable, and yield physically reliable solutions
        self.elist=elist
        self.nlist=nlist
        self.weights=weights
        self.graph=nx.Graph()
        self.graph.add_edges_from(self.elist)
        self.graph.add_nodes_from(self.nlist)
        self.tau=tau
        self.theta=theta
        self.beta=beta
        self.alpha=alpha
        self.sigma=sigma
        self.a=a
        self.b=b

    def sigmoid(self, x):
        """two different functions for the disturbances the neighboring nodes creates towards node i"""
        if 1:
            return erf((x)/(self.sigma)) #newly discovered (inspired by a quantum computing research). sigma could be different for every node
        else:
            return (1-np.exp(-self.alpha*x))/(1+np.exp(-self.alpha*(x-self.theta))) #DOI: 10.1103/PhysRevE.75.056107

    def neighbors(self, node):
        """returns the neighboring nodes"""
        return list(self.graph.neighbors(node))

    def M(self,node):
        """link strengths"""
        neighbors = self.neighbors(node)
        Mij=np.zeros_like(np.array(neighbors),dtype=float)
        for nbrid, nbr in enumerate(neighbors):
            Mij[nbrid]=1.0
        return Mij

    def Delay(self,node):
        """gives time-delay for disease to spread"""
        neighbors = self.neighbors(node)
        tij = np.zeros_like(neighbors,dtype=float)
        for nbrid, nbr in enumerate(neighbors):
            tij[nbrid] = 1.0
        return tij

    def nodeDegree(self,node):
        """returns node degree"""
        return len(list(self.graph.neighbors(node)))

    def f(self,node):
        """weighs the influence of neighboring nodes on node i"""
        return (self.a*self.nodeDegree(node))/(1+self.b*self.nodeDegree(node))

    def evolve(self,x,t):
        """time-dynamics of all the nodes. time-delay is set to 0 for simplicity"""
        dxdt=np.zeros_like(x,dtype=float)
        for i in range(len(x)):
            if len(np.array(self.neighbors(i+1))-1)==0:
                dxdt[i] = -x[i] / self.tau[i]
            else:
                xj=x[np.array(self.neighbors(i+1))-1]
                dxdt[i] = -x[i] / self.tau[i] + self.sigmoid(np.sum(xj * np.array(self.weights[i + 1]) * np.exp(-self.beta * np.array(self.Delay(i + 1)),dtype=float) / np.array((self.f(i + 1)),dtype=float)))
        return dxdt

#create an object of Links
linkobject=Links()
elist=linkobject.linktuples

#create an object of Nodes
nodeobject=Nodes()
coord, labels=nodeobject.nodesdict()

weights=nodeobject.weights()

if __name__ == "__main__":
    N=31
    assert N == len(coord)
    nlist=np.arange(N,dtype=int)+1
    nlist=nlist.tolist()
    taulist=np.ones(N)*5 #keep identical healing rates for all the nodes
    spread=diseasespread(nlist,elist,taulist,weights)
    x0=np.ones(N)*0 #at t=0, all other cities are normal
    x0[11]=1 #at t=0, Kathmandu is diseased
    samples=100
    simuwindow=100 #the evolution is distinctly observed at longer times, so keep the simulation window large
    t=np.linspace(0,simuwindow,samples)
    xt=odeint(spread.evolve,x0,t)

    if 0:
        for i in range(N):
            plt.plot(t,xt[:,int(i)])
        plt.show()

    else:
        for day in range(int(samples)):
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
            neplinks = nx.draw_networkx_edges(G, coord, edge_colors='k', style='dashed', edge_size=1, alpha=0.6)
            nepnodes = nx.draw_networkx_nodes(G, coord, nodelist=nodes, node_color=colors, alpha=0.5,with_labels=True, node_size=500, cmap=plt.cm.jet)
            nx.draw_networkx_labels(G, coord, labels, font_size=16)
            plt.colorbar(nepnodes)
            plt.axis('off')

            #draw map of Nepal, need the .shp file
            sns.set(style="whitegrid", color_codes=True)
            sns.mpl.rc("figure", figsize=(10,6))
            pathshp = "npl_admbnda_districts_nd_20190430.shp"
            # pathshp = "npl_admbnda_adm0_nd_20190430.shp"
            shapef = shp.Reader(pathshp)

            def country_map(shapef):
                for shape in shapef.shapeRecords():
                    xcoord = [xpt[0] for xpt in shape.shape.points[:]]
                    ycoord = [ypt[1] for ypt in shape.shape.points[:]]
                    plt.plot(xcoord, ycoord, 'k')
            country_map(shapef)
            print('Time - ',day)
            plt.title('Time-'+str(int(int(day))),fontsize=24)
            plt.savefig('results_road/covid000'+str(int(int(day)))+'.png')

    #ffmpeg -r 0.5 -f image2 -s 1920x1080 -i covid%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p covidlatest.mp4 #run from the terminal