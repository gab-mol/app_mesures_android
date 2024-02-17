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
from kivy.properties import DictProperty, StringProperty 
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.config import ConfigParser
# other modules
from datetime import datetime, timezone
import pyrebase

# KV code         ####     ####     ####
KV = '''
#: import SlideTransition kivy.uix.screenmanager.SlideTransition
<ScManag>:

    user_mail: mail.text
    user_pwd: pwd.text
    
    mail_r: mail_r.text
    pwd_r1: pwd_r1.text
    pwd_r2: pwd_r2.text

    # peso: peso_tf.text
    # dso_mx: so_mx_tf.text
    # dso_mn: so_mn_tf.text
    # dbo_mx: bo_mx_tf.text
    # dbo_mn: bo_mn_tf.text
    
    Screen:
        name: "auth_sign"
        FloatLayout:
            # padding: 15
            MDLabel:
                pos_hint: {'center_x': 0.8,'center_y': .9}
                font_size: app.wresize["input_font_s"]
                text: "Ingresar."
                bold: True
                color: app.COLS["purple"]
            MDTextField:
                id: mail
                pos_hint: {'center_x': 0.5,'center_y': .75}
                size_hint_x: 0.85
                hint_text: "Correo"
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: pwd
                pos_hint: {'center_x': 0.5,'center_y': .55}
                size_hint_x: 0.85
                hint_text: "Contraseña (medidas-app)"
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                password: True
                line_color_normal: app.theme_cls.accent_color
            MDRaisedButton:
                pos_hint: {'center_x': .49,'center_y': .4}
                font_size: app.wresize["titl_font_s"]
                text: "Entrar"
                on_release: app.root.sign_in()
            MDFlatButton:
                pos_hint: {'center_x': .27,'center_y': .3}
                font_size: app.wresize["titl_font_s"]
                text: "[color=#dede35]Registrarse.[/color]"
                on_press:
                    app.root.transition = SlideTransition(direction="left")
                    app.root.current = "auth_regis"             
    Screen:
        name: "auth_regis"
        FloatLayout:
            MDLabel:
                pos_hint: {'center_x': 0.595,'center_y': .9}
                font_size: app.wresize["titl_font_s"]
                text: "Registrarse. \\nCorreo a elección y contraseña"
                bold: True
                color: app.COLS["purple"]
            MDTextField:
                id: mail_r
                pos_hint: {'center_x': 0.5,'center_y': .75}
                size_hint_x: 0.85
                hint_text: "Correo"
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: pwd_r1
                pos_hint: {'center_x': 0.5,'center_y': .55}
                size_hint_x: 0.85
                hint_text: "Contraseña"
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                line_color_normal: app.theme_cls.accent_color
            MDTextField:
                id: pwd_r2
                pos_hint: {'center_x': 0.5,'center_y': .35}
                size_hint_x: 0.85
                hint_text: "Confirmar contraseña"
                mode: "rectangle"
                font_size: app.wresize["bar_fsize"]
                line_color_normal: app.theme_cls.accent_color
            MDRaisedButton:
                pos_hint: {'center_x': .32,'center_y': .22}
                font_size: app.wresize["titl_font_s"]
                text: "Confirmar"
                on_release: app.root.registr()
            MDFlatButton:
                pos_hint: {'center_x': .37,'center_y': .12}
                font_size: app.wresize["titl_font_s"]
                text: "[color=#dede35]Volver a Ingresar.[/color]"
                on_press: 
                    app.root.transition = SlideTransition(direction="right")
                    app.root.current = "auth_sign"         
    Screen:
        name: "corp_mes"
        FloatLayout:
            size_hint: 1, .13
            pos_hint: {'top': 1}
            MDTopAppBar:
                title: "[size="+app.wresize["bar_fsize"]+"]  Medidas[/size]"
                anchor_title: "left"
                # right_action_items: [["content-save", lambda x: root.save_mes()]]
                pos_hint: {'top': 1}
            MDIconButton:
                icon: "content-save"
                pos_hint: {'right': .99, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press: root.save_mes()
            MDIconButton:
                icon: "test-tube"
                pos_hint: {'right': .85, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press: root.test_db()
        BoxLayout:
            size_hint: 1, .9
            orientation: 'vertical'
            padding: 15
            ScrollView:
                
                MDList:
                    id: input_fields
                    spacing: 10
                # MDTextField:
                #     id: peso_tf
                #     size_hint: 1, .08
                #     hint_text: "Peso (g)"
                #     mode: "rectangle"
                #     font_size: app.wresize["bar_fsize"]
                #     line_color_normal: app.theme_cls.accent_color
                # MDTextField:
                #     id: so_mx_tf
                #     size_hint: 1, .08
                #     mode: "rectangle"
                #     font_size: app.wresize["bar_fsize"]
                #     hint_text: "Diámetro SO max (cm)"
                #     line_color_normal: app.theme_cls.accent_color
                # MDTextField:
                #     id: so_mn_tf
                #     size_hint: 1, .08
                #     mode: "rectangle"
                #     font_size: app.wresize["bar_fsize"]
                #     hint_text: "Diámetro SO max (cm)"
                #     line_color_normal: app.theme_cls.accent_color
                # MDTextField:
                #     id: bo_mx_tf
                #     size_hint: 1, .08
                #     mode: "rectangle"
                #     font_size: app.wresize["bar_fsize"]
                #     hint_text: "Diámetro BO max (cm)"
                #     line_color_normal: app.theme_cls.accent_color
                # MDTextField:
                #     id: bo_mn_tf
                #     size_hint: 1, .08
                #     mode: "rectangle"
                #     font_size: app.wresize["bar_fsize"]
                #     hint_text: "Diámetro BO max (cm)"
                #     markup: True
                #     line_color_normal: app.theme_cls.accent_color
'''

