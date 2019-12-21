'''
Created on 08 gen 2019

@author: Antonino
'''
import opendatagov as odg
import os
import pprint
import pandas as pd

key = "musei"

ds = odg.search(key,'L')
pprint.pprint(ds)

left_ind = ds.index("elenco-dei-musei-lazio")
right_ind = ds.index("musei-gallerie-siti-archeologici")

#User chooses the dataset, that wants to explore 
left_urls = odg.search(ds[left_ind],'S')
right_urls = odg.search(ds[right_ind],'S')

left_df = odg.ext(left_urls[2])
right_df = odg.ext(right_urls[0])

#Make a directory and save datasets
if not os.path.exists(str(key)):
    os.makedirs(str(key))

left_df.to_csv(str(key)+'/musei_left.csv')
right_df.to_csv(str(key)+'/musei_right.csv')

#Set treshold to 0.75
left_keys,right_keys = odg.header_linkage(left_df,right_df, 0.75)
print('Attributes found in header linkage are (First Dataset Attribute e Second Dataset Attribute):')
print(left_keys,right_keys)

#Set both tresholds to 0.1 and Jaro-Winkler treshold to 0.98
left_records,right_records = odg.record_linkage(left_df,right_df, 0.1, 0.1, th_jaro = 0.98, user = True)
print("Attribute names found in record linkage are:")
print(left_records,right_records)

left_result, right_result = odg.merge_keys(left_keys,left_records,right_keys,right_records)
res_dic = dict(zip(left_result, right_result))
print('Recommend concatenating from datasets, attributes:')
#Eventually manual modification of the dictionary can occur here (ex. remove a key-value element)
print(res_dic) 

#Save Cleaned Datasets    
left_df.to_csv(str(key)+'/musei_new_left.csv')
right_df.to_csv(str(key)+'/musei_new_right.csv')

#Change column name from left dataset and concatenate 
renamed_left_df = left_df.rename(columns=res_dic)
renamed_left_df.to_csv(str(key)+'/musei_renamed_left.csv')

result = pd.concat([renamed_left_df,right_df], keys=['Lazio','Sicilia'], sort=True)
#Save result merged dataset
result.to_csv(str(key)+'/musei_result.csv')  
print("New dataset: musei_result.csv created.")