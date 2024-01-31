'''
# Antotador personal. 
Intento de aplicación diseñada para android.

'''
# Kivy imports
from kivy.config import Config
## Configuración de dimensiones de ventana
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '700')
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty, NumericProperty 
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.textfield.textfield import MDTextField
# other modules
import os
from configparser import ConfigParser
from datetime import datetime, timezone
import requests
# import json

# KV code         ####     ####     ####
KV = '''
<ScManag>:
    peso: peso_tf.text
    dso_mx: so_mx_tf.text
    dso_mn: so_mn_tf.text
    dbo_mx: bo_mx_tf.text
    dbo_mn: bo_mn_tf.text
    Screen:
        name: "corp_mes"
        FloatLayout:
            size_hint: 1, .1
            pos_hint: {'top': 1}
            MDTopAppBar:
                title: "[size="+app.wresize["bar_fsize"]+"]  Medidas[/size]"
                anchor_title: "left"
                # right_action_items: [["content-save", lambda x: root.save_mes()]]
                pos_hint: {'top': 1}
            MDIconButton:
                icon: "content-save"
                pos_hint: {'right': .99, "center_y": .55}
                icon_size: app.wresize["bar_fsize"]
                on_press: root.save_mes()
        BoxLayout:
            id: fields_cont
            size_hint: 1, .9
            orientation: 'vertical'
            padding: 15
            MDTextField:
                id: peso_tf
                size_hint: 1, .08
                hint_text: "Peso (g)"
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: so_mx_tf
                size_hint: 1, .08
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                hint_text: "Diámetro SO max (cm)"
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: so_mn_tf
                size_hint: 1, .08
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                hint_text: "Diámetro SO max (cm)"
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: bo_mx_tf
                size_hint: 1, .08
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                hint_text: "Diámetro BO max (cm)"
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: bo_mn_tf
                size_hint: 1, .08
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                hint_text: "Diámetro BO max (cm)"
                markup: True
                line_color_normal: app.theme_cls.accent_color
'''

Builder.load_string(KV)



# Kivy classes          ####     ####     ####
class ScManag(MDScreenManager):
    peso = StringProperty()
    dso_mx = StringProperty()
    dso_mn = StringProperty()
    dbo_mx = StringProperty()
    dbo_mn = StringProperty()

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        
        # Read database connection info from "db.ini"
        DIR = os.getcwd()
        config = ConfigParser()
        config.read(os.path.join(DIR, "db.ini"))
        self.db_url = config["firebase"]["url"]
        self.data_name = config["firebase"]["data_name"]
        self.download_all()

    # Screen: 'corp_mes' methods        ####str(datetime.now(timezone.utc))
    def save_mes(self):
        '''Send to database using `request.post` method.
        A timestamp is included along with the data 
        (`datetime` module. UTC).
        '''
        print("prueba:\n",self.peso, self.dso_mx, self.dso_mn,
            self.dbo_mx, self.dbo_mn)
        timestamp = str(datetime.now(timezone.utc)).replace(" ", "_")
        data ={
            "timestamp":timestamp,
            "medidas":{
                "peso":self.peso,
                "dso_mx":self.dso_mx,
                "dso_mn":self.dso_mn,
                "dbo_mx":self.dbo_mx,
                "dbo_mn":self.dbo_mn
                }
            }

        try:
            res = requests.post(
                url=self.db_url+self.data_name+"/.json", 
                json=data
            )
            self.send_note()
        except:
            print("POST ERROR: data could not be sent")
            self.app.warning()
        finally:
            print(res)            
        
    def download_all(self):
        '''Verificar'''
        res2 = requests.get(url=self.db_url+"medidasxfecha/.json")
        res_json = res2.json()
        for k in res_json.keys():
            print(res_json[k], type(res_json[k]))
            print("")
            
    def send_note(self):
        '''
        Barra inferior emergente para recordar al usuario las coordenadas 
        y hora de descarga
        '''
        print(self.app.wresize["warg_font_s"])
        MDSnackbar(
            MDLabel(
                text=f'[size={self.app.wresize["warg_font_s"]}\
]  Datos enviados[/size]',
                markup=True,
                bold=True,
                halign= "center"
            ),
            duration=3,
            y=dp(24),
            pos_hint={"center_x": 0.5, "top":.8},
            size_hint_x=0.8,
            radius=[20,20,20,20]           
        ).open()
        
class MedidasApp(MDApp):
    
    COLS = DictProperty()
    wresize = DictProperty()
    w_emg = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # valores relativos
        self.wresize["bar_fsize"] = str(int(Window.size[1]/15))
        self.wresize["input_font_s"] = str(int(Window.size[1]/15))
        self.wresize["warg_font_s"] = str(int(Window.size[1]/30))
        Window.bind(on_resize=self.on_resize)

        # colores (rgb 0-1)
        self.COLS = {
            "purple": (.611764705882353, 
            .15294117647058825, .6901960784313725)
        }
            
    def on_resize(self, *args):
        '''Al cambiar dimensiones de ventana'''
        self.wresize["bar_fsize"] = str(int(Window.size[1]/15))
        print(self.wresize["bar_fsize"])
    
    def warning(self):
        '''POST error warning.'''
        if not self.w_emg:
            self.w_emg = MDDialog(
                text="NO SE PUDO ENVIAR\n (verificar conexión a internet)",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press= self.close_warng
                    ),
                ]
            )
            self.w_emg.open()
            
    def close_warng(self, *args):
        if self.w_emg:
            self.w_emg.dismiss(force=True)
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"

        return ScManag()


if __name__ == "__main__":
    MedidasApp().run()