Builder.load_string(KV)

class FireBase:
    
    def __init__(self, config:ConfigParser):
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
            self.conn = pyrebase.initialize_app(conf)
            print("`initialize_app`: > WORK")
        except:
            print("`initialize_app`: X FAIL")
        
    def db(self):
        '''Returns Firebase `Database` object'''
        try:
            db = self.conn.database()
            print("`database`: > WORK")
            return db
        except:
            print("`database`: X FAIL")
            return None
    def auth(self):
        '''Returns Firebase `auth` object 
        (user authentication methods)'''
        try:
            auth = self.conn.auth()
            print("`auth`: > WORK")
            return auth
        except:
            print("`auth`: X FAIL")
            return None

# Kivy classes          ####     ####     ####
class Input(MDTextField):
    id = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScManag(MDScreenManager):
    
    # autentication propertys
    user_mail = StringProperty()
    user_pwd = StringProperty()
    
    mail_r = StringProperty()
    pwd_r1 = StringProperty()
    pwd_r2 = StringProperty()
    
    # 'Mesures screen' propertys
    # peso = StringProperty()
    # dso_mx = StringProperty()
    # dso_mn = StringProperty()
    # dbo_mx = StringProperty()
    # dbo_mn = StringProperty()
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        # config file
        self.config = ConfigParser()
        self.config.read("db.ini")
        
        # Firebase init
        self.fbase = FireBase(self.config)
        self.auth = self.fbase.auth()
        self.db = self.fbase.db()
        ## DB directory
        self.db_node_target = self.config["pyrebase"]["db_node"]
        ## verify store user
        self.user = None
        self.mail = self.config["user"]["mail"]
        self.pwd = self.config["user"]["pwd"]
        
        if self.mail == "" or self.pwd == "":
            self.current = "auth_sign"
        else:
            self.user_mail = self.mail
            self.user_pwd = self.pwd
            print(f"\nUSUARIO: {self.mail}\n")
            self.sign_in()
            self.current = "corp_mes"
            
            # Read database connection info from "db.ini"
            self.db_url = self.config["firebase"]["url"]
            self.data_name = self.config["firebase"]["data_name"]
            # print(f"deprecated:{self.db_url}\n{self.data_name}")
        
        # input list declaration
        for  ids, text in zip(
            ["peso_tf","so_mx_tf","so_mn_tf","bo_mx_tf","bo_mn_tf"],
            ["Peso (g)",
             "Diámetro SO max (cm)",
             "Diámetro SO max (cm)",
             "Diámetro BO max (cm)",
             "Diámetro BO max (cm)"]
            ):
            self.ids.input_fields.add_widget(
                MDTextField(
                    id=ids,
                    size_hint=(.7, .08),
                    mode="rectangle",
                    font_size=self.app.wresize["bar_fsize"],
                    hint_text=text,
                    line_color_normal=self.app.theme_cls.accent_color
                )
            )
        # Trick to allow user to adjust visibility of input boxes in phones
        # (because of android onscreen keyboard)
        for i in range(50):
            self.ids.input_fields.add_widget(
                MDLabel(size_hint=(.7, .08))
            )
    # authentication methods (Screens: 'auth_sign' & 'auth_regist')
    def sign_in(self):
        print("sign_in:", self.user_mail, self.user_pwd)
        try:
            self.user = self.auth.sign_in_with_email_and_password(self.user_mail, self.user_pwd)
            print(self.user)
            self.current = "corp_mes"
        except:
            print("NO fue posible loggearse en Firebase con:")
            print("Res:",self.user)
            print(self.user_mail, self.user_pwd)
            self.show_note("Error al iniciar sesión")
        if self.user:
            self.config["user"]["mail"] = self.user_mail
            self.config["user"]["pwd"] = self.user_pwd
            self.config.write()
        
    def registr(self):
        print("registr:", self.mail_r, self.pwd_r1, self.pwd_r2)

        if self.pwd_r1 == self.pwd_r2:
            try:
                r = self.auth.create_user_with_email_and_password(self.mail_r, self.pwd_r1)
                print(r)
                print("NUEVAS CRED:", self.mail_r, self.pwd_r1)
                self.config["user"]["mail"] = self.mail_r
                self.config["user"]["pwd"] = self.pwd_r1
                
                self.config.write()                
            except:
                print("NO pudo crearse usario Firebase")
        else:
            print("CONFIRMACIÓN DE CONTRASEÑA NO COINCIDEN")
    
    # Screen: 'corp_mes' methods        ####str(datetime.now(timezone.utc))
    def save_mes(self):
        '''Send to database using `request.post` method.
        A timestamp is included along with the data 
        (`datetime` module. UTC).
        '''
        # Retive text from ScrollView's MDTextField childrens
        data_list = []
        for child in reversed(self.ids.input_fields.children):
            if isinstance(child, MDTextField):
                data_list.append(child.text)
        print("DATA LIST:",data_list)
        timestamp = str(datetime.now(timezone.utc)).replace(" ", "_")
        data ={
            "timestamp":timestamp,
            "medidas":{
                "peso":data_list[0],
                "dso_mx":data_list[1],
                "dso_mn":data_list[2],
                "dbo_mx":data_list[3],
                "dbo_mn":data_list[4]
                }
            }
        
        def alta(*args):
            '''Send data to Firebase DB.'''
            print("mandar:", self.db_node_target)
            try:
                results = self.db.child(
                    self.db_node_target
                    ).child(datetime.now().strftime(
                        "%d-%m-%y(%H:%M:%S)")
                        ).set(data, self.user['idToken'])
                self.show_note("Datos enviados.")
                print("RESPUESTA:")
                print(results)       
            except:
                self.show_note("No se pudo enviar.")
            self.app.close_warng()

        # NOTA: importante pasar `self.user['idToken']` es el token de usuario que verifica que está registrado
        self.app.warning(
            text="¿Enviar medidas?",
            ok_txt="Enviar",
            dism_txt="Cancelar",
            met1=alta
        )
        
    def show_note(self,note:str, durat=3):
        '''
        Float snackbar based popup.
        '''
        print(self.app.wresize["warg_font_s"])
        MDSnackbar(
            MDLabel(
                text=f'[size={self.app.wresize["warg_font_s"]}\
]  {note}[/size]',
                markup=True,
                bold=True,
                halign= "center"
            ),
            duration=durat,
            y=dp(24),
            pos_hint={"center_x": 0.5, "top":.8},
            size_hint_x=0.8,
            radius=[20,20,20,20]           
        ).open()
        
        
    def test_db(self):
        '''Switch between defoult and test nodes of Firebase DB.
        (for development purposes only)'''
        cfg = self.config["pyrebase"]
        print(self.db_node_target, "to:")
        if self.db_node_target == cfg["db_node"]:
            self.db_node_target = cfg["db_node_pr"]
        else:
            self.db_node_target = cfg["db_node"]
        print(self.db_node_target)
        self.show_note(f"A: {self.db_node_target}", durat=.2)
        
        
