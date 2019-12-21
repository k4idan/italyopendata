#!/usr/bin/env python
from collections import OrderedDict
from recordlinkage.preprocessing import clean
import urllib.request
import json
import pprint
import rdflib
import pandas as pd
from tabula import read_pdf
import jellyfish
import sys

#package_list
pl = 'https://www.dati.gov.it/api/3/action/package_list' 
ps = 'http://www.dati.gov.it/api/3/action/package_show?id='

#key = search key, kind = L to use package_list e S to use package_show
#Use Web API for searching in dati.gov.it
def search(key, kind):
    # Make the HTTP request.
    while True:
        try:
            if kind == 'L':
                response = urllib.request.urlopen(pl)
            elif kind == 'S':
                response = urllib.request.urlopen(ps+key)
            else:
                raise ValueError("Parameter kind isn't valid")
            
            assert response.code == 200
            # Use the json module to load CKAN's response into a dictionary.
            response_dict = json.loads(response.read()) 
            # Check the contents of the response.
            assert response_dict['success'] is True
            result = response_dict['result']
            #pprint.pprint(result)
            if kind == 'L':
                matching = [s for s in result if key in s]
                #return the list of packages
                return matching
            elif kind == 'S':
                l = result['resources']
                matching = []
                for diz in l:    
                    matching.append(diz['url'])
                #return the content of a package
                return matching
        except ValueError:
            print("Parameter kind  have to be L or S. Try again")
    
