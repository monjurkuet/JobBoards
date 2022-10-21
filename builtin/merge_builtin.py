import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
                              #host='localhost', 
                              host='161.97.97.183',
                              database='companydatabase',
                              user='root', 
                              password='$C0NTaB0vps8765%%$#', 
                              port=3306
                              ,auth_plugin='caching_sha2_password')
cursor = connection.cursor() 

sql_query = pd.read_sql_query ('''SELECT * FROM builtin''', connection)

df_builtincompanies = pd.DataFrame(sql_query)
df_builtinjobs=pd.read_excel('jobdata.xlsx')

df_builtinjobs=df_builtinjobs.rename(columns={"company_id": "id"})

df_builtinjobs['id']=df_builtinjobs['id'].astype(str)
df_builtincompanies['id']=df_builtincompanies['id'].astype(str)

df_builtin_final=pd.merge(df_builtinjobs, df_builtincompanies, on='id',how='left')

df_builtin_final.to_excel('builtin_final.xlsx',index=None)