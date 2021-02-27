import pandas as pd
import re


#Loading raw survey
raw_survey=pd.read_csv(r'c:/Users/pedro/Desktop/FinancialMarket_PortugueseSample/Mercado Financeiro_ Impacto da COVID-19 nos hábitos dos Portugueses .csv')

#Removing timestamp colum, we dont need it, just noise in data
survey = raw_survey.drop(labels='Timestamp',axis=1)



#Remove spaces, and question marks in columns labels
survey.columns= [ re.sub('\s+','_',(re.sub('\?','',name).strip())).lower() for name in survey.columns]


#Manually chaning some values that were not in the format we want
survey.loc[44, "idade"] = 26

#We assume here that when the person puts a range of numbers that the estimation is the mean of the two values
survey.loc[5, "qual_o_retorno_em_%(percentagem)_que_espera_ter_anualmente"] = 7.5
survey.loc[17, "qual_o_retorno_em_%(percentagem)_que_espera_ter_anualmente"] = 15
survey.loc[41, "qual_o_retorno_em_%(percentagem)_que_espera_ter_anualmente"] = 17.5
survey.loc[44, "qual_o_retorno_em_%(percentagem)_que_espera_ter_anualmente"] = 8.5



#Lower case this two columns as well as removing spaces

survey['cidade']= survey['cidade'].str.lower()
survey['cidade']= survey['cidade'].str.strip()


survey['país']= survey['país'].str.lower()
survey['país']= survey['país'].str.strip()

#normalizing single cases that were detected
survey.replace({'cidade': {'cacais': 'cascais', 'setúbal': 'setubal'}},inplace=True)

#removing percentage simbols 
survey['qual_o_retorno_em_%(percentagem)_que_espera_ter_anualmente'] = survey['qual_o_retorno_em_%(percentagem)_que_espera_ter_anualmente'].str.replace(r'%', '')



#dataframe with one hot encoding for all the platforms, a person can use more than one platform
platform= pd.DataFrame(survey['qual_a_plataforma_que_usa_para_investir'])
platform['qual_a_plataforma_que_usa_para_investir'] = [x.replace(r';',',') for x in platform['qual_a_plataforma_que_usa_para_investir'] ]
platform=platform['qual_a_plataforma_que_usa_para_investir'].str.get_dummies(sep=',')


#dataframe with one hot encoding for the type of investments of the person, they might have several
investments = pd.DataFrame(survey['qual_o_tipo_de_investimentos_que_faz'])
investments=investments['qual_o_tipo_de_investimentos_que_faz'].str.get_dummies(sep=';')


#dataframe with one hot encoding for the type of investments of the person 
reason = pd.DataFrame(survey['qual_a_razão_para_ter_começado_em_investir'])
reason=reason['qual_a_razão_para_ter_começado_em_investir'].str.get_dummies(sep=';')



#I might need to have everything in the same dataframe
#survey = pd.concat([survey.drop('qual_a_plataforma_que_usa_para_investir',1),platform],1)

