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
import matplotlib
import datetime

from data_loader.road_data import Nodes, Links, Weights
from data_loader.plot_map import plot_map
from data_loader.make_folium import make_folium

# from nodesdata import Nodes
# from linksdata import Links

class diseasespread():
    """parameters for the model"""
    def __init__(self, nlist, elist, label, pop_density, healthcare, weights, nc_tau=1, nc_M=1, sigma=25, alpha=0.1,beta=0.01,theta=10,a=4.0,b=3.0): #one needs to find a good paramter such that ODEs become solvable, and yield physically reliable solutions
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
        self.pop_density = pop_density
        self.healthcare = healthcare
        self.theta=theta
        self.beta=beta
        self.alpha=alpha
        self.sigma=sigma
        self.a=a
        self.b=b
        self.firstpart = []
        self.secondpart = []

    def tau(self, node):
        return(self.nc_tau*14*self.healthcare[node])

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
            # print(nbrid, nbr)
            Mij[nbrid]=self.nc_M*self.weights[self.label[node]][self.label[nbr]]
        return Mij
        # return 

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
        fp = np.zeros_like(x,dtype=float)
        sp = np.zeros_like(x,dtype=float)
        for i in range(len(x)):
            if len(np.array(self.neighbors(i+1))-1)==0:
                fp[i] = -x[i] / self.tau(i+1)
                sp[i] = 0
            else:
                xj=x[np.array(self.neighbors(i+1))-1]
                fp[i] = -x[i] / self.tau(i+1)
                sp[i] = self.sigmoid(np.sum(xj * np.array(self.M(i+1)) * np.exp(-self.beta * np.array(self.Delay(i + 1)),dtype=float) / np.array((self.f(i + 1)),dtype=float)))
            dxdt[i] = fp[i] + sp[i]
        # self.firstpart.append(fp)
        # self.secondpart.append(sp)
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
space = [1]
if __name__ == "__main__":
    N=77
    assert N == len(coord)
    nlist=np.arange(N,dtype=int)+1
    nlist=nlist.tolist()
    # taulist=np.ones(N)*5 #keep identical healing rates for all the nodes
    x0=np.ones(N)*0 #at t=0, all other cities are normal
    x0[24]=0.1 #at t=0, Kathmandu is diseased
    samples=100
    simuwindow=100 #the evolution is distinctly observed at longer times, so keep the simulation window large
    cnt = 0
    for i in space:
        
        print("normalization tau = "+str(10)+", M = "+str(i))
        spread=diseasespread(nlist,elist,labels,pop_density,healthcare,weights,nc_tau=i,nc_M=i)
        t=np.linspace(0,simuwindow,samples)
        xt=odeint(spread.evolve,x0,t)
        # print(xt.shape)
        if 0:
            plt.plot(t,np.sum(xt, axis=1)/N,color="black", label="total")
            # print(np.sum(xt,axis=1).shape)
            # plt.plot(t,np.sum(np.array(spread.firstpart), axis=1),color="green", label="recovered")
            # plt.plot(t,np.sum(np.array(spread.secondpart), axis=1),color="red", label="new")
            # plt.title("Using erf and sigma = 25, normalization tau = "+str(10)+", M = "+str(i))
            # plt.title("Using sigmoid, normalization tau = "+10+", M = "+str(j))
            plt.title("Infection Plot")
            plt.ylabel("Total Infections (in percent)")
            plt.xlabel("Time (Days)")
            plt.savefig("results/totalplot_"+str(cnt)+".png")

            plt.show()
            plt.clf()
            cnt+=1
            for day in range(int(simuwindow)):
                intensity = xt[day]*100/N
                geofile = "shapefiles/nepal-map-governance/NEPAL_DISTRICTS_WGS.shp"
                save_image = "results/districts_road/map/covid000"+str(int(int(day)))+".png"
                title = 'Day-'+str(int(int(day)))
                plot_map(geofile, intensity, save_image, title)
        else:
            coordinates = coord.values()
            data = xt*100/N
            make_folium(coordinates, data, datetime.date(year=2020, month=5, day=6), save_file="results/results.html")

        # else:
        if 0:
            for day in range(int(simuwindow)):
                xt[day] /= N
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
                nepnodes = nx.draw_networkx_nodes(G, coord, nodelist=nodes, node_color=colors, alpha=0.5,with_labels=True, node_size=700, cmap=plt.cm.jet)
                # nx.draw_networkx_labels(G, coord, labels, font_size=12)
                maxval = np.max(np.array(list(groups),dtype="float"))
                cbar = plt.colorbar(nepnodes,label='Intensity of Infection (in %)')
                cbar.ax.set_yticklabels(np.around(np.linspace(0,maxval,8)*100,decimals=4),size=22)

                text = cbar.ax.yaxis.label
                font = matplotlib.font_manager.FontProperties(size=22)
                text.set_font_properties(font)

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
                plt.title('Day-'+str(int(int(day))),fontsize=30)
                plt.savefig('results/districts_road/map1/covid000'+str(int(int(day)))+'.png')

    #ffmpeg -r 0.5 -f image2 -s 1920x1080 -i covid%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p covidlatest.mp4 #run from the terminal