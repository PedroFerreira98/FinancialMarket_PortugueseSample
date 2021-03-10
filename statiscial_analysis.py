# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 21:20:37 2021

@author: pedro
"""

from DataPreparation import cleaning
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import t
import numpy as np
from scipy.stats import normaltest
import numpy as np
from sklearn.preprocessing import PowerTransformer
import scipy
from scipy import stats
import scipy.stats as st
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import chi2_contingency


survey = cleaning.survey
#print(survey.describe)
#print(survey.dtypes)

print(survey.columns)
# Age ( histogram of whole survey)
survey['idade'] = survey['idade'].astype(int) 
a = plt.hist(survey['idade'],bins=7)

survey['idade'] = survey['idade'].astype(int) 
age = list(survey['idade'])


# 95% Confidence interval of the mean of age of the sample
age_inter = t(df = len(age)-1, 
            loc = np.mean(age),        
            scale = np.std(age)/np.sqrt(len(age))) 
print('\nMean of ages from the survey with 95% confidence interval:',age_inter.interval(0.95))


# 95% confidence interval of mean of ages thar are currently investing
age_investment_nowadays = survey[survey['investe_atualmente_no_mercado_financeiro']=='Sim']

age_now = list(age_investment_nowadays['idade'])
age_inter_now = t(df = len(age_now)-1, 
            loc = np.mean(age_now),        
            scale = np.std(age_now)/np.sqrt(len(age_now))) 
print('\nMean of ages that currently invest with 95% confidence interval:',age_inter_now.interval(0.95))
print('\n')





# H0: There's <= 20.2% of the population investing in financial markets
# H1: Theres > 20.2% of the population investing in financial markets

dict_when_started_investing = {'Sim':  1,    'Não':  0  }
survey['investe_atualmente_no_mercado_financeiro'] = survey['investe_atualmente_no_mercado_financeiro'].map(dict_when_started_investing, na_action='ignore')

investing_survey = age_investment_nowadays.shape[0]
number_survey = survey.shape[0]
print('\nH0: Theres <= 20.2% of the population investing in financial markets ,\
 \nH1: Theres > 20.2% of the population investing in financial markets \n',proportions_ztest(investing_survey,number_survey,value=0.202,alternative='larger'))
investing_today = (investing_survey/number_survey)*100

print(f'\n There is {investing_today}% investing today in financial markets! \n')


# H0: Percentage of people investing before covid was <= 10,1%
# H1: Percentage of people investing before covid was > 10,1%


investing_before_covid = survey[survey['quando_começou_a_investir']=='Antes da pandemia ( Março de 2020 )']

print('\nH0: Percentage of people investing before covid was <= 10,1% ,\
 \nH1: Percentage of people investing before covid was > 10,1% \n',proportions_ztest(investing_before_covid.shape[0],number_survey,value=0.101,alternative='larger'))
invest_before_covid=(investing_before_covid.shape[0]/number_survey)*100

print(f'\nThere was {invest_before_covid}% investing before COVID-19\n')



# H0: Percentage of people that started investing after COVID-19 is <= 22.4%
# H1: Percentage of people that started investing after COVID-19 is > 22.4%


investing_after_covid = survey[survey['quando_começou_a_investir']=='Depois da pandemia']

print('\nH0: Percentage of people that started investing after COVID-19 is <= 22.4% ,\
 \nH1: Percentage of people that started investing after COVID-19 is > 22.4% \n',proportions_ztest(investing_after_covid.shape[0],number_survey,value=0.224,alternative='larger'))
invest_after_covid=(investing_after_covid.shape[0]/number_survey)*100

print(f'\nThere is {invest_after_covid}% investing after COVID-19\n')


print('Começou a investir depois COVID-19:',investing_after_covid.shape[0])

# Hipothesis testing that there is no association between age and whether it started investing before or after COVID-19

before_covid = survey[survey['quando_começou_a_investir']=='Antes da pandemia ( Março de 2020 )']
after_covid = survey[survey['quando_começou_a_investir']=='Depois da pandemia']



before = []
after = []

before.append((before_covid[before_covid['idade']<=25]).shape[0])
before.append((before_covid[        (before_covid['idade']>25)  & (before_covid['idade']<=35 )    ]   ).shape[0])
before.append((before_covid[before_covid['idade']>35]  ).shape[0])


after.append((after_covid[after_covid['idade']<=25]).shape[0])
after.append((after_covid[        (after_covid['idade']>25)  & (after_covid['idade']<=35 )    ]   ).shape[0])
after.append((after_covid[after_covid['idade']>35]  ).shape[0])

print(before)
print(after)


table=[[4,7],
            [5,3],
            [5,0]]


print('\nH0: There is no association between the two variables ( independents) ,\
 \nH1: There is association  \n', st.chi2_contingency(np.array(table) ) )
print('We get a p-value of 0.055 which tell us that with 95% confidence, there is no association between the two and if there is its minimal,\
      therefore it would be natural to think that there would be an association where there would be more young people starting after COVID-19 ,\
      however theres people of all ages starting investing after COVID-19 , stating that there might be a connection between COVID-19 and people start investing')

'''
pt = PowerTransformer(method='yeo-johnson')
test_age_norm = np.array(age_investment_nowadays['idade']).reshape(-1, 1)
pt.fit(test_age_norm)
transformed_data = pt.transform(test_age_norm)

k2, p = normaltest(test_age_norm)
k2_n, p_n = normaltest(transformed_data)

print(f'k:{k2},p:{p}')
print(f'k:{k2_n},p:{p_n}')

transformed_k2, transformed_p = normaltest(transformed_data)


'''

#survey['qual_o_tipo_de_investimentos_que_faz']=survey['qual_o_tipo_de_investimentos_que_faz'].astype('category')
#survey['investimentos'] =survey['qual_o_tipo_de_investimentos_que_faz'].cat.codes




print(survey.describe())



#Correlation between age and when it started investing

#print('Correlation of Age and When did it started investing :',survey['idade'].corr(survey['quando_começou_a_investir'],method='pearson'))


# Populacao que consigo chegar / reach do mundo, nao consigo chegar a todos
# Sample aos que consigo chegar