#Check file format and open it. url = package url, index = index column
#Format accepted: csv, json, excel, txt, rdf and pdf
def ext(url, index=None):
    #Manage file formats
    if 'csv' in url:
        print('Found file in format: CSV')
        count = 0
        #Try to open with ; separator
        try:
            if isinstance(index,int):
                df = pd.read_csv(url, sep=";", engine='python', index_col=index)
            else:
                df = pd.read_csv(url, sep=";", engine='python', index_col=None)
            if df.empty==True:
                dfExist=False
            else:
                dfExist = True
                sep = ";"
                count = count+1
        #Check on encode/decode and Parser errors
        except UnicodeDecodeError:
            print("Decode Error")
            if isinstance(index,int):
                df = pd.read_csv(url, sep=";", encoding='latin-1', engine='python', index_col=index)
            else:
                df = pd.read_csv(url, sep=";", encoding='latin-1', engine='python', index_col=None)
        except UnicodeEncodeError:
            print("Encode Error")
            if isinstance(index,int):
                df = pd.read_csv(url, sep=";", encoding='latin-1', engine='python', index_col=index)
            else:
                df = pd.read_csv(url, sep=";", encoding='latin-1', engine='python', index_col=None)
        except pd.errors.ParserError: 
            print("Parser Error")
            dfExist = False
        
        #Try to open with comma separator
        try:
            if isinstance(index,int):
                dfcomma = pd.read_csv(url, sep=",", engine='python', index_col=index)
            else:
                dfcomma = pd.read_csv(url, sep=",", engine='python', index_col=None)
            if dfcomma.empty==True:
                dfcommaExist=False
            else: 
                dfcommaExist = True
                sep =","
                count = count+1
        except UnicodeDecodeError:
            print("Decode Error")
            if isinstance(index,int):
                dfcomma = pd.read_csv(url, sep=",", encoding='latin-1', engine='python', index_col=index)
            else:
                dfcomma = pd.read_csv(url, sep=",", encoding='latin-1', engine='python', index_col=None)
        except UnicodeEncodeError:
            print("Encode Error")
            if isinstance(index,int):
                dfcomma = pd.read_csv(url, sep=",", encoding='latin-1', engine='python', index_col=index)
            else:
                dfcomma = pd.read_csv(url, sep=",", encoding='latin-1', engine='python', index_col=None)
        except pd.errors.ParserError:
            dfcommaExist = False
        
        #Try to open with tab separator    
        try:
            if isinstance(index,int):
                dftab = pd.read_csv(url, sep="\t", engine='python', index_col=index)
            else:
                dftab = pd.read_csv(url, sep="\t", engine='python', index_col=None)
            if dftab.empty==True:
                dftabExist=False  
            else:
                dftabExist = True
                sep="\t"
                count = count+1
        except UnicodeDecodeError:
            print("Decode Error")
            if isinstance(index,int):
                dftab = pd.read_csv(url, sep="\t", encoding='latin-1', engine='python', index_col=index)
            else:
                dftab = pd.read_csv(url, sep="\t", encoding='latin-1',engine='python', index_col=None)
        except UnicodeEncodeError:
            print("Encode Error")
            if isinstance(index,int):
                dftab = pd.read_csv(url, sep="\t", engine='python', index_col=index)
            else:
                dftab = pd.read_csv(url, sep="\t", engine='python', index_col=None)
        except pd.errors.ParserError:
            dftabExist = False 
            
        #Try to open with whitespace separator    
        try:
            if isinstance(index,int):
                dfspace = pd.read_csv(url, sep=" ", engine='python', index_col=index)
            else:
                dfspace = pd.read_csv(url, sep=" ", engine='python', index_col=None)
            if dfspace.empty==True:
                dfspaceExist=False
            else: 
                dfspaceExist = True
                sep =" "
                count = count+1
        except UnicodeDecodeError:
            print("Decode Error")
            if isinstance(index,int):
                dfspace = pd.read_csv(url, sep=" ", encoding='latin-1', engine='python', index_col=index)
            else:
                dfspace = pd.read_csv(url, sep=" ", encoding='latin-1', engine='python', index_col=None)
        except UnicodeEncodeError:
            print("Encode Error")
            if isinstance(index,int):
                dfspace = pd.read_csv(url, sep=" ", encoding='latin-1', engine='python', index_col=index)
            else:
                dfspace = pd.read_csv(url, sep=" ", encoding='latin-1', engine='python', index_col=None)
        except pd.errors.ParserError:
            dfspaceExist = False
        
        #Manage CSV separators error
        if count == 0:
            sys.exit("Error: can't open this csv file. Exit")
        elif count > 1:
            print("There are " + str(count) + " good separators.")
            if dfExist==True:
                print("Separator ;") 
                pprint.pprint(df.head(1))
            if dfcommaExist==True :
                print("Separator ,") 
                pprint.pprint(dfcomma.head(1))
            if dftabExist==True:
                print("Separator tab") 
                pprint.pprint(dftab.head(1))
            if dfspaceExist==True :
                print("Separatore whitespace") 
                pprint.pprint(dfspace.head(1))
            sep = input("Insert the chosen separator (; , tab space): ")
            
        if sep==";":
            print("File opened correctly using the separator: ;")
            return df
        elif sep==",":
            print("File opened correctly using the separator: ,")
            return dfcomma
        elif sep=="tab":
            print("File opened correctly using the separator: tab")
            return dftab
        elif sep==" ":
            print("File opened correctly using the separator: whitespace")
            return dfspace
        else:
            print("The separator isn't valid")
    elif 'json' in url:
        print('Found file in format: JSON')
        df = pd.read_json(url)
    elif 'xml' in url:
        print('Found file in format: XML')
        if isinstance(index,int):
            df = pd.read_excel(url, encoding='utf-8',index_col=index)
        else:
            df = pd.read_excel(url, encoding='utf-8',index_col=None)
        return df
    elif 'xls' in url:
        print('Found file in format: XLS')
        if isinstance(index,int):
            df = pd.read_excel(url, encoding='utf-8',index_col=index)
        else:
            df = pd.read_excel(url, encoding='utf-8',index_col=None)
        return df
    elif 'rdf' in url:
        print('Found file in format: RDF')
        file = urllib.request.urlopen(url)
        g = rdflib.Graph()
        g.parse(file, format='xml')
        for stmt in g:
            pprint.pprint(stmt)
        return g
    elif 'pdf' in url:
        print('Found file in format: PDF')
        df = read_pdf(url)
        return df
    elif 'txt' in url:
        print('Found file in format: TXT')
        if isinstance(index,int):
            df = pd.read_csv(url, encoding='utf-8',index_col=index, sep = " ")
        else:
            df = pd.read_csv(url, encoding='utf-8',index_col=None, sep = " ")
    else:
        sys.exit("This format isn't supported. Exit")  

