import pandas as pd
import sqlalchemy
import urllib
import sqlite3

params_sql = urllib.parse.quote("DRIVER={SQL Server};SERVER=ADA-MSSQL-IDB;DATABASE=reference_database;UID=;PWD=")
cn_ref = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params_sql)

params_idb = urllib.parse.quote("DRIVER={SQL Server};SERVER=ADA-MSSQL-IDB;DATABASE=IDB;UID=;PWD=")
cn_idb = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params_idb)

# Countries to be extracted from SQL
countries = ['156','840']

#%% Create connection to SQLite; read existing data

cnx = sqlite3.connect('site.db')
sqlite_rate = pd.read_sql_query("SELECT * FROM rate", cnx)
sqlite_type = pd.read_sql_query("SELECT * FROM type", cnx)
sqlite_desc = pd.read_sql_query("SELECT * FROM desc", cnx)

#%% SQL Server

# Find the latest year
str_sql= "SELECT Reporter, Year FROM Inventory"
inventory = pd.read_sql(str_sql, cn_idb)
inventory = inventory.groupby('Reporter')['Year'].max().reset_index()
country_year = inventory[inventory['Reporter'].isin(countries)][['Reporter','Year']]

# countries and latest year to be extracted
country_year = [tuple(x) for x in country_year.values]

#%%
df_rate = pd.DataFrame()
df_type = pd.DataFrame()
df_desc = pd.DataFrame()

for cy in country_year:
#    cy=('156','2017')
#    cy=('840','2019')
    # TC
    str_sql= "SELECT [Reporter] AS reporter,[Year] AS year,[TL],[TLS],[Duty Type],[Duty Code],[Partner],"+\
             "[AV Duty Rate] AS rate_av,[Specific Duty Rate] AS rate_nav FROM [TC] "+\
             "WHERE [Record Status]<>'D' AND [Reporter]=" + cy[0] + "AND [Year]=" + cy[1]
    tc = pd.read_sql(str_sql, cn_idb)
    tc['hs'] = tc['TL'] + '-' + tc['TLS']
    tc['hs'] = tc['hs'].str[0:-3]
    tc['type_code'] = tc['reporter'] + '-' + tc['Duty Type'] + tc['Duty Code']
    tc['type_code'] = tc['type_code'].str.strip()
    tc = tc[['reporter','year','hs','type_code','rate_av','rate_nav']]
    df_rate = df_rate.append(tc, sort=True)

    #TT
    str_sql= "SELECT [Reporter] AS reporter,[Year] AS year,[TL],[TLS],[Description] AS description FROM [TT] "+\
             "WHERE [Reporter]=" + cy[0] + "AND [Year]=" + cy[1]
    tt = pd.read_sql(str_sql, cn_idb)
    tt['hs'] = tt['TL'] + '-' + tt['TLS']
    tt['hs'] = tt['hs'].str[0:-3]
    tt = tt[['reporter','year','hs','description']]
    df_desc = df_desc.append(tt, sort=True)

    # Partner & Partner Group
    str_sql= "SELECT [Reporter] AS reporter,[Year] AS year,[Code] AS type_code,[WTO Code] AS partner FROM [Partner_Group] "+\
         "WHERE [Reporter]=" + cy[0] + "AND [Year]=" + cy[1]
    partner_group = pd.read_sql(str_sql, cn_idb)

    str_sql= "SELECT [Reporter] AS reporter,[Year] AS year,[Code] AS type_code,[Name] AS type_desc FROM [Partner] "+\
         "WHERE [Reporter]=" + cy[0] + "AND [Year]=" + cy[1]
    partner = pd.read_sql(str_sql, cn_idb)
    
    types = pd.merge(partner_group, partner, on=['reporter','year','type_code'])
    types['type_code'] = types['reporter'] + '-' + types['type_code'].str[1:3]
    types['type_code'] = types['type_code'].str.strip()
    types.loc[-1] = [cy[0],cy[1], cy[0]+'-02','000','MFN applied duty rates'] 

    df_type = df_type.append(types, sort=True)

