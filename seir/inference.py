import numpy as np
from helper_func import checkbound_ini, checkbound
from seir import seir
def inference(M, pop, incidence):
#Inference for the metapopulation SEIR model
#Adapted from code by Sen Pei

   #Load files
   # mobility (373,375,14)
   # population (375, 1)
   # load observation (14, 375)

   # Define constants
   Td=9;                         % average reporting delay
   a=1.85;                       % shape parameter of gamma distribution
   b=Td/a;                       % scale parameter of gamma distribution

   num_loc=M.shape[0];            % number of locations
   rnds=ceil(gamrnd(a,b,1e4,1)); %pre-generate gamma random numbers

   # observation operator: obs=Hx
   H=np.zeros([num_loc,5*num_loc+6]);
   for i in range(num_loc):
       H[i,(i-1)*5+5]=1;


   num_times=incidence.shape[0];
   obs_truth=incidence.T;
   #set OEV
   OEV=np.zeros([num_loc,num_times]);
   for l in range(num_loc):
       for t in range(num_times):(
           OEV[l,t] = max(4,obs_truth[l,t]^2/4);
       end
   end

   num_ens=300;#number of ensemble
   pop0=pop*np.ones([1,num_ens]);
   [x,paramax,paramin]=initialize(pop0,num_ens);#get parameter range
   num_var=x.shape[0];#number of state variables

   #IF setting
   Iter=10; #number of iterations
   num_para=paramax.shape[0];#number of parameters
   theta=np.zeros([num_para,Iter+1]);#mean parameters at each iteration
   para_post=np.zeros([num_para,num_ens,num_times,Iter]);#posterior parameters
   sig=np.zeros([1,Iter]);#variance shrinking parameter
   alp=0.9;#variance shrinking rate
   SIG=np.power((paramax-paramin),2/4);#initial covariance of parameters
   lambda_val=1.1;#inflation parameter to aviod divergence within each iteration

   %start iteration for Iter round
   for n in range(Iter):
       sig[n]=alp^(n-1);
       #generate new ensemble members using multivariate normal distribution
       Sigma=np.diag(sig[n]^2*SIG);
       if (n==1):
           #first guess of state space
           [x,~,~]=initialize(pop0,num_ens);
           para=x[end-5:end,:];
           theta[:,1]=np.mean(para,2);#mean parameter
       else
           [x,~,~]=initialize(pop0,num_ens);
           para=np.random.multivariate_normal(theta(:,n).T,Sigma,num_ens).T;#generate parameters (multivariate random numbers)
           x[end-5:,:]=para;

       #correct lower/upper bounds of the parameters
       x=checkbound_ini(x,pop0);
       #Begin looping through observations
       x_prior=np.zeros([num_var,num_ens,num_times]) #prior
       x_post=np.zeros([num_var,num_ens,num_times]);#posterior
       pop=pop0;
       obs_temp=np.zeros([num_loc,num_ens,num_times]);#records of reported cases
       for t in range(num_times):
           print([n, t])
           #inflation
           temp1 = np.mean(x,2) * np.ones([1, num_ens])
           x=temp1+lambda_val*(x-temp1);
           x=checkbound(x,pop);
           #integrate forward
           x,pop=SEIR(x,M,pop,t,pop0);
           obs_cnt=H*x;#new infection
           #add reporting delay
           for k in range(num_ens):
               for l in range(num_loc):
                   if obs_cnt[l,k]>0:
                       rnd=datasample[rnds,obs_cnt[l,k]];
                       for h in range(len(rnd)):
                           if (t+rnd[h]<=num_times)
                               obs_temp[l,k,t+rnd[h]]=obs_temp[l,k,t+rnd[h]]+1;





           obs_ens=obs_temp[:,:,t];#observation at t
           x_prior[:,:,t]=x;#set prior
           #loop through local observations
           for l in range(num_loc):
               #Get the variance of the ensemble
               obs_var = OEV[l,t];
               prior_var = np.var(obs_ens[l,:]);
               post_var = prior_var*obs_var/(prior_var+obs_var);
               if prior_var==0:#if degenerate
                   post_var=1e-3;
                   prior_var=1e-3;

               prior_mean = np.mean(obs_ens[l,:]);
               post_mean = post_var*(prior_mean/prior_var + obs_truth[l,t]/obs_var);

               ### Compute alpha and adjust distribution to conform to posterior moments
               alpha = np.power((obs_var/(obs_var+prior_var)),0.5);
               dy = post_mean + alpha*(obs_ens[l,:]-prior_mean)-obs_ens[l,:];

               #Loop over each state variable (connected to location l)
               rr=np.zeros[1,num_var];
               neighbors=np.union1d(np.nonzero(np.sum(M[:,l,:],3)>0),
                               np.nonzero(np.sum(M[l,:,:],3)>0));
               neighbors=np.vcat((neighbors,l));#add location l
               for i in range(len(neighbors)):
                   idx=neighbors[i];
                   for j in range(5):
                       A=np.cov(x[(idx-1)*5+j,:],obs_ens[l,:]); #caclulate covariance
                       rr[(idx-1)*5+j]=A[2,1]/prior_var;


               for i in range(num_loc*5+1,num_loc*5+6):
                   A=np.cov(x[i,:],obs_ens[l,:]);     #calculate covariance
                   rr[i]=A[2,1]/prior_var;


               #Get the adjusted variable
               dx=rr.T*dy;
               x=x+dx;
               #Corrections to DA produced aphysicalities
               x = checkbound(x,pop);

           x_post[:,:,t]=x;
           para_post[:,:,t,n]=x[end-5:,:];

       para=x_post(end-5:end,:,1:num_times);
       temp=np.squeeze(np.mean(para,2));#average over ensemble members
       theta[:,n+1]=np.mean(temp,2);#average over time

   parameters=theta[:,end];#estimated parameters

   np.save('parameters.npz',parameters);