#Data Cleaning on records of each attribute of the dataset
#Parameters are Dataframe, Float (Jaro-Winkler treshold), True/False for User Option
def preprocess(df, th_jaro, user):
    for attr in df:
        try:
            df[attr] = clean(df[attr],remove_brackets='False')    
        except AttributeError: 
            #Pass when the attribute column doesn't contain string records 
            pass   
   
    #Delete multi-whitespace if They appear in the last part of a string
    for attr in df:
        for v in df[attr]:
            if str(v).endswith(" "):
                df[attr].replace(to_replace=str(str(v)),value=str(v).rstrip(" "),inplace=True) 

    firsts = []
    seconds = []   
    for attr in df:
        for v in df[attr]:   
            for b in df[attr]:  
                #Avoid digit records  
                if not any(c.isdigit() for c in str(v)):
                    if not any(d.isdigit() for d in str(b)):
                        #Use Jaro-Winkler algorithm for similarity
                        if jellyfish.jaro_winkler(str(v),str(b)) >= th_jaro and jellyfish.jaro_winkler(str(v),str(b)) < 1 :
                            if not ( (v in firsts and b in seconds) or (b in firsts and v in seconds) ):
                                firsts.append(v)
                                seconds.append(b)
                                
    #If user is True, user can choose what word keep
    if user == True:              
        print("There are " + str(len(firsts)) + " Related Words. Insert the number to choose what word keep (1 or 2 or 0 to skip)")
        for i in range(len(firsts)):
            num = input("1 for: " + "\"" + firsts[i] + "\"" + " o 2 for: " + "\"" + seconds[i] + "\"" + "\n")
            if num==str(1):
                for col in df:
                    df[col].replace(to_replace=str(seconds[i]),value=str(firsts[i]),inplace=True)
                print('Replaced ' + "\"" + str(seconds[i]) + "\"" + " with: " + "\"" + str(firsts[i]) + "\"")
            elif num==str(2):
                for col in df:
                    df[col].replace(to_replace=str(firsts[i]),value=str(seconds[i]),inplace=True)
                print('Replaced ' + "\"" + str(firsts[i]) + "\"" + " with: " + "\"" + str(seconds[i]) + "\"")
            else:
                pass
            i = i+1
    else: #If user is False, keep the first value
        for i in range(len(firsts)):
            for col in df:
                df[col].replace(to_replace=str(seconds[i]),value=str(firsts[i]),inplace=True) 
            print('Sostituito ' + "\"" + str(seconds[i]) + "\"" + " con: " + "\"" + str(firsts[i]) + "\"")
   
#Find similarity between attribute name of two datasets
#Parameters are DataFrame, DataFrame, Float (Similarity Treshold)
def header_linkage(left_df,right_df, treshold = 0.8):
    #Data Cleaning on attribute names
    left_df.columns = clean(left_df.columns,remove_brackets='False')
    right_df.columns = clean(right_df.columns,remove_brackets='False')
    left_header = list(left_df)
    right_header = list(right_df)
    print("Header left cleaned")
    print(list(left_df))
    print("Header right cleaned")
    print(list(right_df))
    left_keys = []
    right_keys = []
    #Record linkage with Jaro-Winkler algorithm
    for l_value in left_header:
        for r_value in right_header:
            if jellyfish.jaro_winkler(l_value, r_value) >= treshold:
                left_keys.append(l_value)
                right_keys.append(r_value)
                
    #print(keys)
    #Return arrays of similar left/right dataframe attribute names
    return left_keys,right_keys

#Check if a word is numeric
def isfloat(val):
    return all([ [any([i.isnumeric(), i in ['.','e']]) for i in val],  len(val.split('.')) == 2] )

#Find considerable words in columns of a dataset
#Parameters: DataFrame, Float (Occurences treshold), String Array, Float, True/False
def find_claims(df, treshold, stopword, th_jaro, user):
    preprocess(df, th_jaro, user)
    count = 0
    dicts = [dict() for count in range(len(df.columns))]
    for col in df:
        #Split records in words/values using whitespaces as separators
        for val in df[col]:
            val = str(val).split(" ")
            #Count word occurrences and insert the result in a dictionary
            for word in val:
                if word in dicts[count]:
                    dicts[count][word] = dicts[count][word]  + 1
                else:
                    dicts[count][word] = 1
        dicts[count] = OrderedDict(sorted(dicts[count].items(), key=lambda t: t[1], reverse=True))
        count = count + 1
        
    indMerge= []
    dizMerge = []
    for col in dicts:
        ind = []
        diz = {}
        for key in col.keys(): 
            #Don't count null values 
            if 'nan' not in key:    
                if 'nan' in col.keys():
                    den = (df.shape[0] - col['nan'])
                    #Filter numbers, stopwords and values with an occurences treshold minor than threshold
                    if len(str(key)) > 1 and not(str(key).isdigit()) and not(isfloat(str(key))) and str(key) not in stopword and col[str(key)]/den > treshold: 
                        ind.append(key)
                        diz[str(key)] = col[str(key)]/den
                else:
                    if len(str(key)) > 1 and not(str(key).isdigit()) and not(isfloat(str(key))) and str(key) not in stopword and col[str(key)]/df.shape[0] > treshold:
                        ind.append(key)
                        diz[str(key)] = col[str(key)]/df.shape[0]
        indMerge.append(ind)   
        dizMerge.append(diz)
    return indMerge, dizMerge

