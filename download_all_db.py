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

# pruebas_desarrollo OR medidas_reales_pr
DB_DIR = "pruebas_desarrollo"

# cvs file storage
NAME_CVS = "pr_download.cvs"


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
        peso.append(pd.to_numeric(medid["peso"].replace(",",".")))
        dso_mx.append(pd.to_numeric(medid["dso_mx"].replace(",",".")))
        dso_mn.append(pd.to_numeric(medid["dso_mn"].replace(",",".")))
        dbo_mx.append(pd.to_numeric(medid["dbo_mx"].replace(",",".")))
        dbo_mn.append(pd.to_numeric(medid["dbo_mn"].replace(",",".")))
        
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
    response = None
    try:
        response = db.child(DB_DIR).get(token=user["idToken"])
    except:
        print("FALLÓ DESCARGA DE DATOS")
    
    timestamp = []
    peso = []
    dso_mx = []
    dso_mn = []
    dbo_mx = []
    dbo_mn = []
    
    for d in response.each():

        regis = dict(d.val())

        # timestamp
        time_str = regis["timestamp"]
        time = pd.to_datetime(time_str.replace("_", " "))
        time = time - pd.Timedelta(hours=3)
        timestamp.append(time)

        # actual mesures
        medid = regis["medidas"]
        peso.append(pd.to_numeric(medid["peso"].replace(",",".")))
        dso_mx.append(pd.to_numeric(medid["dso_mx"].replace(",",".")))
        dso_mn.append(pd.to_numeric(medid["dso_mn"].replace(",",".")))
        dbo_mx.append(pd.to_numeric(medid["dbo_mx"].replace(",",".")))
        dbo_mn.append(pd.to_numeric(medid["dbo_mn"].replace(",",".")))
            
    tb = pd.DataFrame({
        "fechaUTC":timestamp,
        "peso":peso,
        "dso_mx":dso_mx,
        "dso_mn":dso_mn,
        "dbo_mx":dbo_mx,
        "dbo_mn":dbo_mn
    })
    print(tb)
    return tb

tb = download_all()
tb.to_csv(NAME_CVS, ";", index=False)