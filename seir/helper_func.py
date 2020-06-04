import numpy as np

import random
def checkbound_ini(x,pop, priors):
   #S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
   betalow=priors['betalow'];   betaup=priors['betaup'];#transmission rate
   mulow=priors['mulow'];       muup=priors['muup'];#relative transmissibility
   thetalow=priors['thetalow']; thetaup=priors['thetaup'];#movement factor
   Zlow=priors['Zlow'];         Zup=priors['Zup'];#latency period
   alphalow=priors['alphalow']; alphaup=priors['alphaup'];#reporting rate
   Dlow=priors['Dlow'];         Dup=priors['Dup'];#infectious period

   xmin=np.array([betalow,mulow,thetalow,Zlow,alphalow,Dlow]);
   xmax=np.array([betaup,muup,thetaup,Zup,alphaup,Dup]);
   num_loc=pop.shape[0];
   for i in range(num_loc):
       #S
       x[i*5,x[i*5,:]<0]=0;
       x[i*5,x[i*5,:]>pop[i,:]]=pop[i,x[i*5,:]>pop[i,:]];
       #E
       x[i*5+1,x[i*5+1,:]<0]=0;
       #Ir
       x[i*5+2,x[i*5+2,:]<0]=0;
       #Iu
       x[i*5+3,x[i*5+3,:]<0]=0;
       #obs
       x[i*5+4,x[i*5+4,:]<0]=0;

   for i in range(6):
       temp=x[-6+i,:];

       i1 = temp < xmin[i]
       i2 = temp > xmax[i]

       index=np.logical_or(i1, i2); # logical or
       index_out=np.nonzero(index>0);
       index_in=np.nonzero(index==0);

       #redistribute out bound ensemble members
       temp1 = x[-6+i, index_in]
       x[-7+i,index_out]=np.random.choice(temp1.reshape((temp1.shape[1],)),
                                           len(index_out));
       #x = x.reshape(x.shape[0],1)

   return x


def checkbound(x,pop, priors):
   #S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
   betalow=priors['betalow'];   betaup=priors['betaup'];#transmission rate
   mulow=priors['mulow'];       muup=priors['muup'];#relative transmissibility
   thetalow=priors['thetalow']; thetaup=priors['thetaup'];#movement factor
   Zlow=priors['Zlow'];         Zup=priors['Zup'];#latency period
   alphalow=priors['alphalow']; alphaup=priors['alphaup'];#reporting rate
   Dlow=priors['Dlow'];         Dup=priors['Dup'];#infectious period
   
   xmin=np.array([betalow,mulow,thetalow,Zlow,alphalow,Dlow]);
   xmax=np.array([betaup,muup,thetaup,Zup,alphaup,Dup]);
   num_loc=pop.shape[0];
   for i in range(num_loc):
       #S
       x[i*5,x[i*5,:]<0]=0; #logical indexing
       x[i*5,x[i*5,:]>pop[i,:]]=pop[i,x[i*5,:]>pop[i,:]];
       #E
       x[i*5+1,x[i*5+1,:]<0]=0;
       #Ir
       x[i*5+2,x[i*5+2,:]<0]=0;
       #Iu
       x[i*5+3,x[i*5+3,:]<0]=0;
       #obs
       x[i*5+4,x[i*5+4,:]<0]=0;

   for i in range(6):
      #logical indexing : the y-indices of x that are less than xmin(i)
       temp1 = xmin[i]*(1+0.1* np.random.rand(np.sum(x[-6+i,:]<xmin[i]),1))
       x[-6+i,x[-6+i,:]<xmin[i]]= temp1.reshape((temp1.shape[0],));
       #logical indexing : the y-indices of x that are greater than xmin(i)
       temp2 = xmax[i]*(1-0.1* np.random.rand(np.sum(x[-6+i,:]>xmax[i]),1))
       x[-6+i,x[-6+i,:]>xmax[i]]= temp2.reshape((temp2.shape[0],));

   return x
