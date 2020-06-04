import scipy.io
M_file = scipy.io.loadmat("data/M.mat")
pop_file = scipy.io.loadmat("data/pop.mat")
incidence_file = scipy.io.loadmat("data/incidence.mat")
M= M_file['M']
pop = pop_file['pop']
incidence = incidence_file['incidence']
from inference import inference
params = {}
params['Td']=14;                         # average reporting delay
params['a']=1.85;                       # shape parameter of gamma distribution

params['num_ensemble']=300;                  #number of ensembleIter=params['num_iter']10; #number of iterationss
Iter=params['num_iter']= 10;            #number of iterations
params['alpha'] = 0.8;                  #variance shrinking rate
params['lambda_val']= 1.1;              #inflation parameter to aviod divergence within each iteration


#S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
priors = {}
priors['betalow']=0.8;  priors['betaup']=1.5;#transmission rate
priors['mulow']=0.2;    priors['muup']=1.0;#relative transmissibility
priors['thetalow']=1;   priors['thetaup']=1.75;#movement factor
priors['Zlow']=2;       priors['Zup']=5;#latency period
priors['alphalow']=0.02;priors['alphaup']=1.0;#reporting rate
priors['Dlow']=2;       priors['Dup']=5;#infectious period


intial_prior = {}
initial_prior['Slow']=1.0;      initial_prior['Sup']=1.0;           # susceptible fraction
initial_prior['Elow']=0;        initial_prior['Eup']=0;               # exposed
initial_prior['Irlow']=0;       initial_prior['Irup']=0;             # documented infection
initial_prior['Iulow']=0;       initial_prior['Iuup']=0;             # undocumented infection
initial_prior['obslow']=0;      initial_prior['obsup']=0;           # reported case
initial_prior['betalow']=0.8;   initial_prior['betaup']=1.5;     # transmission rate
initial_prior['mulow']=0.2;     initial_prior['muup']=1.0;         # relative transmissibility
initial_prior['thetalow']=1;    initial_prior['thetaup']=1.75;    # movement factor
initial_prior['Zlow']=2;        initial_prior['Zup']=5;               # latency period
initial_prior['alphalow']=0.02; initial_prior['alphaup']=1.0;  # reporting rate
initial_prior['Dlow']=2;        initial_prior['Dup']=5;               # infectious period

seed = 169 #TODO: add a matrix of seed

parameters = inference(M, pop, incidence, params, priors, initial_prior, seed)
print(parameters)