class MedidasApp(MDApp):
    
    COLS = DictProperty()
    wresize = DictProperty()
    w_emg = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # valores relativos
        self.on_resize()
        Window.bind(on_resize=self.on_resize)

        # colores (rgb 0-1)
        self.COLS = {
            "purple": (.611764705882353, 
            .15294117647058825, .6901960784313725),
            "elect_yell": (1, 0.98823529411, 0)
        }
            
    def on_resize(self, *args):
        '''Al cambiar dimensiones de ventana'''
        self.wresize["bar_fsize"] = str(int(Window.size[1]/15))
        self.wresize["input_font_s"] = str(int(Window.size[1]/15))
        self.wresize["warg_font_s"] = str(int(Window.size[1]/30))
        self.wresize["titl_font_s"] = str(int(Window.size[1]/25))
        # print(self.wresize["bar_fsize"])
    
    def warning(self, text:str, ok_txt:str, 
            dism_txt:str, met1, met2=None):
        '''Popup dialog with user.'''
        if met2:
            met2= self.close_warng

        if not self.w_emg:
            self.w_emg = MDDialog(
                text=text,
                buttons=[
                    MDFlatButton(
                        text=ok_txt,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press= met1
                    ),
                    MDFlatButton(
                        text=dism_txt,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press= self.close_warng
                    )             
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