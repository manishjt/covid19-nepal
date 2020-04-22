def checkbound_ini(x,pop):
   #S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
   betalow=0.8;betaup=1.5;#transmission rate
   mulow=0.2;muup=1.0;#relative transmissibility
   thetalow=1;thetaup=1.75;#movement factor
   Zlow=2;Zup=5;#latency period
   alphalow=0.02;alphaup=1.0;#reporting rate
   Dlow=2;Dup=5;#infectious period

   xmin=np.array([betalow,mulow,thetalow,Zlow,alphalow,Dlow]);
   xmax=np.array([betaup,muup,thetaup,Zup,alphaup,Dup]);
   num_loc=pop.shape[0];
   for i in range(num_loc):
       #S
       x[(i-1)*5+1,x[(i-1)*5+1,:]<0]=0;
       x[(i-1)*5+1,x[(i-1)*5+1,:]>pop[i,:]]=pop[i,x[(i-1)*5+1,:]>pop[i,:]];
       #E
       x[(i-1)*5+2,x[(i-1)*5+2,:]<0]=0;
       #Ir
       x[(i-1)*5+3,x[(i-1)*5+3,:)<0]=0;
       #Iu
       x[(i-1)*5+4,x[(i-1)*5+4,:)<0]=0;
       #obs
       x[(i-1)*5+5,x[(i-1)*5+5,:]<0]=0;

   for i in range(6):
       temp=x[end-6+i,:];
       index=(temp<xmin[i]) or (temp>xmax[i]); # logical or
       index_out=np.nonzero(index>0);
       index_in=np.nonzero(index==0);
       #redistribute out bound ensemble members
       x[end-6+i,index_out]=datasample(x[end-6+i,index_in],
                                             len(index_out));
                            #TODO: Find numpy equivalent of datasample

   return x

def checkbound(x,pop):
   #S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
   betalow=0.8;betaup=1.5;#transmission rate
   mulow=0.2;muup=1.0;#relative transmissibility
   thetalow=1;thetaup=1.75;#movement factor
   Zlow=2;Zup=5;#latency period
   alphalow=0.02;alphaup=1.0;#reporting rate
   Dlow=2;Dup=5;#infectious period
   xmin=np.array([betalow,mulow,thetalow,Zlow,alphalow,Dlow]);
   xmax=np.array([betaup,muup,thetaup,Zup,alphaup,Dup]);
   num_loc=pop.shape[0];
   for i in range(num_loc):
       #S
       x[(i-1)*5+1,x[(i-1)*5+1,:]<0]=0; #logical indexing
       x[(i-1)*5+1,x[(i-1)*5+1,:]>pop[i,:]]=pop[i,x[(i-1)*5+1,:]>pop[i,:]];
       #E
       x[(i-1)*5+2,x[(i-1)*5+2,:]<0]=0;
       #Ir
       x[(i-1)*5+3,x[(i-1)*5+3,:]<0]=0;
       #Iu
       x[(i-1)*5+4,x[(i-1)*5+4,:]<0]=0;
       #obs
       x[(i-1)*5+5,x[(i-1)*5+5,:]<0]=0;

   for i in range(6):
      #logical indexing : the y-indices of x that are less than xmin(i)
       x[end-6+i,x[end-6+i,:]<xmin[i]]=xmin[i]*(1+0.1*
                                                np.random.rand(np.sum(x[end-6+i,:]<xmin[i]),1));
       #logical indexing : the y-indices of x that are greater than xmin(i)
       x[end-6+i,x[end-6+i,:]>xmax[i]]=xmax[i]*(1-0.1*
                                                np.random.rand(np.sum(x[end-6+i,:]>xmax[i]),1));

    return x
