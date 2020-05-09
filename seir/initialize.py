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
        xmin +=[Slow*pop[i,0],
                Elow*pop[i,0],
                Irlow*pop[i,0],
                Iulow*pop[i,0],
                obslow];

        xmax += [Sup*pop[i,0],
                 Eup*pop[i,0],
                 Irup*pop[i,0],
                 Iuup*pop[i,0],
                 obsup];

    xmin += [betalow, mulow, thetalow, Zlow, alphalow, Dlow];
    xmax += [betaup, muup, thetaup, Zup, alphaup, Dup];

    xmin = np.array(xmin)
    xmax = np.array(xmax)

    paramax = xmax[-6:];
    paramin=xmin[-6:];

    # seeding in Wuhan
    # Wuhan - 170
    seedid = 169; #counting from 0
    #E
    xmin[(seedid)*5+1]=0;
    xmax[(seedid)*5+1]=2000;
    #Is
    xmin[(seedid)*5+2]=0;
    xmax[((seedid)*5+2)]=0;
    #Ia
    xmin[((seedid)*5+3)]=0;
    xmax[((seedid)*5+3)]=2000;

#     print("xmin = ", xmin[840:850])
#     print("xmax = ", xmax[840:850])
#     #Latin Hypercubic Sampling
    x=lhsu(xmin,xmax,num_ens);
    x=x.T;

    for i in range(num_loc):
        x[i*5:i*5+3,:]= np.ceil(x[i*5:i*5+3,:]);
        
    # seeding in other cities
    C=M[:,seedid,0]; #first day
    C = C.reshape(C.shape[0],1)

    seedid = 169

    for i in range(num_loc):
        if i !=seedid:
            #E
            Ewuhan=x[(seedid)*5+1,:];
            x[i*5+1,:]=np.round(C[i]*3*Ewuhan/pop[seedid,0],0);
            #print(Ewuhan[:10])

            #Ia
            Iawuhan=x[(seedid)*5+3,:];
            x[i*5+3,:] = np.round(C[i]*3*Iawuhan/pop[seedid,0]);
            #print(Iawuhan[:10])
    #print(x[:7, :7])
    return x, paramax, paramin
