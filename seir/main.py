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

parameters = inference(M, pop, incidence, params)
print(parameters)
