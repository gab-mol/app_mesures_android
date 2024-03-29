'''
# Anotador personal.
Intento de aplicación diseñada para android.

'''
# Kivy imports
from kivy.config import Config
## Configuración de dimensiones de ventana
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '700')
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty #, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.config import ConfigParser
import asynckivy as ak

# other modules
from datetime import datetime, timezone
import pyrebase
import re

# KV code         ####     ####     ####
KV = '''
#: import SlideTransition kivy.uix.screenmanager.SlideTransition
<ScManag>:

    user_mail: mail.text
    user_pwd: pwd.text
    
    mail_r: mail_r.text
    pwd_r1: pwd_r1.text
    pwd_r2: pwd_r2.text
    
    Screen:
        name: "auth_sign"
        FloatLayout:
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
                on_release: 
                    app.root.sign_in()
                    app.root.input_lists_init()
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
                title: "[size="+app.wresize["bar_fsize"]+"]Medidas[/size]"
                anchor_title: "left"
                # right_action_items: [["content-save", lambda x: root.save_mes_med()]]
                pos_hint: {'top': 1}
            MDRectangleFlatIconButton:
                icon: root.led_ico
                text: " "+root.count
                theme_text_color: "Custom"
                text_color: "white"
                line_color: 1,1,1,0
                pos_hint: {'right': .99, "center_y": .65}
            MDIconButton:
                icon: "content-save"
                pos_hint: {'right': .89, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press: root.save_mes("corp_mes")
            MDIconButton:
                icon: "test-tube"
                pos_hint: {'right': .79, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press: root.test_db()
            MDIconButton:
                icon: "bicycle"
                pos_hint: {'right': .69, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press:
                    app.root.transition = SlideTransition(direction="right")
                    app.root.current = "bike_notes"

        BoxLayout:
            size_hint: 1, .9
            orientation: 'vertical'
            padding: 15
            ScrollView:
                MDList:
                    id: input_fields
                    spacing: 10
    Screen:
        name: "bike_notes"
        FloatLayout:
            size_hint: 1, .13
            pos_hint: {'top': 1}
            MDTopAppBar:
                title: "[size="+app.wresize["bar_fsize2"]+"]Pinchadura Bicicl.[/size]"
                anchor_title: "left"
                # right_action_items: [["content-save", lambda x: root.save_mes_bike()]]
                pos_hint: {'top': 1}
            MDIconButton:
                icon: "content-save"
                pos_hint: {'right': .99, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press: root.save_mes("bike_notes")
            MDIconButton:
                icon: "scale-balance"
                pos_hint: {'right': .83, "center_y": .65}
                icon_size: app.wresize["bar_fsize"]
                on_press:
                    app.root.transition = SlideTransition(direction="left")
                    app.root.current = "corp_mes"      
        BoxLayout:
            size_hint: 1, .9
            orientation: 'vertical'
            padding: 15
            ScrollView:
                MDList:
                    id: input_bike
                    spacing: 10
'''
Builder.load_string(KV)

# Focused `Input` instance
focus_txin = None


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

    def check_today_data(self,db, db_node, idToken) -> tuple:
        '''
        Checks if there is data from the current day in the database.
        
        return
            tuple: (bool, str). If it is data from today, and how many records (formated).
        '''
        childrens = db.child(db_node).get(token=idToken).val().keys()
        today = datetime.now().strftime("%d-%m-%y")
        dates = [chil[0:8] for chil in childrens]
        today_dat = str(sum(today == d for d in dates))
        if today in dates:
            print("Datos ya enviados hoy")
            check = True
        else:
            print("No hay datos de hoy")
            check = False
        
        return (check, f"{today_dat}")


