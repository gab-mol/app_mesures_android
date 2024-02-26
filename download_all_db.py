import requests
import os
from configparser import ConfigParser
import pandas as pd
import pyrebase
import sqlite3



DIR = os.getcwd()
# pruebas_desarrollo OR medidas_reales_pr
# DB_DIR = "medidas_reales_pr"
# cvs file storage (tests)
NAME_CVS = "pr_download2.cvs"


class FireDbConn:
    def __init__(self, config:ConfigParser) -> None:
        self.config = config
        self.db_url = self.config["firebase"]["url"]
        self.data_name = self.config["firebase"]["data_name"]
        db_confg = self.config["pyrebase"]
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
            self.conn = pyrebase.initialize_app(conf)
            print("`initialize_app`: > WORK")
        except:
            print("`initialize_app`: X FAIL")
    
    def db_utils(self):
        db = self.conn.database()
        auth = self.conn.auth()
        user = auth.sign_in_with_email_and_password(self.config["user"]["mail"], self.config["user"]["pwd"])

        return db, auth, user


class Extrac:

    def __init__(self, db, user):
        self.db = db
        self.user = user

    # deprecated
    def download_all_request(db_url,data_name) -> pd.DataFrame:
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

    def download_mesur(self, DB_DIR, time_str=False):
        '''Download all content from `DB_DIR` directory of the DB.'''
        response = None
        try:
            response = self.db.child(DB_DIR).get(token=self.user["idToken"])
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
            print("\n\n\n",regis,"\n\n\n")
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
            "fecha":timestamp,
            "peso":peso,
            "dso_mx":dso_mx,
            "dso_mn":dso_mn,
            "dbo_mx":dbo_mx,
            "dbo_mn":dbo_mn
        })
        print(tb)

        if time_str:
            tb["fecha"] = tb["fecha"].dt.strftime('%Y-%m-%d-%H:%M:%S')

        return tb


    def download_punct(self, DB_DIR, time_str=False):
        '''Download all content from `DB_DIR` directory of the DB.'''
        response = None
        try:
            response = self.db.child(DB_DIR).get(token=self.user["idToken"])
        except:
            print("FALLÓ DESCARGA DE DATOS pinchadura")
        
        timestamp = []
        fecha = []
        bicicl = []
        rueda = []
        camar = []
        npinc = []
        camar_r = []

        for d in response.each():

            regis = dict(d.val())

            # timestamp
            time_str = regis["timestamp"]
            time = pd.to_datetime(time_str.replace("_", " "))
            time = time - pd.Timedelta(hours=3)
            timestamp.append(time)
            
            # actual mesures
            medid = regis["notas_bicicleta"]
            fecha.append(str(medid["Fecha"].replace(",",".")))
            bicicl.append(str(medid["Bicicleta"].replace(",",".")))
            rueda.append(str(medid["Rueda"].replace(",",".")))
            camar.append(str(medid["Cámara"].replace(",",".")))
            npinc.append(pd.to_numeric(medid["n° Pinchaduras"].replace(",",".")))
            camar_r.append(str(medid["Cámara reemplazo"].replace(",",".")))

        tb = pd.DataFrame({
            "registro":timestamp,
            "fecha":fecha,
            "bicicleta":bicicl,
            "rueda":rueda,
            "camara":camar,
            "n_pinchadura":npinc,
            "camara_reemplazo":camar_r
        })
        print(tb)

        if time_str:
            tb["registro"] = tb["registro"].dt.strftime('%Y-%m-%d-%H:%M:%S')

        return tb

    def cvs(tb:pd.DataFrame, name):
        print(f"Guardado {name} en:\n{DIR}")
        tb.to_csv(os.path.join(DIR,name), ";", index=False)


