import numpy as np

def lhsu(xmin,xmax,nsample):
   nvar=xmin.shape[0];
   ran=np.random.random((nsample,nvar));
   s= np.zeros((nsample,nvar));
   for j in range(nvar):
      idx=np.random.permutation(nsample);
      P =(idx.T -ran[:,j])/nsample;
      s[:,j] = xmin[j] + np.multiply(P, (xmax[j]-xmin[j]));
   return s

def initialize(pop,num_ens, M):
    #Initialize the metapopulation SEIRS model
    #inputs: pop -> population matrix, num_ens -> number of ensembles, M -> mobility matrix
    num_loc=pop.shape[0];
    # num_var=5*num_oc+6;
    # S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
    #prior range
    Slow=1.0;Sup=1.0;           # susceptible fraction
    Elow=0;Eup=0;               # exposed
    Irlow=0;Irup=0;             # documented infection
    Iulow=0;Iuup=0;             # undocumented infection
    obslow=0;obsup=0;           # reported case
    betalow=0.8;betaup=1.5;     # transmission rate
    mulow=0.2;muup=1.0;         # relative transmissibility
    thetalow=1;thetaup=1.75;    # movement factor
    Zlow=2;Zup=5;               # latency period
    alphalow=0.02;alphaup=1.0;  # reporting rate
    Dlow=2;Dup=5;               # infectious period

    #range of model state including variables and parameters
    xmin=[];
    xmax=[];
    for i in range(num_loc):
        xmin +=[Slow*pop[i],
                Elow*pop[i],
                Irlow*pop[i],
                Iulow*pop[i],
                obslow];

        xmax += [Sup*pop[i],
                 Eup*pop[i],
                 Irup*pop[i],
                 Iuup*pop[i],
                 obsup];

    xmin += [betalow, mulow, thetalow, Zlow, alphalow, Dlow];
    xmax += [betaup, muup, thetaup, Zup, alphaup, Dup];
    xmin = np.array(xmin)
    xmax = np.array(xmax)

    paramax = xmax[-5:];
    paramin=xmin[-5:];

    # seeding in Wuhan
    # Wuhan - 170
    seedid = 170;
    #E
    xmin[(seedid-1)*5+2]=0;
    xmax[(seedid-1)*5+2]=2000;
    #Is
    xmin[(seedid-1)*5+3]=0;
    xmax[((seedid-1)*5+3)]=0;
    #Ia
    xmin[((seedid-1)*5+4)]=0;
    xmax[((seedid-1)*5+4)]=2000;

    #Latin Hypercubic Sampling
    x=lhsu(xmin,xmax,num_ens);
    x=x.T;
    for i in range(num_loc):
        x[(i-1)*5+1:(i-1)*5+4,:]= np.round(x[(i-1)*5+1:(i-1)*5+4,:]);


    # seeding in other cities
    C=M[:,170,1]; #first day
    for i in range(num_loc):
        if i !=seedid:
            #E
            Ewuhan=x[(seedid-1)*5+2,:];
            x[(i-1)*5+2,:]=np.round(C[i]*3*Ewuhan/pop[seedid]);
            #Ia
            Iawuhan=x[(seedid-1)*5+4,:];
            x[(i-1)*5+4,:] = np.round(C[i]*3*Iawuhan/pop[seedid]);
    return x, paramax, paramin
