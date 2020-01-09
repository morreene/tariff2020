import pandas as pd
import sqlite3

conn = sqlite3.connect("data.db")
hs= pd.read_sql('select * from hs',conn)













#%% TO DELETE OLD CODE 
#put hs description in json for autocomplete box 
#https://github.com/twitter/typeahead.js/blob/gh-pages/data/countries.json

conn = sqlite3.connect("site.db")
hs= pd.read_sql('select * from hs',conn)
#problem with decoding
hs['clean'] = hs['hs_desc'].str.strip()

hs['clean'] = hs['hs_desc'].map(lambda x: x.encode('unicode-escape').decode('utf-8'))
hs['clean'] = hs['clean'].str.replace('"','')
hs_list = hs['clean'].tolist()

with open("hs_desc_new.json", "w") as output:
    output.write(str(hs_list))        
    
    
file = open('hs_desc_new.txt', 'w')
i=0
for item in hs_list:
    if i >1000: break

    if ' ' in item:
        file.write('"%s",' % item)
    else:
        file.write("%s," % item)
    i = i +1
        
file.close()
