import numpy as np

def SEIR(x, M , pop, ts, pop0):
    #the metapopulation SEIR model
    dt = 1
    tmstep = 1

    #integrate forward for one day
    num_loc = pop.shape[0];
    num_ens = x.shape[1];
   
    #S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
    #TODO: check 0 indexing
    Sidx = np.array(range(1,5,5*num_loc));
    Eidx = np.array(range(2,5,5*num_loc));
    Isidx = np.array(range(3,5,5*num_loc));
    Iaidx = np.array(range(4,5,5*num_loc));
    obsidx = np.array(range(5,5,5*num_loc));
    betaidx = 5*num_loc+1;
    muidx=5*num_loc+2;
    thetaidx=5*num_loc+3;
    Zidx=5*num_loc+4;
    alphaidx=5*num_loc+5;
    Didx=5*num_loc+6;

    S=zeros(num_loc,num_ens,tmstep+1);
    E=zeros(num_loc,num_ens,tmstep+1);
    Is=zeros(num_loc,num_ens,tmstep+1);
    Ia=zeros(num_loc,num_ens,tmstep+1);
    Incidence=zeros(num_loc,num_ens,tmstep+1);
    obs=zeros(num_loc,num_ens);

    #initialize S,E,Is,Ia and parameters
    S[:,:,0]=x[Sidx,:];
    E[:,:,0]=x[Eidx,:];
    Is[:,:,0]=x[Isidx,:];
    Ia[:,:,0]=x[Iaidx,:];
    beta=x[betaidx,:];
    mu=x[muidx,:];
    theta=x[thetaidx,:];
    Z=x[Zidx,:];
    alpha=x[alphaidx,:];
    D=x[Didx,:];
   
    #start integration
    #TODO: pythonize, rewrite repeated steps as functions
    tcnt=0;
    for t in range(ts+dt,dt,ts+tmstep):
        tcnt=tcnt+1;
        dt1=dt;
        #first step
        M_ts = M[:,:,ts]
        S_tcnt = S[:,:,tcnt]
        Ia_tcnt = Ia[:,:,tcnt]
        Is_tcnt = Is[:,:,tcnt]
        E_tcnt = E[:, :, tcnt]
        
        dt_theta = dt1*(np.ones(num_loc,1) * theta)
        temp2 = (pop-Is_tcnt)
        ESenter=np.multiply(dt_theta,
                            (M_ts*np.divide(S_tcnt,temp2)));
        ESleft=np.min(np.multiply((dt_theta),
                           np.multiply(np.divide(S_tcnt,temp2),(np.sum(M_ts).T*ones(1,num_ens)))),
                      dt1*S_tcnt);
        EEenter=np.multiply(dt_theta,
                            (M_ts*np.divide(E_tcnt,temp2)));
        EEleft=np.min(np.multiply(dt_theta,
                          np.multiply(np.divide(E_tcnt,temp2),np.sum(M_ts).T*ones(1,num_ens))),
                      dt1*E[:,:,tcnt]);
        EIaenter= np.multiply(dt_theta,
                              (M_ts*np.divide(Ia_tcnt,temp2)));
        EIaleft=np.min(np.multiply(dt_theta,
                            np.multiply(np.divide(Ia_tcnt,temp2),(np.sum(M_ts).T*ones(1,num_ens)))),
                       dt1*Ia_tcnt);
       
        
        Eexps=np.divide(dt1*np.multiply((ones(num_loc,1)*beta),np.multiply(S_tcnt,Is_tcnt)),pop);
        Eexpa=np.divide(np.multiply(dt1*(ones(num_loc,1)*mu),
                                    np.multiply((ones(num_loc,1)*beta),
                                                np.multiply(S_tcnt,Ia_tcnt))),
                        pop);
        Einfs=np.divide(dt1*np.multiply((ones(num_loc,1)*alpha),E_tcnt),(ones(num_loc,1)*Z));
        Einfa=np.divide(dt1*np.multiply((ones(num_loc,1)*(1-alpha)),E_tcnt),(ones(num_loc,1)*Z));
        Erecs=dt1*np.divide(Is_tcnt,(ones(num_loc,1)*D));
        Ereca=dt1*np.divide(Ia_tcnt,ones(num_loc,1)*D);
       
        ESenter=max(ESenter,0);ESleft=max(ESleft,0);
        EEenter=max(EEenter,0);EEleft=max(EEleft,0);
        EIaenter=max(EIaenter,0);EIaleft=max(EIaleft,0);
        Eexps=max(Eexps,0);Eexpa=max(Eexpa,0);
        Einfs=max(Einfs,0);Einfa=max(Einfa,0);
        Erecs=max(Erecs,0);Ereca=max(Ereca,0);
       
        ##########stochastic version
        ESenter=np.random.poisson(ESenter);ESleft=np.random.poisson(ESleft);
        EEenter=np.random.poisson(EEenter);EEleft=np.random.poisson(EEleft);
        EIaenter=np.random.poisson(EIaenter);EIaleft=np.random.poisson(EIaleft);
        Eexps=np.random.poisson(Eexps);
        Eexpa=np.random.poisson(Eexpa);
        Einfs=np.random.poisson(Einfs);
        Einfa=np.random.poisson(Einfa);
        Erecs=np.random.poisson(Erecs);
        Ereca=np.random.poisson(Ereca);

        sk1=-Eexps-Eexpa+ESenter-ESleft;
        ek1=Eexps+Eexpa-Einfs-Einfa+EEenter-EEleft;
        isk1=Einfs-Erecs;
        iak1=Einfa-Ereca+EIaenter-EIaleft;
        ik1i=Einfs;
        
        
        #second step
        Ts1=S[:,:,tcnt]+sk1/2;
        Te1=E[:,:,tcnt]+ek1/2;
        Tis1=Is[:,:,tcnt]+isk1/2;
        Tia1=Ia[:,:,tcnt]+iak1/2;
       
        M_ts = M[:, :, ts]
        temp3 = pop-Tis1
        temp4 = (sum(M_ts).T*ones(1,num_ens))
        ESenter=np.multiply(dt_theta,(M_ts*np.divide(Ts1,temp3)));
        ESleft=min(np.multiply(np.multiply(dt_theta,np.divide(Ts1,temp3)),temp4),dt1*Ts1);
        EEenter=np.multiply(dt_theta,(M_ts*np.divide(Te1,temp3)));
        EEleft=min(np.multiply(np.multiply(dt_theta,np.divide(Te1,temp3)),temp4),dt1*Te1);
        EIaenter=np.multiply(dt_theta,(M_ts*np.divide(Tia1,temp3)));
        EIaleft=min(np.multiply(np.multiply(dt_theta,np.divide(Tia1,temp3)),temp4),dt1*Tia1);
       
        num_loc_ones = np.ones(num_loc, 1)
        Eexps=np.multiply(dt1*(num_loc_ones*beta),
                          np.multiply(Ts1, np.divide(Tis1,pop)));
        Eexpa=np.multiply(dt1*(num_loc_ones*mu),
                          np.multiply(np.multiply((num_loc_ones*beta),Ts1),
                                      np.divide(Tia1,pop)));
        Einfs=np.multiply(dt1*(num_loc_ones*alpha),np.divide(Te1,(num_loc_ones*Z)));
        Einfa=np.multiply(dt1*(num_loc_ones*(1-alpha)),np.divide(Te1,(num_loc_ones*Z)));
        Erecs=dt1*np.divide(Tis1,(num_loc_ones*D));
        Ereca=dt1*np.divide(Tia1,(num_loc_ones*D));
       
        ESenter=max(ESenter,0);ESleft=max(ESleft,0);
        EEenter=max(EEenter,0);EEleft=max(EEleft,0);
        EIaenter=max(EIaenter,0);EIaleft=max(EIaleft,0);
        Eexps=max(Eexps,0);Eexpa=max(Eexpa,0);
        Einfs=max(Einfs,0);Einfa=max(Einfa,0);
        Erecs=max(Erecs,0);Ereca=max(Ereca,0);
       
        ###########stochastic version
        ESenter=np.random.poisson(ESenter);ESleft=np.random.poisson(ESleft);
        EEenter=np.random.poisson(EEenter);EEleft=np.random.poisson(EEleft);
        EIaenter=np.random.poisson(EIaenter);EIaleft=np.random.poisson(EIaleft);
        Eexps=np.random.poisson(Eexps);
        Eexpa=np.random.poisson(Eexpa);
        Einfs=np.random.poisson(Einfs);
        Einfa=np.random.poisson(Einfa);
        Erecs=np.random.poisson(Erecs);
        Ereca=np.random.poisson(Ereca);

        sk2=-Eexps-Eexpa+ESenter-ESleft;
        ek2=Eexps+Eexpa-Einfs-Einfa+EEenter-EEleft;
        isk2=Einfs-Erecs;
        iak2=Einfa-Ereca+EIaenter-EIaleft;
        ik2i=Einfs;
        
        #third step
        Ts2=S[:,:,tcnt]+sk2/2;
        Te2=E[:,:,tcnt]+ek2/2;
        Tis2=Is[:,:,tcnt]+isk2/2;
        Tia2=Ia[:,:,tcnt]+iak2/2;
       
        M_ts = M[:, :, ts]
        temp5 = pop-Tis2
        temp6 = (sum(M_ts).T*ones(1,num_ens))
        ESenter=np.multiply(dt_theta,(M_ts*np.divide(Ts2,temp5)));
        ESleft=min(np.multiply(np.multiply(dt_theta,np.divide(Ts2,temp5)),temp6),dt1*Ts2);
        EEenter=np.multiply(dt_theta,(M_ts*np.divide(Te2,temp5)));
        EEleft=min(np.multiply(np.multiply(dt_theta,np.divide(Te2,temp5)),temp6),dt1*Te2);
        EIaenter=np.multiply(dt_theta,(M_ts*np.divide(Tia2,temp5)));
        EIaleft=min(np.multiply(np.multiply(dt_theta,np.divide(Tia2,temp5)),temp6),dt1*Tia2);
       
        num_loc_ones = np.ones(num_loc, 1)
        Eexps=np.multiply(dt1*(num_loc_ones*beta),
                          np.multiply(Ts2, np.divide(Tis2,pop)));
        Eexpa=np.multiply(dt1*(num_loc_ones*mu),
                          np.multiply(np.multiply((num_loc_ones*beta),Ts2),
                                      np.divide(Tia2,pop)));
        Einfs=np.multiply(dt1*(num_loc_ones*alpha),np.divide(Te2,(num_loc_ones*Z)));
        Einfa=np.multiply(dt1*(num_loc_ones*(1-alpha)),np.divide(Te2,(num_loc_ones*Z)));
        Erecs=dt1*np.divide(Tis2,(num_loc_ones*D));
        Ereca=dt1*np.divide(Tia2,(num_loc_ones*D));

       
        ESenter=max(ESenter,0);ESleft=max(ESleft,0);
        EEenter=max(EEenter,0);EEleft=max(EEleft,0);
        EIaenter=max(EIaenter,0);EIaleft=max(EIaleft,0);
        Eexps=max(Eexps,0);Eexpa=max(Eexpa,0);
        Einfs=max(Einfs,0);Einfa=max(Einfa,0);
        Erecs=max(Erecs,0);Ereca=max(Ereca,0);
       
        ###########stochastic version
        ESenter=np.random.poisson(ESenter);ESleft=np.random.poisson(ESleft);
        EEenter=np.random.poisson(np.random.poissonEEenter);EEleft=np.random.poisson(EEleft);
        EIaenter=np.random.poisson(EIaenter);EIaleft=np.random.poisson(EIaleft);
        Eexps=np.random.poisson(Eexps);
        Eexpa=np.random.poisson(Eexpa);
        Einfs=np.random.poisson(Einfs);
        Einfa=np.random.poisson(Einfa);
        Erecs=np.random.poisson(Erecs);
        Ereca=np.random.poisson(Ereca);

        sk3=-Eexps-Eexpa+ESenter-ESleft;
        ek3=Eexps+Eexpa-Einfs-Einfa+EEenter-EEleft;
        isk3=Einfs-Erecs;
        iak3=Einfa-Ereca+EIaenter-EIaleft;
        ik3i=Einfs;
       
        #fourth step
        Ts3=S[:,:,tcnt]+sk3;
        Te3=E[:,:,tcnt]+ek3;
        Tis3=Is[:,:,tcnt]+isk3;
        Tia3=Ia[:,:,tcnt]+iak3;
        
        M_ts = M[:, :, ts]
        temp5 = pop-Tis3
        temp6 = (sum(M_ts).T*ones(1,num_ens))
        ESenter=np.multiply(dt_theta,(M_ts*np.divide(Ts3,temp5)));
        ESleft=min(np.multiply(np.multiply(dt_theta,np.divide(Ts3,temp5)),temp6),dt1*Ts3);
        EEenter=np.multiply(dt_theta,(M_ts*np.divide(Te3,temp5)));
        EEleft=min(np.multiply(np.multiply(dt_theta,np.divide(Te3,temp5)),temp6),dt1*Te3);
        EIaenter=np.multiply(dt_theta,(M_ts*np.divide(Tia3,temp5)));
        EIaleft=min(np.multiply(np.multiply(dt_theta,np.divide(Tia3,temp5)),temp6),dt1*Tia3);
       
        num_loc_ones = np.ones(num_loc, 1)
        Eexps=np.multiply(dt1*(num_loc_ones*beta),
                          np.multiply(Ts3, np.divide(Tis3,pop)));
        Eexpa=np.multiply(dt1*(num_loc_ones*mu),
                          np.multiply(np.multiply((num_loc_ones*beta),Ts3),
                                      np.divide(Tia3,pop)));
        Einfs=np.multiply(dt1*(num_loc_ones*alpha),np.divide(Te3,(num_loc_ones*Z)));
        Einfa=np.multiply(dt1*(num_loc_ones*(1-alpha)),np.divide(Te3,(num_loc_ones*Z)));
        Erecs=dt1*np.divide(Tis3,(num_loc_ones*D));
        Ereca=dt1*np.divide(Tia3,(num_loc_ones*D));

        ESenter=max(ESenter,0);ESleft=max(ESleft,0);
        EEenter=max(EEenter,0);EEleft=max(EEleft,0);
        EIaenter=max(EIaenter,0);EIaleft=max(EIaleft,0);
        Eexps=max(Eexps,0);Eexpa=max(Eexpa,0);
        Einfs=max(Einfs,0);Einfa=max(Einfa,0);
        Erecs=max(Erecs,0);Ereca=max(Ereca,0);
       
        ##########stochastic version
        ESenter=np.random.poisson(ESenter);ESleft=np.random.poisson(ESleft);
        EEenter=np.random.poisson(EEenter);EEleft=np.random.poisson(EEleft);
        EIaenter=np.random.poisson(EIaenter);EIaleft=np.random.poisson(EIaleft);
        Eexps=np.random.poisson(Eexps);
        Eexpa=np.random.poisson(Eexpa);
        Einfs=np.random.poisson(Einfs);
        Einfa=np.random.poisson(Einfa);
        Erecs=np.random.poisson(Erecs);
        Ereca=np.random.poisson(Ereca);

        sk4=-Eexps-Eexpa+ESenter-ESleft;
        ek4=Eexps+Eexpa-Einfs-Einfa+EEenter-EEleft;
        isk4=Einfs-Erecs;
        iak4=Einfa-Ereca+EIaenter-EIaleft;
        ik4i=Einfs;
       
        ##########
        S[:,:,tcnt+1]=S[:,:,tcnt]+round(sk1/6+sk2/3+sk3/3+sk4/6);
        E[:,:,tcnt+1]=E[:,:,tcnt]+round(ek1/6+ek2/3+ek3/3+ek4/6);
        Is[:,:,tcnt+1]=Is[:,:,tcnt]+round(isk1/6+isk2/3+isk3/3+isk4/6);
        Ia[:,:,tcnt+1]=Ia[:,:,tcnt]+round(iak1/6+iak2/3+iak3/3+iak4/6);
        Incidence[:,:,tcnt+1]=round(ik1i/6+ik2i/3+ik3i/3+ik4i/6);
        obs=Incidence[:,:,tcnt+1];
    
    ##update x
    x[Sidx,:]=S[:,:,tcnt+1];
    x[Eidx,:]=E[:,:,tcnt+1];
    x[Isidx,:]=Is[:,:,tcnt+1];
    x[Iaidx,:]=Ia[:,:,tcnt+1];
    x[obsidx,:]=obs;
    ###update pop
    pop=pop-np.sum(M[:,:,ts],1).T*theta+np.sum(M[:,:,ts],2)*theta;
    minfrac=0.6;
    pop[pop<minfrac*pop0]=pop0[pop<minfrac*pop0]*minfrac;
                                                                      
    return x, pop