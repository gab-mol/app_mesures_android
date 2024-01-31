import requests
import os
import configparser
import pandas as pd

DIR = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(DIR, "db.ini"))
db_url = config["firebase"]["url"]
data_name = config["firebase"]["data_name"]

def download_all() -> pd.DataFrame:
    '''
    Descarga todo lo almacenado en la base de datos (Firebase) 
    mediante `request.get`, y lo retorna en formateado 
    como `pandas.DataFrame`.
    '''
    
    try:
        res2 = requests.get(url=db_url+data_name+"/.json")
    except:
        Exception("Falló la consulta")
    finally:
        print(res2)
        
    res_json = res2.json()
    
    timestamp = []
    peso = []
    dso_mx = []
    dso_mn = []
    dbo_mx = []
    dbo_mn = []
    
    for k in res_json.keys():
        time_str = res_json[k]["timestamp"]
        time = pd.to_datetime(time_str.replace("_", " "))
        
        timestamp.append(time)
        medid = res_json[k]["medidas"]
        peso.append(pd.to_numeric(medid["peso"]))
        dso_mx.append(pd.to_numeric(medid["dso_mx"]))
        dso_mn.append(pd.to_numeric(medid["dso_mn"]))
        dbo_mx.append(pd.to_numeric(medid["dbo_mx"]))
        dbo_mn.append(pd.to_numeric(medid["dbo_mn"]))
        
    tb = pd.DataFrame({
        "fechaUTC":timestamp,
        "peso":peso,
        "dso_mx":dso_mx,
        "dso_mn":dso_mn,
        "dbo_mx":dbo_mx,
        "dbo_mn":dbo_mn
    })
    
    return tb

tb = download_all()

print(tb)