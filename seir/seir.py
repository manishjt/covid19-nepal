import numpy as np

def SEIR(x, M , pop, ts, pop0):
    ''' Input description:
        x: state variables for each ensemble (6*375, 300)
        M: mobility matrix (375, 375, 14)
        pop: population matrix (375, 1)
        ts: timestep
        pop0: inintial population
        375 = number of nodes
        300 = number of ensembles
        6 = number of states
    '''


    #the metapopulation SEIR model
    print("In SEIR")
    dt = 1
    tmstep = 1

    #integrate forward for one day
    num_loc = pop.shape[0];
    num_ens = x.shape[1];

    #S,E,Is,Ia,obs,...,beta,mu,theta,Z,alpha,D
    #TODO: check 0 indexing
    Sidx = np.array(range(0,  5*num_loc, 5));
    Eidx = np.array(range(1,  5*num_loc, 5));
    Isidx = np.array(range(2, 5*num_loc, 5));
    Iaidx = np.array(range(3, 5*num_loc, 5));
    obsidx = np.array(range(4,5*num_loc, 5));

    betaidx = 5*num_loc;
    muidx=5*num_loc + 1;
    thetaidx=5*num_loc + 2;
    Zidx=5*num_loc + 3;
    alphaidx=5*num_loc + 4;
    Didx=5*num_loc + 5;

    S=np.zeros((num_loc,num_ens,tmstep+1));
    E=np.zeros((num_loc,num_ens,tmstep+1));
    Is=np.zeros((num_loc,num_ens,tmstep+1));
    Ia=np.zeros((num_loc,num_ens,tmstep+1));
    Incidence=np.zeros((num_loc,num_ens,tmstep+1));
    obs=np.zeros((num_loc,num_ens));

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
    #print(range(ts+dt, dt, ts+tmstep))
    for t in range(ts+dt,ts+tmstep+1, dt):
        dt1=dt;
        #first step
        M_ts = M[:,:,ts]
        S_tcnt = S[:,:,tcnt]
        Ia_tcnt = Ia[:,:,tcnt]
        Is_tcnt = Is[:,:,tcnt]
        E_tcnt = E[:, :, tcnt]

        dt_theta = dt1*(np.ones((num_loc,1)) * theta)
        temp2 = (pop-Is_tcnt)

        sum_Mts = np.sum(M_ts,0).reshape(M_ts.shape[0],1)
        ESenter=np.multiply(dt_theta,
                            np.matmul(M_ts,np.divide(S_tcnt,temp2)));
        ESleft=np.minimum(np.multiply((dt_theta),
                           np.multiply(np.divide(S_tcnt,temp2),np.matmul(sum_Mts,np.ones((1,num_ens))))),
                      dt1*S_tcnt);

        EEenter=np.multiply(dt_theta,
                            np.matmul(M_ts,np.divide(E_tcnt,temp2)));
        EEleft=np.minimum(np.multiply(dt_theta,
                          np.multiply(np.divide(E_tcnt,temp2),np.matmul(sum_Mts,np.ones((1,num_ens))))),
                      dt1*E_tcnt);

        EIaenter= np.multiply(dt_theta,
                              np.matmul(M_ts,np.divide(Ia_tcnt,temp2)));
        EIaleft=np.minimum(np.multiply(dt_theta,
                            np.multiply(np.divide(Ia_tcnt,temp2),np.matmul(sum_Mts,np.ones((1,num_ens))))),
                            dt1*Ia_tcnt);


        Eexps=np.divide(dt1*np.multiply((np.ones((num_loc,1))*beta),np.multiply(S_tcnt,Is_tcnt)),pop);

        Eexpa=np.divide(np.multiply(dt1*(np.ones((num_loc,1))*mu),
                                    np.multiply((np.ones((num_loc,1))*beta),
                                                np.multiply(S_tcnt,Ia_tcnt))),
                        pop);

        Einfs=np.divide(dt1*np.multiply((np.ones((num_loc,1))*alpha),E_tcnt),(np.ones((num_loc,1))*Z));
        Einfa=np.divide(dt1*np.multiply((np.ones((num_loc,1))*(1-alpha)),E_tcnt),(np.ones((num_loc,1))*Z));
        Erecs=dt1*np.divide(Is_tcnt,(np.ones((num_loc,1))*D));
        Ereca=dt1*np.divide(Ia_tcnt,np.ones((num_loc,1))*D);


        ESenter=np.maximum(ESenter,np.zeros(ESenter.shape));
        ESleft=np.maximum(ESleft,np.zeros(ESleft.shape));
        EEenter=np.maximum(EEenter,np.zeros(EEenter.shape));
        EEleft=np.maximum(EEleft,np.zeros(EEleft.shape));
        EIaenter=np.maximum(EIaenter,np.zeros(EIaenter.shape));
        EIaleft=np.maximum(EIaleft,np.zeros(EIaleft.shape));
        Eexps=np.maximum(Eexps,np.zeros(Eexps.shape));
        Eexpa=np.maximum(Eexpa,np.zeros(Eexpa.shape));
        Einfs=np.maximum(Einfs,np.zeros(Einfs.shape));
        Einfa=np.maximum(Einfa,np.zeros(Einfa.shape));
        Erecs=np.maximum(Erecs,np.zeros(Erecs.shape));
        Ereca=np.maximum(Ereca,np.zeros(Ereca.shape));

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
        temp4 = np.matmul(sum(M_ts, 0).reshape(M_ts.shape[0],1),np.ones((1,num_ens)))
        ESenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Ts1,temp3)));
        ESleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Ts1,temp3)),temp4),dt1*Ts1);
        EEenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Te1,temp3)));
        EEleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Te1,temp3)),temp4),dt1*Te1);
        EIaenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Tia1,temp3)));
        EIaleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Tia1,temp3)),temp4),dt1*Tia1);

        num_loc_ones = np.ones((num_loc, 1))
        Eexps=np.multiply(dt1*(num_loc_ones*beta),
                          np.multiply(Ts1, np.divide(Tis1,pop)));
        Eexpa=np.multiply(dt1*(num_loc_ones*mu),
                          np.multiply(np.multiply((num_loc_ones*beta),Ts1),
                                      np.divide(Tia1,pop)));
        Einfs=np.multiply(dt1*(num_loc_ones*alpha),np.divide(Te1,(num_loc_ones*Z)));
        Einfa=np.multiply(dt1*(num_loc_ones*(1-alpha)),np.divide(Te1,(num_loc_ones*Z)));
        Erecs=dt1*np.divide(Tis1,(num_loc_ones*D));
        Ereca=dt1*np.divide(Tia1,(num_loc_ones*D));

        ESenter=np.maximum(ESenter,np.zeros(ESenter.shape));
        ESleft=np.maximum(ESleft,np.zeros(ESleft.shape));
        EEenter=np.maximum(EEenter,np.zeros(EEenter.shape));
        EEleft=np.maximum(EEleft,np.zeros(EEleft.shape));
        EIaenter=np.maximum(EIaenter,np.zeros(EIaenter.shape));
        EIaleft=np.maximum(EIaleft,np.zeros(EIaleft.shape));
        Eexps=np.maximum(Eexps,np.zeros(Eexps.shape));
        Eexpa=np.maximum(Eexpa,np.zeros(Eexpa.shape));
        Einfs=np.maximum(Einfs,np.zeros(Einfs.shape));
        Einfa=np.maximum(Einfa,np.zeros(Einfa.shape));
        Erecs=np.maximum(Erecs,np.zeros(Erecs.shape));
        Ereca=np.maximum(Ereca,np.zeros(Ereca.shape));
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
        temp6 = np.matmul(sum(M_ts, 0).reshape(M_ts.shape[0],1),np.ones((1,num_ens)))
        ESenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Ts2,temp5)));
        ESleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Ts2,temp5)),temp6),dt1*Ts2);
        EEenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Te2,temp5)));
        EEleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Te2,temp5)),temp6),dt1*Te2);
        EIaenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Tia2,temp5)));
        EIaleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Tia2,temp5)),temp6),dt1*Tia2);

        num_loc_ones = np.ones((num_loc, 1))
        Eexps=np.multiply(dt1*(num_loc_ones*beta),
                          np.multiply(Ts2, np.divide(Tis2,pop)));
        Eexpa=np.multiply(dt1*(num_loc_ones*mu),
                          np.multiply(np.multiply((num_loc_ones*beta),Ts2),
                                      np.divide(Tia2,pop)));
        Einfs=np.multiply(dt1*(num_loc_ones*alpha),np.divide(Te2,(num_loc_ones*Z)));
        Einfa=np.multiply(dt1*(num_loc_ones*(1-alpha)),np.divide(Te2,(num_loc_ones*Z)));
        Erecs=dt1*np.divide(Tis2,(num_loc_ones*D));
        Ereca=dt1*np.divide(Tia2,(num_loc_ones*D));


        ESenter=np.maximum(ESenter,np.zeros(ESenter.shape));
        ESleft=np.maximum(ESleft,np.zeros(ESleft.shape));
        EEenter=np.maximum(EEenter,np.zeros(EEenter.shape));
        EEleft=np.maximum(EEleft,np.zeros(EEleft.shape));
        EIaenter=np.maximum(EIaenter,np.zeros(EIaenter.shape));
        EIaleft=np.maximum(EIaleft,np.zeros(EIaleft.shape));
        Eexps=np.maximum(Eexps,np.zeros(Eexps.shape));
        Eexpa=np.maximum(Eexpa,np.zeros(Eexpa.shape));
        Einfs=np.maximum(Einfs,np.zeros(Einfs.shape));
        Einfa=np.maximum(Einfa,np.zeros(Einfa.shape));
        Erecs=np.maximum(Erecs,np.zeros(Erecs.shape));
        Ereca=np.maximum(Ereca,np.zeros(Ereca.shape));

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
        temp6 = np.matmul(sum(M_ts, 0).reshape(M_ts.shape[0],1),np.ones((1,num_ens)))
        ESenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Ts3,temp5)));
        ESleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Ts3,temp5)),temp6),dt1*Ts3);
        EEenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Te3,temp5)));
        EEleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Te3,temp5)),temp6),dt1*Te3);
        EIaenter=np.multiply(dt_theta,np.matmul(M_ts,np.divide(Tia3,temp5)));
        EIaleft=np.minimum(np.multiply(np.multiply(dt_theta,np.divide(Tia3,temp5)),temp6),dt1*Tia3);

        num_loc_ones = np.ones((num_loc, 1))
        Eexps=np.multiply(dt1*(num_loc_ones*beta),
                          np.multiply(Ts3, np.divide(Tis3,pop)));
        Eexpa=np.multiply(dt1*(num_loc_ones*mu),
                          np.multiply(np.multiply((num_loc_ones*beta),Ts3),
                                      np.divide(Tia3,pop)));
        Einfs=np.multiply(dt1*(num_loc_ones*alpha),np.divide(Te3,(num_loc_ones*Z)));
        Einfa=np.multiply(dt1*(num_loc_ones*(1-alpha)),np.divide(Te3,(num_loc_ones*Z)));
        Erecs=dt1*np.divide(Tis3,(num_loc_ones*D));
        Ereca=dt1*np.divide(Tia3,(num_loc_ones*D));

        ESenter=np.maximum(ESenter,np.zeros(ESenter.shape));
        ESleft=np.maximum(ESleft,np.zeros(ESleft.shape));
        EEenter=np.maximum(EEenter,np.zeros(EEenter.shape));
        EEleft=np.maximum(EEleft,np.zeros(EEleft.shape));
        EIaenter=np.maximum(EIaenter,np.zeros(EIaenter.shape));
        EIaleft=np.maximum(EIaleft,np.zeros(EIaleft.shape));
        Eexps=np.maximum(Eexps,np.zeros(Eexps.shape));
        Eexpa=np.maximum(Eexpa,np.zeros(Eexpa.shape));
        Einfs=np.maximum(Einfs,np.zeros(Einfs.shape));
        Einfa=np.maximum(Einfa,np.zeros(Einfa.shape));
        Erecs=np.maximum(Erecs,np.zeros(Erecs.shape));
        Ereca=np.maximum(Ereca,np.zeros(Ereca.shape));

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
        S[:,:,tcnt+1]=S[:,:,tcnt]+np.round(sk1/6+sk2/3+sk3/3+sk4/6);
        E[:,:,tcnt+1]=E[:,:,tcnt]+np.round(ek1/6+ek2/3+ek3/3+ek4/6);
        Is[:,:,tcnt+1]=Is[:,:,tcnt]+np.round(isk1/6+isk2/3+isk3/3+isk4/6);
        Ia[:,:,tcnt+1]=Ia[:,:,tcnt]+np.round(iak1/6+iak2/3+iak3/3+iak4/6);
        Incidence[:,:,tcnt+1]=np.round(ik1i/6+ik2i/3+ik3i/3+ik4i/6);
        obs=Incidence[:,:,tcnt+1];
        tcnt=tcnt+1;
        print("Seir iteration:", t)
    np.save('output/seir_s_'+str(ts)+'.npz', S)
    np.save('output/seir_e_'+str(ts)+'.npz', E)
    np.save('output/seir_is_'+str(ts)+'.npz', Is)
    np.save('output/seir_ia_'+str(ts)+'.npz', Ia)
    np.save('output/seir_incidence_'+str(ts)+'.npz', Incidence)
    np.save('output/seir_obs_'+str(ts)+'.npz', obs)

    ##update x
    x[Sidx,:]=S[:,:,tcnt];
    x[Eidx,:]=E[:,:,tcnt];
    x[Isidx,:]=Is[:,:,tcnt];
    x[Iaidx,:]=Ia[:,:,tcnt];
    x[obsidx,:]=obs;
    ###update pop


    M_sum0 = np.sum(M[:,:,ts],0); M_sum0 = M_sum0.reshape(M_sum0.shape[0],1)
    M_sum1 = np.sum(M[:,:,ts],1); M_sum1 = M_sum1.reshape(1,M_sum1.shape[0])
    theta = theta.reshape(theta.shape[0],1)
    #rint(M_sum0.shape, M_sum1.shape, theta.shape, pop.shape)
    pop=pop-M_sum0*theta.T+M_sum1.T*theta.T;
    minfrac=0.6;
    pop[pop<minfrac*pop0]=pop0[pop<minfrac*pop0]*minfrac;

    return x, pop
