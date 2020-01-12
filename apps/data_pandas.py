import pandas as pd
import sqlite3

cnx = sqlite3.connect("../data.db")
hs= pd.read_sql('select * from hs',cnx)

df_rate = pd.read_sql_query("SELECT * FROM rate", cnx)
df_type = pd.read_sql_query("SELECT * FROM type", cnx)
sqlite_desc = pd.read_sql_query("SELECT * FROM desc", cnx)


# use data
IMPORTER = '156'
EXPORTER = '418' # Laos
HS = '100620'

data_rate = df_rate[(df_rate['reporter']==IMPORTER) & (df_rate['hs'].str[0:6]==HS)]
data_regi = df_type[(df_type['reporter']==IMPORTER) & (df_type['partner']==EXPORTER)]
result = pd.merge(data_rate, data_regi, on=['reporter','type_code'])







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
