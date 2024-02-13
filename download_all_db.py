import requests
import os
import configparser
import pandas as pd
import pyrebase


DIR = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(DIR, "db.ini"))
db_url = config["firebase"]["url"]
data_name = config["firebase"]["data_name"]
db_confg = config["pyrebase"]
conf = {
        "apiKey": db_confg["apiKey"],
        "authDomain": db_confg["authDomain"],
        "databaseURL": db_confg["databaseURL"],
        "projectId": db_confg["projectId"],
        "storageBucket": db_confg["storageBucket"],
        "messagingSenderId": db_confg["messagingSenderId"],
        "appId": db_confg["appId"],
        "measurementId": db_confg["measurementId"],
        }
try:
    conn = pyrebase.initialize_app(conf)
    print("`initialize_app`: > WORK")
except:
    print("`initialize_app`: X FAIL")
    
db = conn.database()
auth = conn.auth()
user = auth.sign_in_with_email_and_password(config["user"]["mail"], config["user"]["pwd"])
for k in user.keys():
    print("\n", k,"\n")
    print(user[k],"\n")

def download_all_request() -> pd.DataFrame:
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

def download_all():
    try:
        data = db.child("pruebas_desarrollo").get(token=user["idToken"])
        print(data.val())
    except:
        print("FALLÓ DESCARGA DE DATOS")

res = db.child("pruebas_desarrollo").get(token=config["user"]["idtoken"])
print(res)