class LocStor:
    '''Local storage of App records.'''
    def __init__(self, confg:ConfigParser) -> None:
        confg = confg["sql"]
        db_path = confg["db_path_pr"]
        self.name_tb_m = confg["name_tb1"]
        self.name_tb_p = confg["name_tb2"]

        self.conn = sqlite3.connect(db_path)
        
        # SQL table creation querrys
        cursor = self.conn.cursor()
        ## Mesures        
        main_tb = f'''CREATE TABLE IF NOT EXISTS {self.name_tb_m}(\
            timestamp TEXT PRIMARY KEY, \
            peso real, \
            dso_mx real, \
            dso_mn real, \
            dbo_mx real, \
            dbo_mn real)'''

        cursor.execute(main_tb)
        stage_tb = f'''CREATE TABLE IF NOT EXISTS stage(\
            timestamp TEXT PRIMARY KEY, \
            peso real, \
            dso_mx real, \
            dso_mn real, \
            dbo_mx real, \
            dbo_mn real)'''
        cursor.execute(stage_tb)

        ## Punctures
        punc_tb = f'''CREATE TABLE IF NOT EXISTS {self.name_tb_p}(\
            timestamp TEXT PRIMARY KEY, \
            fecha TEXT, \
            bicicleta TEXT, \
            rueda TEXT, \
            camara TEXT, \
            n_pinchaduras real,
            camara_reempl TEXT)'''
        cursor.execute(punc_tb)

        punc_tb_s = f'''CREATE TABLE IF NOT EXISTS stage2(\
            timestamp TEXT PRIMARY KEY, \
            fecha TEXT, \
            bicicleta TEXT, \
            rueda TEXT, \
            camara TEXT, \
            n_pinchaduras real,
            camara_reempl TEXT)'''
        cursor.execute(punc_tb_s)

        self.conn.commit()

    def alta(self,data:list, tb_name:str, cols:list[str]):
        '''Performs `INSERT INTO` querry for table `tb_name`
        with columns `cols`.

        ### Parameters
            - `data`: `list` of data to insert.
            - `tb_name`: name of the table in DB to insert.
            - `cols`: `list` of `str` with de columns of table.
        '''
        querry = f'''
        INSERT INTO {tb_name}({", ".join(cols)}) 
        VALUES({", ".join(["?" for i in range(len(cols))])})
        '''

        try:
            cursor = self.conn.cursor()
            cursor.execute(querry, data)
            self.conn.commit()
            print(f"\nRegistro guardado en tabla: {tb_name}\n")
        except:
            print("ERROR EN ALTA A: sqlite local")

    def scd1_m(self,df:pd.DataFrame):
        '''Alta Querry with SCD type 1 strategy.'''
        columns = ["timestamp", "peso", "dso_mx", "dso_mn", "dbo_mx",
            "dbo_mn"]
        # staging
        for i in range(len(df)):
            record = df.iloc[i].to_list()
            data = [str(record[0]), float(record[1]), float(record[2]), 
            float(record[3]), float(record[4]), float(record[5])]

            sql_local.alta(data, "stage", columns)

        # Load to main table
        q = f'''
            INSERT OR IGNORE INTO {self.name_tb_m}(timestamp, peso, dso_mx, dso_mn, dbo_mx, dbo_mn)
            SELECT stage.timestamp, stage.peso, stage.dso_mx, stage.dso_mn, stage.dbo_mx, 
            stage.dbo_mn 
            FROM stage 
            LEFT OUTER JOIN {self.name_tb_m} 
            ON {self.name_tb_m}.timestamp = stage.timestamp;
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(q)
            self.conn.commit()
            print(f"\nLEFT OUTER JOIN: stage-{self.name_tb_m}")
        except:
            print("ERROR en querry, o no hay registros nuevos que agregar\n\
(condición del join no se cumple)")
        finally:
            print("Cleaning stage tb...")
            self.stage_clean()
    
    def scd1_p(self,df:pd.DataFrame):
        '''Alta Querry with SCD type 1 strategy.'''
        columns = ["timestamp", "fecha", "bicicleta", "rueda", "camara",
            "n_pinchaduras", "camara_reempl"]
        # staging
        for i in range(len(df)):
            record = df.iloc[i].to_list()
            data = [str(record[0]), str(record[1]), str(record[2]), 
            str(record[3]), str(record[4]), int(record[5]), str(record[6])]

            sql_local.alta(data, "stage2", columns)

        # Load to main table
        q = f'''
            INSERT OR IGNORE INTO {self.name_tb_p}(timestamp, fecha, bicicleta, rueda, camara,
            n_pinchaduras, camara_reempl)
            SELECT stage2.timestamp, stage2.fecha, stage2.bicicleta, stage2.rueda, stage2.camara,
            stage2.n_pinchaduras, stage2.camara_reempl
            FROM stage2 
            LEFT OUTER JOIN {self.name_tb_p} 
            ON {self.name_tb_p}.timestamp = stage2.timestamp;
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(q)
            self.conn.commit()
            print(f"\nLEFT OUTER JOIN: stage2-{self.name_tb_m}")
        except:
            print("ERROR en querry, o no hay registros nuevos que agregar\n\
(condición del join no se cumple)")
        finally:
            print("Cleaning stage tb...")
            self.stage_clean("2")
        
    def stage_clean(self,target="1"):
        if target == "1":
            tb_n = "stage"
        else:
            tb_n = "stage2"

        '''REMOVE ALL RECORDS FROM stage TABLE.'''
        truncate = f'''
        DELETE FROM {tb_n};
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(truncate)
            self.conn.commit()
            print("\ntb stage limpia.")
        except:
            print("ERROR en querry.")


if __name__ == "__main__":
    confg = ConfigParser()
    confg.read(os.path.join(DIR, "db.ini"))

    ini_ext = FireDbConn(confg)
    db, auth, user = ini_ext.db_utils()

    extrac = Extrac(db,user)
    tb_m = extrac.download_mesur(confg["pyrebase"]["db_node1"],
        time_str=True)
    tb_p = extrac.download_punct(confg["pyrebase"]["db_node2"],
        time_str=True)
    
    sql_local = LocStor(confg)
    sql_local.scd1_m(tb_m)
    sql_local.scd1_p(tb_p)

    
