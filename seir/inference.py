import numpy as np
from helper_func import checkbound_ini, checkbound
from seir import SEIR
from initialize import initialize
import numpy as np

def inference(M, pop, incidence, params, priors, seeds):
    #Inference for the metapopulation SEIR model
    #Adapted from code by Sen Pei

    #Load files
    # mobility (373,375,14)
    # population (375, 1)
    # load observation (14, 375)

    # Define constants
    Td = params['Td']               # average reporting delay
    a = params['a']                 # shape parameter of gamma distribution
    b = Td/a;                       # scale parameter of gamma distribution
    num_ensemble = params['num_ensemble']

    num_loc=M.shape[0];           # number of locations
    rnds=np.ceil(np.random.gamma(a,b,(10000,1))); # pre-generate gamma random numbers

    # observation operator: obs=Hx
    H=np.zeros([num_loc,5*num_loc+6]);
    for i in range(num_loc):
       H[i,i*5+4]=1;


    num_times=incidence.shape[0];
    obs_truth=incidence.T;


    #set OEV
    OEV=np.zeros([num_loc,num_times]);
    for l in range(num_loc):
       for t in range(num_times):
           OEV[l,t] = max(4,obs_truth[l,t]**2/4);

    num_ens=params['num_ensemble'];#number of ensemble
    pop0=np.matmul(pop.reshape((pop.shape[0],1)), np.ones([1,num_ens]));
    [x,paramax,paramin]=initialize(pop0,num_ens, M, priors, seeds);#get parameter range
    num_var=x.shape[0];#number of state variables


     #IF setting
    Iter=params['num_iter']; #number of iterations
    num_para=paramax.shape[0];#number of parameters
    theta=np.zeros([num_para,Iter+1]);#mean parameters at each iteration
    para_post=np.zeros([num_para,num_ens,num_times,Iter]);#posterior parameters
    sig=np.zeros([1,Iter]);#variance shrinking parameter
    alp= params['alpha'];#variance shrinking rate
    SIG=np.power((paramax-paramin),2/4);#initial covariance of parameters
    lambda_val= params['lambda_val'];#inflation parameter to aviod divergence within each iteration


    #start iteration for Iter round

    for n in range(Iter):
       sig[0, n]=alp**(n-1);
       #generate new ensemble members using multivariate normal distribution
       Sigma=np.diag(sig[0, n]**2*SIG);
       if (n==0):
           #first guess of state space
           [x,_,_]=initialize(pop0,num_ens, M, priors, seeds);
           para = x[-6:, :]
           theta[:,1]=np.mean(para,1);#mean parameter
       else:
           [x,_, _]=initialize(pop0,num_ens, M, priors, seeds);
           para =np.random.multivariate_normal(theta[:,n],Sigma,(num_ens,1)).T;#generate parameters (multivariate random numbers)
           x[-6:,:]=para.reshape((6, num_ens));

       #correct lower/upper bounds of the parameters

       print("IN iter loop: ", n, "Shape of x: ", x.shape)
       x=checkbound_ini(x,pop0);
       #Begin looping through observations
       x_prior=np.zeros([num_var,num_ens,num_times]) #prior
       x_post=np.zeros([num_var,num_ens,num_times]);#posterior
       pop=pop0;
       obs_temp=np.zeros([num_loc,num_ens,num_times]);#records of reported cases
       for t in range(num_times):
           #inflation
           x_mean = np.mean(x,1)
           temp1 = x_mean.reshape(x_mean.shape[0],1) * np.ones([1, num_ens])
           x=temp1+lambda_val*(x-temp1);
           x=checkbound(x,pop);
           #integrate forward
           x,pop=SEIR(x,M,pop,t,pop0);
           #print(x[:5,:5], H[:5, :5])
           obs_cnt=np.matmul(H, x);#new infection
           #print("obs_cnt:", obs_cnt[:5, :5])
           #add reporting delay
           for k in range(num_ens):
               for l in range(num_loc):
                   if obs_cnt[l,k]>0:
                      rnd = (np.random.choice(rnds.reshape((rnds.shape[0],)),int(obs_cnt[l,k])));
                      rnd = rnd.astype(int)
                      for h in range(len(rnd)):
                        if (t+rnd[h]<num_times):
                           obs_temp[l,k,t+rnd[h]]=obs_temp[l,k,t+rnd[h]]+1;




           obs_ens=obs_temp[:,:,t];#observation at t
           x_prior[:,:,t]=x;#set prior
           print("Set x_prior")
           #loop through local observations
           for l in range(num_loc):
               #Get the variance of the ensemble
               obs_var = OEV[l,t];
               prior_var = np.var(obs_ens[l,:]);
               post_var = prior_var*obs_var/(prior_var+obs_var);
               if prior_var==0:#if degenerate
                   post_var = 1e-3;
                   prior_var = 1e-3;

               prior_mean = np.mean(obs_ens[l,:]);
               post_mean = post_var*(prior_mean/prior_var + obs_truth[l,t]/obs_var);

               ### Compute alpha and adjust distribution to conform to posterior moments
               alpha = np.power((obs_var/(obs_var+prior_var)),0.5);
               dy = post_mean + alpha*(obs_ens[l,:]-prior_mean)-obs_ens[l,:];

               #Loop over each state variable (connected to location l)
               rr=np.zeros([num_var]);
               #neighbors=union(find(sum(M(:,l,:),1)>0),find(sum(M(l,:,:),1)>0));

               neighbors=np.union1d(np.nonzero(np.sum(M[:,l,:],1)>0),
                               np.nonzero(np.sum(M[l,:,:],1)>0));
               neighbors = neighbors.reshape((neighbors.shape[0],1))
               neighbors=np.vstack((neighbors,l));#add location l
               for i in range(len(neighbors)):
                   idx=neighbors[i];
                   for j in range(5):
                       A=np.cov(x[idx*5+j,:],obs_ens[l,:]); #caclulate covariance
                       rr[idx*5+j]=A[1,0]/prior_var;


               for i in range(num_loc*5,num_loc*5+5):
                   A=np.cov(x[i,:],obs_ens[l,:]);     #calculate covariance
                   rr[i]=A[1,0 ]/prior_var;

               rr = rr.reshape((rr.shape[0],1))
               dy = dy.reshape((dy.shape[0],1))
               #Get the adjusted variable
               dx= np.matmul(rr, dy.T);
               x=x+dx;
               #Corrections to DA produced aphysicalities
               x = checkbound(x,pop);


           x_post[:,:,t]=x;
           para_post[:,:,t,n]=x[-6:,:];

       para=x_post[-6:,:,1:num_times];
       temp=np.squeeze(np.mean(para,1));#average over ensemble members
       theta[:,n+1]=np.mean(temp,1);#average over time


    parameters=theta[:,-1];#estimated parameters
    print(parameters)
    np.save('parameters.npz',parameters);
    return parameters
