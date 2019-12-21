# italyopendata
Tecniche Analitiche per Open Data

Indice
	1. Documentazione
	2. Dati d Prova
	3. Istruzioni
	
1. Documentazione

Il progetto contiene tre moduli:
	
	a. opendatigov, che contiene la libreria sviluppata. 
	b. mafia, che contiene il "Test su Beni Confiscati alla Mafia".
	c. musei, che contiene il "Test su Anagrafica Museale".
	
Tutte le funzioni in "a" sono commentate all'interno del codice sorgenti con relativi commenti esplicativi. Si specificano sotto le funzioni principali utilizzabili dall'utente, escludendo i sub-metodi utilizzati da esse:

	- def search(key, kind): 
		#key = search key, kind = L to use package_list e S to use package_show
		#Use Web API for searching in dati.gov.it
	- def ext(url, index=None):
		#Check file format and open it. url = package url, index = index column
		#Format accepted: csv, json, excel, txt, rdf and pdf
	- def header_linkage(left_df,right_df, treshold = 0.8):
		#Find similarity between attribute name of two datasets
		#Parameters are DataFrame, DataFrame, Float (Similarity Treshold)
	- def record_linkage(left_df,right_df,left_treshold = 0, right_treshold = 0, th_jaro = 0.944, user = True):
		#Find similarity between words/values in two datasets
		#Parameters are 2x DataFrame, 2x Float (Considerable tresholds), Float (Jaro-Winkler Treshold), True/False
		#If User is true, user can choose between two similar records in conflict
	- def merge_keys(left_keys,left_records,right_keys,right_records): 
		#Parameters: 4x Arrays
		#Merge results from header linkage and record linkage functions

2. Dati di Prova

Il progetto contiene tre moduli e due sotto-cartelle

	d. la cartella "mafia" e "musei", che contengono:
		- i file csv "input" per la prova anche in locale;
		- i file csv generati dal modulo;
		- il file excel con un riassunto di tutta l'evoluzione dei dataset divisa per fogli.
		- il file compresso con tutti i dati cui sopra. Utile nel caso in cui siano sovrascritti i file durante la compilazione.

3. Istruzioni

I test "b" e "c" contengono tutti il necessario per essere compilati. Infatti, basta compilare i relativi moduli "mafia.py" o "musei.py" per eseguirli. Nello specifico: 

	- il test "b" utilizza i dati di prova contenuti nella cartella "mafia" al fine di riuscire a provare il progetto anche nel caso in cui il portale dati.gov.it sia down o ci siano problemi di connessione. 
	- Il test "c", invece, richiama le Web API del portale. Di conseguenza, è necessaria una connessione internet.
	
Infine, è possibile provare i metodi contenuti in "a" semplicemente importandole nei progetti.

