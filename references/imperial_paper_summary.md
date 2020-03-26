# [Impact of non-pharmaceutical interventions (NPIs) to reduce COVID-19 mortality and healthcare demand](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf)

NeilMFerguson, Daniel  Laydon,  Gemma  Nedjati-Gilani,Natsuko  Imai, Kylie  Ainslie, Marc  Baguelin, Sangeeta Bhatia, Adhiratha Boonyasiri,  Zulma Cucunubá,Gina Cuomo-Dannenburg,Amy Dighe, Ilaria Dorigatti, Han Fu, Katy Gaythorpe, Will Green, Arran Hamlet, Wes Hinsley,Lucy C Okell, Sabine van Elsland, Hayley Thompson, Robert Verity, Erik Volz, Haowei Wang, Yuanrong Wang, Patrick GT Walker,Caroline Walters,PeterWinskill, CharlesWhittaker, ChristlADonnelly, Steven Riley, AzraCGhani.

## Summary:
* Apply microsimulation model to UK and US
* Look at mitigation and suppression strategies
* Show that for US and UK - mitigation would reduce peak healthcare demand but would still result in hundereds of throusands of death and health care system being overwhelmed
* Suppression is better but might need to do it long term (18 months) until vaccine is available

## Background:

**Suppression strategy**: Reduce the reproduction number R to below 1 -> reduce case numbers to low level. Ideally eliminate human to human transmissions 

**Mitigation strategy**: Reduce peak, but build population immunity which leads to evential rapid decline in case numbers. Reduce R, but not to below 1

## Transmission model:
* Modified individual-based simulation model developed to support influenza planning
* Individuals reside in areas of high-resolution pop density
* Contacts are made within household, school, workplace and community.
 1/3 transmission in household, 1/3 in schools and workplaces, 1/3 in community
* Incubation period 5.1 days
* Infectiousness - 12 hrs prior to onset of symptoms for sympotamtic, 4.6 days after infection in asymptomatic people
* R0 = 2.4, but examine values between 2.0 and 2.6. Symptomatic individuals are 50% more infectious
* Infectiousness is a gamma distribution -> mean 1, shape parameter alpha=0.25
* Disease Progression and Healthcare Demand
  * 40-50% infection were not identified as cases
  * 2/3 cases are symptomatic enough to self isolate
  * Have estimates by age (Table 1)


## NPI Scenarios
5 different interventions:
1. Case isolation at home (Reduce non household contacts by 75%, 70% comply)
2. Voluntary home quarantine (household contact rates double, community, workplace/school reduce by 75%, 50% comply)
3. Social distancing (community contact reduce 75%, school unchange, workplace reduce by 25%, household increase by 25%)
4. Closure of schools (all schools close, 25% universities open. Household contact increase by 50%, community contact decrease by 25%)


## Results
With largely conservative assumptions:
* Without intervention - peak mortality in 3 months, 81% of population will get infected. 510,000 deaths in Great Britain, and 2.2 million in US (not accounting for effects of overwhelmed health system)
* Fig 2: shows result of different mitigation strategies
* Most effective mitigation = a combination of case isolation, home quarantine, and social distancing of those most at risk. Table 3 has more details
* However mitigation not sufficient, suppression necessary to not overwhelm healthcare system