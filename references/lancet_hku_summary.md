# [Nowcasting and Forecasting the potential domestic and international spread of the 2019-nCoV outbreak originating in Wuhan, China: a modeling study]
(https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30260-9/fulltext)

## Summary:
* Data from Dec 31, 2019 - Jan 28, 2020 on number of cases exported from Wuhan internationally to infer number of infections in Wuhan from Dec1 to Jan 25
* Used data on a monthly flight bookings, and data on human mobility from 300 prefectures in mainland China from Tencent
* Confirmed cases from Chinese CDC
* Reproductive number estimated using Markov Chain Monte Carlo methods and presented using posterior mean and 95% credible interval
Findings:
* Estimated basic reproductive number was 2.68 (95% Crl 2.47 - 2.86) and 75,815 (95% Crl 37304-130330)individuals have been infected in Wuhan
* Doubling time 6.4 days (5.8 - 7.1)


## Data sources and assumptions:
* Monthly  number of global flight bookings, daily number of domestic passengers recorded by location-based services of Tencent databae, domestic passenger volumes from and to Wuhan during Spring fesival estimated by Wuhan Transportation Management Bureau

* Used SEIR model to simulate the epidemic 
![](https://github.com/manishjt/covid19-nepal/edit/master/references/equations_lancethku.png?raw=true)S(t), E(t), I(t), and R(t) were the number of susceptible, latent, infectious, and removed individuals at time t; DE and DI were the mean latent (assumed to be the same as incubation) and infectious period (equal to the serial interval minus the mean latent period4
); R0 was the basic reproductive number; z(t) was the zoonotic force of infection equal to 86 cases per day in the baseline scenario before market closure on Jan 1, 2020, and equal to 0 thereafter. The cumulative number of infections and cases that had occurred in Greater Wuhan up to time t was obtained from the SEIR model.

* Assumed that travel behavior was not affected by disease and hence process  international case exportation occured according to a non-homogeneous process with rate lambda
![](https://github.com/manishjt/covid19-nepal/blob/master/references/travel_lancethku.png "Figure 2")