# Kivy classes          ####     ####     ####
class Input(MDTextField):
    id = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_parent(self, widget, parent):
        '''
        Set focus in next `Input`.

        ### Args:
            - widget: this widget
            - parent: parent widget (here `MDList`)
        '''
        if self.next:
            self.next.focus = True

    def on_focus(self, instance, value, *largs):
        '''
        Set `Input.next` relative to current focused instance.
        '''
        global focus_txin
        focus_txin = self
        self.next = self.get_focus_next()

        print("on_focus:", self.id)
        print("on_focus next:", self.next.id)


class ScManag(MDScreenManager):
    
    # autentication propertys
    user_mail = StringProperty()
    user_pwd = StringProperty()
    
    mail_r = StringProperty()
    pwd_r1 = StringProperty()
    pwd_r2 = StringProperty()

    # "sent notice" 
    led_ico = StringProperty()
    count = StringProperty()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        # config file
        self.config = ConfigParser()
        self.config.read("db.ini")
        
        # Firebase init
        self.fbase = FireBase(self.config)
        self.db = self.fbase.db()
        self.auth = self.fbase.auth()
        
        ## DB directory
        self.db_node_target1 = self.config["pyrebase"]["db_node1"]
        self.db_node_target2 = self.config["pyrebase"]["db_node2"]
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
            self.input_lists_init()
            self.current = "corp_mes"
            
            # Read database connection info from "db.ini"
            self.db_url = self.config["firebase"]["url"]
            self.data_name = self.config["firebase"]["data_name"]
        
    def input_lists_init(self):
        '''Initialize screens: "corp_mes" and "bike_notes".'''

        # input list declaration
        t_ids = ["pes", "somin", "somax", "bomin", "bomax"]
        for text, id in zip(["Peso (g)",
             "Diámetro SO max (cm)",
             "Diámetro SO min (cm)",
             "Diámetro BO max (cm)",
             "Diámetro BO min (cm)"],t_ids):
            self.ids.input_fields.add_widget(
                Input(
                    id=id,
                    size_hint=(.7, .08),
                    mode="rectangle",
                    multiline=False,
                    write_tab=False,
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
        
        # input list declaration (Screen: 'bike_notes')
        t_ids2 = ["fec","bici", "rued", "cam", "n", "camr"]
        for text, id in zip(["Fecha (dd/mm/aa)",
             "Bicicleta",
             "Rueda",
             "Cámara",
             "n° Pinchaduras",
             "Cámara reemplazo"], t_ids2):
            self.ids.input_bike.add_widget(
                Input(
                    id=id,
                    size_hint=(.7, .08),
                    mode="rectangle",
                    font_size=self.app.wresize["bar_fsize"],
                    hint_text=text,
                    line_color_normal=self.app.theme_cls.accent_color
                )
            )
        for i in range(50):
            self.ids.input_bike.add_widget(
                MDLabel(size_hint=(.7, .08))
            )

        # "sent led" on?
        already_sent = self.fbase.check_today_data(
            self.db, 
            self.db_node_target1, 
            self.user["idToken"]
            )
        
        self.switch_redled(already_sent[0])
        self.count = already_sent[1]
        
        # init keyboard listener for 'Enter' key selection
        self.lis = KeyBoardLis(self)

    def switch_redled(self, on:bool):
        '''ON/OFF red led for sent data notice.'''
        if on:
            self.led_ico = "resources/led_rojo_on.ico"
        else:
            self.led_ico = "resources/led_rojo_off.ico"

    # authentication methods (Screens: 'auth_sign' & 'auth_regist') #########
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
                print("auth:",self.auth)
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
    
    # input Screens methods #################################################
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
        print(self.db_node_target1, "to:")
        if self.db_node_target1 == cfg["db_node1"]:
            self.db_node_target1 = cfg["db_node_pr"]
        else:
            self.db_node_target1 = cfg["db_node1"]
        print(self.db_node_target1)
        self.show_note(f"A: {self.db_node_target1}", durat=.2)

    def save_mes(self, mode:str):
        '''Send to database using `request.post` method.
        A timestamp is included along with the data 
        (`datetime` module. UTC).
        '''
        if mode == "corp_mes":
            conteiner = self.ids.input_fields.children
            db_node = self.db_node_target1
        elif mode == "bike_notes":
            conteiner = self.ids.input_bike.children
            db_node = self.db_node_target2
        # Retrive text from ScrollView's MDTextField childrens
        data_list = []
        for child in reversed(conteiner):
            if isinstance(child, MDTextField):
                data_list.append(child.text)
        print("DATA LIST:", data_list)
        timestamp = str(datetime.now(timezone.utc)).replace(" ", "_")
        
        # Field verification (for `corp_mes` only)
        def numeric_field(input) -> bool:
            '''Search for alphabetic characters.'''
            detect = re.search(r"[A-Za-z]", input)
            return True if detect else False

        if mode == "corp_mes":
            verify = list()
            for d in data_list:
                verify.append(numeric_field(d))
            
            format_error = True if True in verify else False

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
            
        elif mode == "bike_notes":
            data ={
                "timestamp":timestamp,
                "notas_bicicleta":{
                    "Fecha":data_list[0],
                    "Bicicleta":data_list[1],
                    "Rueda":data_list[2],
                    "Cámara":data_list[3],
                    "n° Pinchaduras":data_list[4],
                    "Cámara reemplazo":data_list[5]
                    }
                }
            
        def alta(*args):
            '''Send data to Firebase DB.'''
            try:
                # `self.user['idToken']` mandatory for user verification
                results = self.db.child(db_node).child(
                    datetime.now().strftime("%d-%m-%y(%H:%M:%S)")
                        ).set(data, self.user['idToken'])
                self.show_note("Datos enviados.")
                print("RESPUESTA:")
                print(results)

                # switch on "led"
                self.switch_redled(True)
                self.count = str(int(self.count)+1)
            except:
                self.show_note("No se pudo enviar.")
            self.app.close_warng()

        if format_error:
            self.show_note("Entrada incorrecta.")
        else:
            self.app.close_warng()
            self.app.warning(
                text="¿Enviar medidas?",
                ok_txt="Enviar",
                dism_txt="Cancelar",
                met1=alta
            )


class KeyBoardLis:
    '''Focus input by 'Enter key' behavior.'''
    def __init__(self, sc_man:ScManag):
        # For keyboard "key up" listening
        # NOTE: Tried with `on_key_down` and it didn't work
        Window.bind(on_key_up=self._keyup)
        self.sc_man = sc_man
        
    def _keyup(self, *args):
        '''
        Detects ENTER key when pressed. 
        Loop `focus` across `Input` of "corp_mes" screen.
        '''
        def switch_focus(text_in_l:str):
            '''
            args:
                - text_in_l: "input_fields" or "input_bike"
            '''
            # global `focus_txin` contein the focused `Input`.
            if focus_txin:
                ak.start(focus_txin.on_parent(focus_txin, getattr(self.sc_man.ids, text_in_l)))

        # after 'Enter' key release
        if args[1] == 13 and args[2] == 40:
            sc_name = self.sc_man.current_screen.name
            if sc_name == "corp_mes":
                texin_list = "input_fields"
            elif sc_name == "bike_notes":
                texin_list = "input_bike"
            else:
                raise Exception("KeyBoardLis: Wrong Screen!")

            switch_focus(texin_list)


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
        self.wresize["bar_fsize"] = str(int(Window.size[1]/18))
        self.wresize["bar_fsize2"] = str(int(Window.size[1]/25))
        self.wresize["input_font_s"] = str(int(Window.size[1]/15))
        self.wresize["warg_font_s"] = str(int(Window.size[1]/30))
        self.wresize["titl_font_s"] = str(int(Window.size[1]/25))
        # print(self.wresize["bar_fsize"])
    
    def warning(self, text:str, ok_txt:str, 
            dism_txt:str, met1, met2=None):
        '''Popup dialog with user.'''
        if met2:
            met2= self.close_warng

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