#%% Delete all records from a table
cur = cnx.cursor()
cur.execute("DELETE FROM rate;")
cur.execute("DELETE FROM type;")
cur.execute("DELETE FROM desc;")
cnx.commit()
#cnx.close()
#%%
df_type.to_sql(name='type', con=cnx, if_exists='append', index=False, chunksize = 190)
df_rate.to_sql(name='rate', con=cnx, if_exists='append', index=False, chunksize = 190)
df_desc.to_sql(name='desc', con=cnx, if_exists='append', index=False, chunksize = 190)

#%% Reference Data
# Partner Name
str_sql= "SELECT [Code] AS partner,[Name] AS name " \
          "FROM [reference_database].[dbo].[Country Code] " \
          "WHERE [Code Prefix] in ('C', 'U')"
partnername = pd.read_sql(str_sql, cn_ref)

partnername.to_sql(name='part', con=cnx, if_exists='append', index=False, chunksize = 190)

# HS 6D descriptions
str_sql= "SELECT [Product Code] AS hs,[Description], [Self Contained Description] " \
          "FROM [reference_database].[dbo].[Product Description] " \
          "WHERE [Classification Code]='HS6' AND [Lang]=1"
hs_desc = pd.read_sql(str_sql, cn_ref)
hs_desc['hs_desc'] = hs_desc['hs'] + ' - ' + hs_desc['Self Contained Description']
hs_desc['hs_len'] = hs_desc['hs'].str.len()
hs_db = hs_desc[hs_desc['hs_len']==6][['hs','hs_desc']]
hs_db.to_sql(name='hs', con=cnx, if_exists='append', index=False, chunksize = 190)

#%% New

IMPORTER = '156'
EXPORTER = '418' # Laos
HS = '100620'

data_rate = df_rate[(df_rate['reporter']==IMPORTER) & (df_rate['hs'].str[0:6]==HS)]
data_regi = df_type[(df_type['reporter']==IMPORTER) & (df_type['partner']==EXPORTER)]
result = pd.merge(data_rate, data_regi, on=['reporter','type_code'])


#%% Below are not used now
# Generate country code as list of tuple, copy to flask

country_name = pd.read_excel('Query1.xlsx')
country_name = country_name.sort_values('Name')
code_country_tuple = [tuple(x) for x in country_name.values]

# to json
country_json = country_name.rename(columns={'Code':'value','Name':'label'}).copy()
country_json['value'] = country_json['value'].astype(str)
country_json.to_json(orient='records')
country_json.to_json('country.json', orient='records')

# Generate country code as dictionary copy to flask
#code_country_dict = dict(zip(country_name.Code,country_name.Name))
#code_country_dict[156]

#%% HS

params_sql = urllib.parse.quote("DRIVER={SQL Server};SERVER=ADA-MSSQL-IDB;DATABASE=reference_database;UID=;PWD=")
cn_ref = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params_sql)

str_sql= "SELECT [Product Code] AS hs,[Description], [Self Contained Description] " \
          "FROM [reference_database].[dbo].[Product Description] " \
          "WHERE [Classification Code]='HS6' AND [Lang]=1"
hs_desc = pd.read_sql(str_sql, cn_ref)
hs_desc['hs_desc'] = hs_desc['hs'] + ' - ' + hs_desc['Self Contained Description']

hs_desc['hs_desc_ex'] = hs_desc['hs_desc']
hs_desc['hs_len'] = hs_desc['hs'].str.len()
hs_desc.to_excel('hs_desc.xlsx')

hs_desc_json = hs_desc[hs_desc['hs_len']==6][['hs','hs_desc']]
hs_desc_json = hs_desc_json.rename(columns={'hs':'value','hs_desc':'label'}).copy()
hs_desc_json.to_json('hs_desc.json', orient='records')
hs_tuple = [tuple(x) for x in hs_desc_json.values]
hs_dict = dict(zip(hs_desc_json.value,hs_desc_json.label))

import pickle
pickle.dump( hs_dict, open( "hs_dict.p", "wb" ) )
hs_dict1 = pickle.load( open( "hs_dict.p", "rb" ) )

pickle.dump( hs_tuple, open( "hs_tuple.p", "wb" ) )
hs_tuple1 = pickle.load( open( "hs_tuple.p", "rb" ) )


hs_db = hs_desc[hs_desc['hs_len']==6][['hs','hs_desc']]
hs_db.to_sql(name='hs', con=cnx, if_exists='append', index=False, chunksize = 190)
