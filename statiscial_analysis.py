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


survey = cleaning.survey
#print(survey.describe)
#print(survey.dtypes)

print(survey.columns)
# Age ( histogram of whole survey)
survey['idade'] = survey['idade'].astype(str) 
a = plt.hist(survey['idade'],bins=20)

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





# H0: After COVID-19 there's <= 20.2% of the population investing in financial markets
# H1: After COVID-19 theres > 20.2% of the population investing in financial markets

dict_when_started_investing = {'Sim':  1,    'Não':  0  }
survey['investe_atualmente_no_mercado_financeiro'] = survey['investe_atualmente_no_mercado_financeiro'].map(dict_when_started_investing, na_action='ignore')

investing_survey = age_investment_nowadays.shape[0]
number_survey = survey.shape[0]
print('\nH0: After COVID-19 theres <= 20.2% of the population investing in financial markets ,\
 \nH1: After COVID-19 theres > 20.2% of the population investing in financial markets \n',proportions_ztest(investing_survey,number_survey,value=0.202,alternative='larger'))
investing_today = (investing_survey/number_survey)*100

print(f'\n There is {investing_today}% investing today in financial markets! \n')


# H0: Percentage of people investing before covid was <= 10,1%
# H1: Percentage of people investing before covid was > 10,1%


investing_before_covid = survey[survey['quando_começou_a_investir']=='Antes da pandemia ( Março de 2020 )']

print('\nH0: Percentage of people investing before covid was <= 10,1% ,\
 \nH1: Percentage of people investing before covid was > 10,1% \n',proportions_ztest(investing_before_covid.shape[0],number_survey,value=0.101,alternative='larger'))
invest_before_covid=(investing_before_covid.shape[0]/number_survey)*100

print(f'\nThere was {invest_before_covid}% investing before COVID-19\n')



# H0: Percentage of people that started investing after COVID-19 is <= 29.2%
# H1: Percentage of people that started investing after COVID-19 is > 29.2%


investing_after_covid = survey[survey['quando_começou_a_investir']=='Depois da pandemia']

print('\nH0: Percentage of people that started investing after COVID-19 is <= 29.2% ,\
 \nH1: Percentage of people that started investing after COVID-19 is > 29.2% \n',proportions_ztest(investing_after_covid.shape[0],number_survey,value=0.292,alternative='larger'))
invest_after_covid=(investing_after_covid.shape[0]/number_survey)*100

print(f'\nThere is {invest_after_covid}% investing after COVID-19\n')












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











#Correlation between age and when it started investing

#print('Correlation of Age and When did it started investing :',survey['idade'].corr(survey['quando_começou_a_investir'],method='pearson'))


# Populacao que consigo chegar / reach do mundo, nao consigo chegar a todos
# Sample aos que consigo chegar