#Find similarity between words/values in two datasets
#Parameters are 2x DataFrame, 2x Float (Considerable tresholds), Float (Jaro-Winkler Treshold), True/False
#If User is true, user can choose between two similar records in conflict
def record_linkage(left_df,right_df,left_treshold = 0, right_treshold = 0, th_jaro = 0.944, user = True):
    stopword = ["a", "in" "adesso", "ai", "al", "alla", "allo", "allora", "altre", "altri", "altro", "anche", "ancora", "avere", "aveva", "avevano", "ben", "buono", "che", "chi", "cinque", "comprare", "con", "consecutivi", "consecutivo", "cosa", "cui", "da", "del", "della", "dello", "dentro", "deve", "devo", "di", "doppio", "due", "e", "ecco", "fare", "fine", "fino", "fra", "gente", "giu", "ha", "hai", "hanno", "ho", "il", "indietro    invece", "io", "la", "lavoro", "le", "lei", "lo", "loro", "lui", "lungo", "ma", "me", "meglio", "molta", "molti", "molto", "nei", "nella", "no", "noi", "nome", "nostro", "nove", "nuovi", "nuovo", "o", "oltre", "ora", "otto", "peggio", "pero", "persone", "piu", "poco", "primo", "promesso", "qua", "quarto", "quasi", "quattro", "quello", "questo", "qui", "quindi", "quinto", "rispetto", "sara", "secondo", "sei", "sembra    sembrava", "senza", "sette", "sia", "siamo", "siete", "solo", "sono", "sopra", "soprattutto", "sotto", "stati", "stato", "stesso", "su", "subito", "sul", "sulla", "tanto", "te", "tempo", "terzo", "tra", "tre", "triplo", "ultimo", "un", "una", "uno", "va", "vai", "voi", "volte", "vostro"]
    #Find considerable words for both datasets
    left_claims, left_weights = find_claims(left_df, left_treshold, stopword, th_jaro, user)
    right_claims, right_weights = find_claims(right_df, right_treshold, stopword, th_jaro, user)
    claims = []
    left_names = []
    right_names = []
    weights = []
    
    #Check if the same considerable word stays in both datasets
    for left_col in left_claims:
        for claim in left_col:
            for right_col in right_claims:
                if claim in right_col:
                    left_p = left_weights[left_claims.index(left_col)][claim]
                    right_p = right_weights[right_claims.index(right_col)][claim]
                    left_colname = str(list(left_df)[left_claims.index(left_col)])
                    right_colname = str(list(right_df)[right_claims.index(right_col)])              
                    print('The word ' + "\"" + str(claim) + "\"" ' stay in the attribute column of the left Dataset: ' + left_colname + ' with weight: ' + str(left_p) + ' and in the attribute column of the right Dataset: ' + right_colname + ' with weight: ' + str(right_p) )
                    totP = left_p + right_p
                    claims.append(claim)
                    left_names.append(left_colname)
                    right_names.append(right_colname)
                    weights.append(totP)
    
    #Make a structure ordered by weights                    
    clrw = sorted(zip(claims,left_names,right_names,weights),key=lambda x: x[3],reverse=True)
    print(clrw)
    left_exist = []
    right_exist = []
    
    for row in clrw:
        for i in range(clrw.index(row)+1,len(clrw)):
            #print(i,len(clrw),row[1],clrw[i][1])
            if row[1] not in left_exist and row[2] not in right_exist:
                left_exist.append(row[1])
                right_exist.append(row[2])
    
    #Return two structures formed by: considerable word, left and right column name, weight of the word            
    return left_exist, right_exist      

#Parameters: 4x Arrays
#Merge results from header linkage and record linkage functions
def merge_keys(left_keys,left_records,right_keys,right_records):
    for row in left_records:
        if row not in left_keys:
            left_keys.append(row)
    for row in right_records:
        if row not in right_keys:
            right_keys.append(row)
            
    return left_keys, right_keys
