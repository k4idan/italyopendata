'''
Created on 20 dic 2018

@author: Antonino
'''
import opendatagov as odg
import os
import pprint
import pandas as pd
from opendatagov import record_linkage, merge_keys

key = "mafia"

#ds = odg.search(key,'L')
#pprint.pprint(ds)

#User chooses the dataset, that wants to explore 
#Download from the web portal
#left_urls = odg.search(ds[2],'S')
#pprint.pprint(left_urls)
#right_urls = odg.search(ds[3],'S')
#pprint.pprint(right_urls)

#Use a batch dataset
#left_url = "mafia/input_mafia_left.csv"
left_url = "mafia/input_mafia_left.csv"
right_url = "mafia/input_mafia_right.csv"

#left_df = odg.ext(left_urls[0],index=0)
#right_df = odg.ext(right_urls[0],index=0)
#left_df = odg.ext(left_url,index=0)
right_df = odg.ext(right_url,index=0)
left_df = odg.ext(left_url,index=0)

#Make a directory and save datasets
if not os.path.exists(str(key)):
    os.makedirs(str(key))
left_df.to_csv(str(key)+'/mafia_left.csv')
right_df.to_csv(str(key)+'/mafia_right.csv')

left_keys,right_keys = odg.header_linkage(left_df,right_df)
print('Attributes found in header linkage are (First Dataset Attribute e Second Dataset Attribute):')
print(left_keys,right_keys)
#print(right_df.columns)

#left_claims, left_weights = odg.find_claims(left_df, soglia)
#right_claims, right_weights = odg.find_claims(right_df, soglia)
# pprint.pprint(left_claims)
# pprint.pprint(right_claims)
# pprint.pprint(left_weights)
# pprint.pprint(right_weights)

#Treshold values are zero by default
left_records,right_records = record_linkage(left_df,right_df, user=True)
#print('Attributes found in record linkage are (Considerable Word, First Dataset Attribute, Second Dataset Attribute, Weight):')
#print(records)
print("Attribute names found in record linkage are:")
print(left_records,right_records)

left_result, right_result = merge_keys(left_keys,left_records,right_keys,right_records)
res_dic = dict(zip(left_result, right_result))
print('Recommend concatenating from datasets, attributes:')
#Eventually manual modification of the dictionary can occur here (ex. remove a key-value element)
print(res_dic)

#Save Cleaned Datasets            
left_df.to_csv(str(key)+'/mafia_new_left.csv')
right_df.to_csv(str(key)+'/mafia_new_right.csv')

#Change column name from left dataset and concatenate 
renamed_left_df = left_df.rename(columns=res_dic)
renamed_left_df.to_csv(str(key)+'/mafia_renamed_left.csv')

result = pd.concat([renamed_left_df,right_df], keys=['Milano','Catania'], sort=True)
#Save result merged dataset
result.to_csv(str(key)+'/mafia_result.csv')  
print("New dataset: mafia_result.csv created.")