import os
import random
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import Screen
import cv2
import json
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDRectangleFlatButton
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
import time
import sqlite3
from ultralytics import YOLO
from kivy.utils import platform

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
if platform != "android":
    Window.size = (360, 600)

KV = '''
ScreenManager:
    IndexScreen:
    RegistrationScreen:
    LoginScreen:
    ProfileScreen:
    MainScreen:
    ReadMoreScreen:

<IndexScreen>:
    name: 'app_index'
    MDBoxLayout:
        id: index_screen
        orientation: 'vertical'

        MDFloatLayout:
            Image:
                id: index_logo
                source: 'bg.png'
                allow_stretch: True
                keep_ratio: True
                size_hint: (1, 1)  # Set size_hint to (1, 1) for full screen
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

            MDBoxLayout:
                orientation: 'horizontal'
                padding: dp(20), dp(10)  # Adjust the padding as needed
                size_hint: 0.9, None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5, "center_y": 0.93}  # Adjust position

                MDLabel:
                    id: rhetorical
                    text: ""
                    halign: "center"
                    valign: "middle"
                    size_hint_y: None
                    height: self.texture_size[1]  # Adjust height dynamically
                    text_size: self.width, None  # Restrict text to label width
                    color: (1, 1, 1, 1)  # White color
                    font_size: '15sp'
                    font_name: "Roboto"
                    bold: True
                    italic: True


<RegistrationScreen>:
    name: 'registration'
    MDFloatLayout:
        id: reg_screen
        orientation: 'vertical'
        MDTopAppBar:
            id: top_bar
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            title: 'Create an Account'
            elevation: 2
            pos_hint: {"center_x": 0.5, "center_y": 0.95}
            type: "top"
            height: dp(30)
        MDTextField:
            id: name_field
            hint_text: "Full Name"
            pos_hint: {"center_x": 0.5, "top": 0.90}
            size_hint_x: 0.8

        MDTextField:
            id: email_field
            hint_text: "Email Address"
            pos_hint: {"center_x": 0.5, "top": 0.82}
            size_hint_x: 0.8

        MDTextField:
            id: password_field
            hint_text: "Password"
            pos_hint: {"center_x": 0.5, "top": 0.74}
            size_hint_x: 0.8
            password: True

        MDTextField:
            id: confirm_password_field
            hint_text: "Confirm Password"
            pos_hint: {"center_x": 0.5, "top": 0.66}
            size_hint_x: 0.8
            password: True

        MDRectangleFlatButton:
            text: "Register"
            pos_hint: {"center_x": 0.5, "top": 0.13}
            size_hint_x: 0.35
            on_release: app.register_user()

        MDCard:
            size_hint: None, None
            size: "340dp", "230dp"  
            pos_hint: {"center_x": .5, "center_y": .35}
            md_bg_color: 0.8, 0.8, 0.8, 1
            radius: 10

            MDFloatLayout:  
                orientation: 'vertical'

                MDRectangleFlatButton:
                    text: "_______"
                    id: bmi_result_label
                    size_hint_y: None
                    height: dp(40)  
                    font_size: "18sp"  
                    bold: True  
                    text_color: 0, 2, 0, 1
                    pos_hint: {"center_x": .5, "center_y": .9}

                MDLabel:
                    text: "Select Gender:"
                    halign: "center"
                    font_style: "Subtitle1"  
                    size_hint_y: None
                    height: dp(30)  
                    color: 1, 0.5, 0, 1
                    pos_hint: {"center_x": .5, "center_y": .72}

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: None, None
                    padding: dp(3)
                    spacing: dp(3)  
                    pos_hint: {"center_x": .5, "center_y": .60}
                    width: dp(340)
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: None, None
                        width: dp(150)
                        padding: dp(10)
                        spacing: dp(3)  
                        MDCheckbox:
                            group: 'gender'
                            id: male_checkbox
                            size_hint_x: 0.5 
                            size: "20dp", "20dp"
                            padding: 3, 3
                            pos_hint: {"center_y": 0.5}

                        MDLabel:
                            text: "Male"
                            size_hint_x: 0.5 
                            width: dp(140)
                            valign: "center"

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: None, None
                        width: dp(150)
                        padding: dp(10)
                        spacing: dp(3)  

                        MDCheckbox:
                            group: 'gender'
                            id: female_checkbox
                            size_hint_x: 0.5 
                            padding: 3, 3
                            size: "20dp", "20dp"
                            pos_hint: {"center_y": 0.5}

                        MDLabel:
                            text: "Female"
                            size_hint_x: 0.5 
                            width: dp(140)
                            valign: "center"



                BoxLayout:  
                    size_hint_y: None
                    height: dp(70)  
                    spacing: dp(10)
                    padding: dp(10)
                    pos_hint: {"center_x": .5, "center_y": .40}  

                    MDTextField:
                        id: height_field
                        hint_text: "Enter Height (meters)"
                        size_hint_x: 0.5  
                        text_color: 1, 0.5, 0, 1 

                    MDTextField:
                        id: weight_field
                        hint_text: "Enter Weight (kg)"
                        size_hint_x: 0.5  
                        text_color: 1, 0.5, 0, 1 

                MDRectangleFlatButton:
                    text: "Calculate BMI"
                    size_hint_y: None
                    pos_hint: {"center_x": .5, "top": .23}  
                    height: dp(40)  # Set a fixed height for the button
                    on_release: app.calculate_bmi()



        MDLabel:
            text: "[color=ff7f00][ref=link]Already have an account? Click here![/ref][/color]"
            markup: True
            halign: "center"
            pos_hint: {"center_x": 0.5, "top": 0.07}
            size_hint_y: None
            height: dp(30)
            text_color: 0, 2, 0, 1
            font_size: "14sp"
            on_ref_press: app.change_screen('login')


<LoginScreen>:
    name: 'login'
    MDTopAppBar:
        id: top_bar
        left_action_items: [["arrow-left", lambda x: app.go_back()]]
        title: 'Users Login'
        elevation: 2
        pos_hint: {"center_x": 0.5, "center_y": 0.95}
        height: dp(30)
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15 , 15

        Image:
            id: logo_image
            source: 'camera_icon.png'
            size_hint: None, None
            size: dp(300), dp(300)
            allow_stretch: True
            keep_ratio: True
            pos_hint: {"center_x": 0.5, "center_y": 0.65}

        MDTextField:
            id: email_field
            hint_text: "Email"
            size_hint_y: None
            height: dp(60)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.75}
            padding: dp(10)

        MDTextField:
            id: password_field
            hint_text: "Password"
            password: True
            size_hint_y: None
            height: dp(60)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.65}
            padding:dp(10)

        MDRectangleFlatButton:
            text: "Log In"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            on_release: app.root.get_screen('login').login_user()

        MDLabel:
            text: "[color=ff7f00][ref=link]Don't have account? Click here![/ref][/color]"
            markup: True
            halign: "center"
            pos_hint: {"center_x": 0.5, "top": 0.03}
            size_hint_y: None
            height: dp(30)
            text_color: 0, 2, 0, 1
            font_size: "14sp"
            on_ref_press: app.change_screen('registration')

<ProfileScreen>
    name: 'profile'
    MDTopAppBar:
        id: top_bar
        left_action_items: [["arrow-left", lambda x: app.go_back()]]
        title: 'My Profile'
        elevation: 2
        pos_hint: {"center_x": 0.5, "center_y": 0.95}
        height: dp(30)
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15 , 15

        Image:
            id: profile_photo
            source: 'camera_icon.png'
            size_hint: None, None
            size: dp(100), dp(100)
            allow_stretch: True
            keep_ratio: True
            pos_hint: {"center_x": 0.5, "center_y": 0.65}

        MDTextField:
            id: name
            text: "Name"
            size_hint_y: None
            height: dp(40) 
            pos_hint: {"center_x": 0.5, "top": 0.75}
            padding: dp(10)
            readonly: True

        MDTextField:
            id: email
            text: "Email"
            size_hint_y: None
            height: dp(40)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.75}
            padding: dp(10)
            readonly: True

        MDTextField:
            id: gender
            text: "Gender"
            size_hint_y: None
            height: dp(40)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.65}
            padding:dp(10)
            readonly: True

        MDTextField:
            id: weight
            text: "Weight"
            size_hint_y: None
            height: dp(40)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.75}
            padding: dp(10)
            readonly: True

        MDTextField:
            id: height
            text: "Height"
            size_hint_y: None
            height: dp(40)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.75}
            padding: dp(10)
            readonly: True

        MDTextField:
            id: bmi
            text: "BMI"
            size_hint_y: None
            height: dp(40)  # Increased height
            pos_hint: {"center_x": 0.5, "top": 0.75}
            padding: dp(10)
            readonly: True

        MDRectangleFlatButton:
            text: "Logout"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_release: app.root.get_screen('profile').logout_user()

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        id: main_screen
        orientation: 'vertical'
        MDTopAppBar:
            id:top_bar
            left_action_items: [["menu", lambda x: app.callback(x)]]
            right_action_items: [["account-box", lambda x: app.manage_screen()]]
            title: 'Fruit Recognition'
            elevation: 2
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDFloatLayout:
            Image:
                id: logo_image
                source: 'camera_icon.png'
                size_hint: None, None
                size: dp(300), dp(300)
                allow_stretch: True
                keep_ratio: True
                pos_hint: {"center_x": 0.5, "center_y": 0.65}

            MDLabel:
                id: result_label
                text: ""
                halign: "center"
                pos_hint: {"center_x": 0.5, "center_y": 0.27}
                padding: (10, 10, 10, 10)

            MDLabel:
                id: desc_label
                text: "Use camera or upload an image"
                halign: "center"
                pos_hint: {"center_x": 0.5, "center_y": 0.15}
                padding: (10, 10, 10, 10)

            MDRectangleFlatButton:
                id: nutritional_facts_button
                text: "Nutritional Facts"
                pos_hint: {"center_x": 0.5, "center_y": 0.15}
                size_hint_x: 0.5
                opacity: 0  # Start hidden
                disabled: True  # Disable it initially
                on_release: app.menu_callback("Read More")


        MDBottomAppBar:
            MDTopAppBar:
                left_action_items: [["file-image", lambda x: app.show_file_chooser()]]
                right_action_items: [["restore", lambda x: app.restart()]]
                icon: 'camera'
                icon_size:"300sp"
                padding: (10, 10, 10, 10)
                type: "bottom"
                on_action_button: app.capture()


<ReadMoreScreen>:
    name: 'read_more'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            id: top_bar
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            title: 'Nutritional Facts'
            elevation: 2
            size_hint_y: None
            height: dp(56)

        MDFloatLayout:
            size_hint_y: None
            height: dp(250)  # Adjusted height to fit the image better
            Image:
                id: logo
                source: 'camera_icon.png'
                size_hint: None, None
                size: dp(240), dp(240)  # Adjust size to a more appropriate value
                allow_stretch: True
                keep_ratio: True
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

        ScrollView:
            size_hint_y: 1 
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(5)
                size_hint_y: None 
                height: self.minimum_height  

                MDRectangleFlatButton:
                    text: "Nutritional Facts"
                    halign: "center"
                    pos_hint: {"center_x": 0.5}
                    font_style: "H6"
                    size_hint_y: None
                    height: dp(40)
                    text_color: (1, 1, 1, 1)
                    md_bg_color: (0.5, 0.5, 0.5, 1)

                MDGridLayout:
                    id: nutritional_grid
                    cols: 2  
                    row_default_height: dp(40)  
                    size_hint_y: None 
                    height: self.minimum_height  
                    padding: dp(5)
                    spacing: dp(5)
'''


class IndexScreen(Screen):

    def on_touch_down(self, touch):
        self.manager.current = 'main'
        return super().on_touch_down(touch)

    def on_enter(self):
        # Delay the label change to ensure the UI is ready
        Clock.schedule_once(self.delayed_change_label, 0.1)

    def delayed_change_label(self, *args):
        self.change_label()

    def change_label(self):
        questions = [
            "Could the vibrant colors of fruits hint at the spectrum of nutrients within?",
            "Isn't it intriguing how nature encodes health benefits into each fruit's composition?",
            "Have you ever pondered the nutritional symphony within every bite of fruit?",
            "Can we truly grasp the complexity of vitamins and minerals dancing within fruits?",
            "Isn't it remarkable how scanning fruit nutrients unveils a tapestry of wellness?",
            "Have you ever wondered about the intricate balance of nutrients tailored by nature?",
            "Could the richness of fruit nutrients be nature's gift for our well-being?",
            "Isn't it fascinating how each fruit's nutrient profile tells a unique story of vitality?",
            "Can we fully appreciate the bounty of nature's pharmacy encapsulated in fruits?",
            "Have you ever paused to marvel at the biological wonders concealed within fruits?",
            "If we don’t fuel our bodies with the right nutrients, how can we expect to feel energized and healthy?",
            "Can we truly thrive without giving our bodies the vitamins and minerals they need?",
            "Why settle for feeling tired and sluggish when a balanced diet can boost our vitality?",
            "Isn’t it obvious that what we eat directly affects how we feel?",
            "Who doesn’t want to boost their immunity with the power of whole foods and essential nutrients?",
            "Can we really ignore the impact of poor nutrition on our long-term health?",
            "Why choose processed junk food when nature has provided us with so many nutrient-rich options?",
            "Is it surprising that our mental clarity and mood are influenced by what we feed our bodies?",
            "How could anyone mistake the vibrant color of a ripe mango or the distinctive shape of a pineapple?",
            "Isn't it fascinating how each fruit has its own unique texture, flavor, and scent?",
            "Who wouldn’t recognize the unmistakable smell of a freshly cut orange or lemon?",
            "Isn’t it incredible that nature gives us such clear signs when fruit is perfectly ripe?",
            "How could we forget the familiar crunch of an apple or the smooth softness of a banana?",
            "Aren’t the bright colors of berries and citrus fruits nature’s way of catching our attention?",
            "Is there anything more delightful than recognizing your favorite fruit at the peak of its season?",
            "How can we not appreciate the variety and beauty of fruits, each with its own unique design and taste?",
            "Isn’t it amazing how we can instantly identify a fruit just by its aroma or color without even tasting it?",
            "Who could confuse the spiky texture of a durian with the smooth skin of a pear?",
            "Isn’t the diversity of fruits remarkable, with each one having its own recognizable shape and flavor?",
            "How can we not marvel at the way nature signals ripeness through the changing colors of fruits like bananas or avocados?",
            "Isn't it incredible how easily we can recognize fruits we’ve never even tasted, just by their look and smell?",
            "Can anyone resist the vibrant, recognizable allure of a perfectly red strawberry or deep purple grapes?",
            "Isn’t it clear that a balanced diet is the foundation of good health?",
            "How can we expect to thrive if our meals lack the right balance of proteins, carbs, and healthy fats?",
            "Can we really achieve optimal health without paying attention to what’s on our plate?",
            "Isn’t it obvious that our body functions best when we provide it with a diverse range of nutrients?",
            "Why settle for nutrient-poor meals when a well-rounded diet can boost both body and mind?",
            "How can we ignore the importance of dietary composition when it directly affects our energy, mood, and long-term health?",
            "Can we expect our bodies to perform well if we fuel them with unbalanced or processed foods?",
            "Isn’t it time to rethink our dietary choices when we know how much they impact our wellbeing?"
        ]
        if self.ids.get('rhetorical'):
            rand_index = random.randint(0, len(questions) - 1)
            random_question = questions[rand_index]
            self.ids.rhetorical.text = random_question
        else:
            print("Rhetorical ID not found.")


class RegistrationScreen(Screen):

    def calculate_bmi(self):
        try:
            height = float(self.ids.height_field.text)
            weight = float(self.ids.weight_field.text)
            bmi = weight / (height ** 2)
            self.ids.bmi_result_label.text = f"Your BMI: {bmi:.2f}"
        except ValueError:
            self.ids.bmi_result_label.text = "Invalid input. Please enter numbers."

    def register_user(self):
        name = self.ids.name_field.text
        email = self.ids.email_field.text
        password = self.ids.password_field.text
        confirm_password = self.ids.confirm_password_field.text
        height = self.ids.height_field.text
        weight = self.ids.weight_field.text
        selected_gender = None
        bmi = None

        if height and weight:
            height_in_meters = float(height)
            weight_in_kg = float(weight)
            bmi = weight_in_kg / (height_in_meters ** 2)

        if self.ids.male_checkbox.active:
            selected_gender = "Male"
        elif self.ids.female_checkbox.active:
            selected_gender = "Female"

        # Validate input fields
        if not name or not email or not password or not height or not weight or not selected_gender or not bmi:
            self.show_dialog("Please fill in all fields.")
            app = MDApp.get_running_app()
            app.change_screen('registration')
            # Clear the password fields for user to re-enter
            self.ids.password_field.text = ''
            self.ids.confirm_password_field.text = ''
            return

        if password != confirm_password:
            self.show_dialog("Passwords do not match.")
            app = MDApp.get_running_app()
            app.change_screen('registration')
            # Clear the password fields for user to re-enter
            self.ids.password_field.text = ''
            self.ids.confirm_password_field.text = ''
            return

        # Insert the data into the database
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users 
                            (name, email, password, bmi, height, weight, gender) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (name, email, password, bmi, height, weight, selected_gender))
            conn.commit()
            conn.close()

            self.show_dialog("Registration successful!")
            # Clear the input fields
            self.ids.name_field.text = ''
            self.ids.email_field.text = ''
            self.ids.password_field.text = ''
            self.ids.confirm_password_field.text = ''
            self.ids.height_field.text = ''
            self.ids.weight_field.text = ''
            app = MDApp.get_running_app()
            app.current_user = {
                'name': name,
                'email': email,
                'password': password,
                'bmi': bmi,
                'height': height,
                'weight': weight,
                'gender': selected_gender
            }
            app.change_screen('main')

        except sqlite3.IntegrityError:
            self.show_dialog("Email already registered.")
            app = MDApp.get_running_app()
            app.change_screen('registration')

        except Exception as e:
            self.show_dialog(f"An error occurred: {e}")

    def show_dialog(self, message):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Message",
            text=message,
            size_hint=(0.8, None),
            height='150dp',
            radius=[20, 20, 20, 20],
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()


class LoginScreen(Screen):

    def on_enter(self):
        # Delay the label change to ensure the UI is ready
        Clock.schedule_once(self.delayed_clear, 0.1)

    def delayed_clear(self, *args):
        self.clear_fields()

    def clear_fields(self):
        self.ids.email_field.text = ""
        self.ids.password_field.text = ""

    def login_user(self):
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()

        if not email or not password:
            self.show_dialog("Please fill in all fields.")
            return

        try:
            conn = sqlite3.connect('app.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                self.show_dialog("Login successful!")
                app = MDApp.get_running_app()

                # Store the current user information in the app object
                app.current_user = {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'bmi': user['bmi'],
                    'height': user['height'],
                    'weight': user['weight'],
                    'gender': user['gender']
                }

                # Store the user's email in a local file for auto-login
                with open("login_info.txt", "w") as f:
                    f.write(email)

                # Change the screen to the main screen
                app.change_screen('main')
            else:
                self.show_dialog("Invalid email or password.")
        except Exception as e:
            self.show_dialog(f"An error occurred: {e}")

    def clear_fields(self):
        self.ids.email_field.text = ""
        self.ids.password_field.text = ""

    def show_dialog(self, message):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Message",
            text=message,
            size_hint=(0.8, None),  # Set size hint for width and flexible height
            height='150dp',  # Adjust height to avoid unnecessary stretching
            radius=[20, 20, 20, 20],  # Rounded corners for a modern look
            buttons=[
                MDRaisedButton(  # Use MDRaisedButton for a cleaner UI
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()


class ProfileScreen(Screen):

    def on_enter(self):
        # Delay the label change to ensure the UI is ready
        Clock.schedule_once(self.delayed_change_label, 0.1)

    def delayed_change_label(self, *args):
        self.update_profile()

    def update_profile(self):
        app = MDApp.get_running_app()
        user_info = app.current_user
        self.ids.name.text = 'Name : ' + user_info.get('name', '')
        self.ids.email.text = 'Email : ' + user_info.get('email', '')
        self.ids.gender.text = 'Gender : ' + user_info.get('gender', '')
        self.ids.height.text = 'Height : ' + user_info.get('height', '') + ' meters'
        self.ids.weight.text = 'Weight : ' + user_info.get('weight', '') + ' kilograms'
        bmi = user_info.get('bmi', None)
        if bmi is not None:
            bmi = float(bmi)
            self.ids.bmi.text = 'My BMI: {:.2f}'.format(bmi)
        else:
            self.ids.bmi.text = 'My BMI: Not available'

    def logout_user(self):
        app = MDApp.get_running_app()
        app.current_user = {}
        if os.path.exists("login_info.txt"):
            os.remove("login_info.txt")
        self.show_dialog("You have been logged out.")
        app.change_screen('login')

    def show_dialog(self, message):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Message",
            text=message,
            size_hint=(0.8, None),  # Set size hint for width and flexible height
            height='150dp',  # Adjust height to avoid unnecessary stretching
            radius=[20, 20, 20, 20],  # Rounded corners for a modern look
            buttons=[
                MDRaisedButton(  # Use MDRaisedButton for a cleaner UI
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.camera = None
        self.img = None
        self.label = None
        self.disease_button = None
        self.model = None
        self.class_names = None
        self.popup = None
        self.class_name = "Fruit"
        self.img_path = "camera_icon.png"
        # Load the model and class names
        self.load_model_and_classes()

    def on_enter(self):
        Clock.schedule_once(self.delayed_change_label, 0.1)

    def delayed_change_label(self, *args):
        self.check_session()
        self.change_title()
        self.auto_login()

    def auto_login(self):
        # Check if the login_info.txt file exists
        if os.path.exists("login_info.txt"):
            with open("login_info.txt", "r") as f:
                email = f.read().strip()

            try:
                # Try to fetch the user from the database
                conn = sqlite3.connect('app.db')
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
                user = cursor.fetchone()
                conn.close()

                if user:
                    app = MDApp.get_running_app()

                    app.current_user = {
                        'id': user['id'],
                        'name': user['name'],
                        'email': user['email'],
                        'bmi': user['bmi'],
                        'height': user['height'],
                        'weight': user['weight'],
                        'gender': user['gender']
                    }

                    app.change_screen('main')
                else:
                    self.show_dialog("Auto-login failed, please log in manually.")
            except Exception as e:
                self.show_dialog(f"An error occurred during auto-login: {e}")

    def change_title(self):
        app = MDApp.get_running_app()
        user_info = app.current_user

        if isinstance(user_info, dict):
            self.ids.top_bar.title = user_info.get('name', 'Fruit Recognition')
        else:
            self.ids.top_bar.title = "Fruit Recognition"

    def check_session(self):
        app = MDApp.get_running_app()
        user_info = app.current_user

        if isinstance(user_info, dict):
            for key, value in user_info.items():
                print(f"{key}: {value}")
        else:
            print("No user is logged in or user_info is not a dictionary.")

    def getImgPath(self):
        return self.img_path

    def getClassName(self):
        return self.class_name

    def restart(self):
        self.ids.logo_image.source = "camera_icon.png"
        self.ids.result_label.text = ""
        self.ids.desc_label.text = ""

    def load_model_and_classes(self):
        try:
            # Load the YOLO model
            self.model = YOLO('best_model.tflite')
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            self.ids.result_label.text = f"Error loading model: {str(e)}"  # Display error on the UI

        try:
            # Load the class names
            with open('model_artifacts.json') as f:
                self.class_names = json.load(f)
            print("Class names loaded successfully!")
        except Exception as e:
            print(f"Error loading class names: {e}")
            self.ids.result_label.text = f"Error loading class names: {str(e)}"  # Display error on the UI

    def capture(self, *args):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.camera = Camera(play=True, resolution=(640, 480))
        content.add_widget(self.camera)

        save_button = MDIconButton(
            icon="camera_icon.png",
            size=(dp(150), dp(150)),
            icon_size=dp(100),
            size_hint=(None, None),  # Keep the size_hint as is
            on_press=self.capture_image,
            pos_hint={"center_x": 0.5}
        )

        content.add_widget(save_button)

        self.popup = Popup(title="Camera", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def capture_image(self, instance):
        # Open the default camera with better settings
        cam_port = 0
        cam = cv2.VideoCapture(cam_port, cv2.CAP_DSHOW)

        # Set the resolution of the camera
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Consider using a lower resolution for faster initialization
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Allow the camera to warm up for a short period
        time.sleep(1)

        # Capture a single frame
        result, image = cam.read()

        result = True

        if result and image is not None:
            img_path = "captured_image.png"
            self.img_path = img_path

            # Save the image with high quality
            cv2.imwrite(img_path, image)

            # Update image source in UI
            self.ids.logo_image.source = img_path
            self.ids.logo_image.reload()

            # Release the camera
            cam.release()

            # Classify the flower using the captured image
            self.identify_fruit(img_path)
            self.popup.dismiss()
        else:
            print("Error: Unable to capture image from the camera.")
            cam.release()

    def show_file_chooser(self, *args):
        layout = BoxLayout(orientation='vertical')

        # Create FileChooser
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.selected)

        # Create Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50)
        back_button = Button(text='Back')
        ok_button = Button(text='OK')

        # Bind button actions
        back_button.bind(on_release=self.on_back)
        ok_button.bind(on_release=lambda btn: self.selected(filechooser, filechooser.selection))

        # Add widgets to layout
        button_layout.add_widget(back_button)
        button_layout.add_widget(ok_button)
        layout.add_widget(filechooser)
        layout.add_widget(button_layout)

        # Create and open Popup
        self.popup = Popup(title="Select Image", content=layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def on_back(self, instance):
        # Handle back button action
        self.popup.dismiss()

    def selected(self, filechooser, selection, *args):
        if selection:
            self.ids.logo_image.source = selection[0]
            self.img_path = selection[0]
            self.ids.logo_image.reload()
            self.identify_fruit(selection[0])
            self.popup.dismiss()

    def identify_fruit(self, img_path):
        try:
            print(f"Detecting fruit in image: {img_path}")
            results = self.model.predict(source=self.img_path, imgsz=640, conf=0.5)
            print("Results:", results)  # Print results for debugging
            self.process_output(results)
        except Exception as e:
            print(f"Error detecting fruit: {str(e)}")

    def process_output(self, results):
        try:
            for result in results:
                boxes = result.boxes
                if hasattr(boxes, 'xyxy'):
                    if len(boxes.xyxy) > 0:
                        for box, cls, conf in zip(boxes.xyxy, boxes.cls, boxes.conf):
                            class_name = self.model.names[int(cls)]
                            print(f"Detected {class_name} with confidence {conf:.2f} at {box.tolist()}")
                            if conf < 0.70:
                                self.ids.result_label.text = "Image could not identify clearly "
                                button = self.ids.nutritional_facts_button
                                button.opacity = 0
                                button.disabled = True
                            else:
                                self.ids.result_label.text = f"Recognized as: {class_name} with an accuracy of {conf * 100:.2f}%"
                                self.ids.desc_label.text = ""
                                button = self.ids.nutritional_facts_button
                                button.opacity = 1
                                button.disabled = False
                            self.class_name = class_name
                    else:
                        print("No bounding boxes found in results.")
                        self.ids.result_label.text = "Image could not be recognized"
                        button = self.ids.nutritional_facts_button
                        button.opacity = 0
                        button.disabled = True
                else:
                    print("No boxes attribute found in results.")
                    self.ids.result_label.text = "Image could not be recognized"

        except Exception as e:
            print(f"Error processing output: {str(e)}")
            self.ids.result_label.text = f"Error processing output: {str(e)}"  # Update UI with error


class ReadMoreScreen(Screen):

    def update_text(self, text):
        self.ids.read_more_label.text = text

    def update_title(self, title):
        self.ids.top_bar.title = title

    def update_image(self, img_path):
        self.ids.logo.source = img_path

    def populate_table(self, nutritional_facts, class_name):
        # Clear previous data in the grid
        nutritional_grid = self.ids.nutritional_grid
        nutritional_grid.clear_widgets()

        # Add headers as buttons
        # Adding headers for Nutrient and Value
        # Adding headers for Nutrient and Value with bold text and gray background
        nutritional_grid.add_widget(
            MDRectangleFlatButton(
                text="Nutrient",
                pos_hint={"center_x": 0.5},
                size_hint=(0.5, None),  # Take half the width of the screen
                height=dp(30),  # Fixed height
                theme_text_color="Custom",  # Allow custom text color
                text_color=(1, 1, 1, 1),  # Set text color to white for better contrast
                md_bg_color=(0.5, 0.5, 0.5, 1),  # Set background color to gray
                font_style="H6"  # Use H6 style for bold text
            )
        )
        nutritional_grid.add_widget(
            MDRectangleFlatButton(
                text="Value",
                pos_hint={"center_x": 0.5},
                size_hint=(0.5, None),  # Take half the width of the screen
                height=dp(30),  # Fixed height
                theme_text_color="Custom",  # Allow custom text color
                text_color=(1, 1, 1, 1),  # Set text color to white for better contrast
                md_bg_color=(0.5, 0.5, 0.5, 1),  # Set background color to gray
                font_style="H6"  # Use H6 style for bold text
            )
        )

        # Populate the grid with nutritional facts for the selected class
        if class_name in nutritional_facts:
            for nutrient, value in nutritional_facts[class_name].items():
                # Create a box layout to center the buttons for nutrients
                nutrient_box = MDBoxLayout(size_hint_y=None, height=dp(20), padding=[dp(2), dp(2)], spacing=dp(2))
                nutrient_box.add_widget(
                    MDRectangleFlatButton(
                        text=nutrient.capitalize(),
                        size_hint=(0.5, None),  # Take half the width of the screen
                        height=dp(20),
                        pos_hint={"center_x": 0.5}  # Centering within the box layout
                    )
                )
                nutritional_grid.add_widget(nutrient_box)

                # Create a box layout for the value
                value_box = MDBoxLayout(size_hint_y=None, height=dp(20), padding=[dp(2), dp(2)], spacing=dp(2))
                value_box.add_widget(
                    MDRectangleFlatButton(
                        text=value,
                        size_hint=(0.5, None),  # Take half the width of the screen
                        height=dp(20),
                        pos_hint={"center_x": 0.5}  # Centering within the box layout
                    )
                )
                nutritional_grid.add_widget(value_box)

        else:
            # Optionally handle the case where class_name is not found
            nutritional_grid.add_widget(
                MDRectangleFlatButton(
                    text="No data available",
                    size_hint=(0.5, None),  # Take half the width of the screen
                    height=dp(50),
                    pos_hint={"center_x": 0.5}
                )
            )
            nutritional_grid.add_widget(
                MDRectangleFlatButton(
                    text="",  # Empty button to maintain structure
                    size_hint=(0.5, None),  # Take half the width of the screen
                    height=dp(50),
                    pos_hint={"center_x": 0.5}
                )
            )


class FruitRecognitionApp(MDApp):
    icon_color = get_color_from_hex("#74C365")

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M2"
        menu_items = [
            {
                "text": "More Info",
                "on_release": lambda x="Read More": self.menu_callback(x),
            }
        ]
        self.menu = MDDropdownMenu(items=menu_items)
        self.current_user = None
        screen = Builder.load_string(KV)
        return screen

    def on_start(self):
        self.setup_database()

    def change(self):
        index_screen = self.root.get_screen('index_screen')
        index_screen.change_label()

    def setup_database(self):
        # Create the database and users table (run once to create the table)
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            email TEXT UNIQUE,
                            password TEXT,
                            bmi TEXT,
                            height TEXT,
                            weight TEXT,
                            gender TEXT
                        )''')
        conn.commit()
        conn.close()

    def register_user(self):
        reg_screen = self.root.get_screen('registration')
        reg_screen.register_user()

    def user_profile(self):
        self.root.current = "profile"

    def manage_screen(self):
        if self.current_user:
            self.user_profile()
        else:
            self.change_screen('login')

    def calculate_bmi(self):
        reg_screen = self.root.get_screen('registration')
        reg_screen.calculate_bmi()

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def show_file_chooser(self):
        main_screen = self.root.get_screen('main')
        main_screen.show_file_chooser()

    def capture(self):
        main_screen = self.root.get_screen('main')
        main_screen.capture()

    def go_back(self):
        self.root.current = 'main'

    def restart(self):
        main_screen = self.root.get_screen('main')
        main_screen.restart()

    def create_dropdown_menu(self):
        main_screen = self.root.get_screen('main')
        main_screen.create_dropdown_menu()

    def change_theme(self, instance):
        # Toggle the theme
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
            instance.icon = "toggle-switch-off-outline"
        else:
            self.theme_cls.theme_style = "Dark"
            instance.icon = "toggle-switch"

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        main_screen = self.root.get_screen('main')
        class_name = main_screen.getClassName()
        class_image = main_screen.getImgPath()
        self.menu.dismiss()
        self.root.current = 'read_more'

        # Update the text based on the menu selection
        read_more_screen = self.root.get_screen('read_more')

        if text_item == "Read More":
            read_more_screen.update_title(class_name)
            read_more_screen.update_image(class_image)
            # Define the dictionary
            nutritional_facts = {
                'pre-mature coconut': {
                    'calories': '44 kcal',
                    'carbohydrates': '9.0g',
                    'protein': '0.5g',
                    'sugars': '3.4g',
                    'vitamin_C': '2.0mg',
                },
                'over-mature coconut': {
                    'calories': '354 kcal',
                    'carbohydrates': '15.2g',
                    'protein': '3.3g',
                    'sugars': '6.2g',
                    'vitamin_C': '3.0mg',
                },
                'ripe mango': {
                    'calories': '60 kcal',
                    'carbohydrates': '15g',
                    'protein': '0.8g',
                    'sugars': '14g',
                    'vitamin_C': '36.4mg',
                },
                'unripe mango': {
                    'calories': '60 kcal',
                    'carbohydrates': '15g',
                    'protein': '0.8g',
                    'sugars': '14g',
                    'vitamin_C': '36.4mg',
                },
                'overripe mango': {
                    'calories': '70 kcal',
                    'carbohydrates': '17.0g',
                    'protein': '0.8g',
                    'sugars': '15.0g',
                    'vitamin_C': '36.4mg',
                },
                'ripe pineapple': {
                    'calories': '50 kcal',
                    'carbohydrates': '13.1g',
                    'protein': '0.5g',
                    'sugars': '9.9g',
                    'vitamin_C': '47.8mg',
                },
                'unripe pineapple': {
                    'calories': '45 kcal',
                    'carbohydrates': '11.1g',
                    'protein': '0.5g',
                    'sugars': '7.5g',
                    'vitamin_C': '17.4mg',
                },
                'overripe pineapple': {
                    'calories': '55 kcal',
                    'carbohydrates': '14.8g',
                    'protein': '0.4g',
                    'sugars': '40.0g',
                    'vitamin_C': '10mg',
                },
                'ripe banana': {
                    'calories': '89 kcal',
                    'carbohydrates': '22.8g',
                    'protein': '1.1g',
                    'sugars': '12g',
                    'vitamin_C': '0.4mg',
                },
                'unripe banana': {
                    'calories': '70 kcal',
                    'carbohydrates': '17.5g',
                    'protein': '0g',
                    'sugars': '0g',
                    'vitamin_C': '7.5mg',
                },
                'overripe banana': {
                    'calories': '90 kcal',
                    'carbohydrates': '22.8g',
                    'protein': '1.1g',
                    'sugars': '12.2g',
                    'vitamin_C': '8.7mg',
                },
                'ripe guava': {
                    'calories': '68 kcal',
                    'carbohydrates': '14.7g',
                    'protein': '2.6g',
                    'sugars': '5g',
                    'vitamin_C': '228.3mg',
                },
                'unripe guava': {
                    'calories': '68 kcal',
                    'carbohydrates': '14.6g',
                    'protein': '2.6g',
                    'sugars': '5g',
                    'vitamin_C': '228.3mg',
                },
                'overripe guava': {
                    'calories': '68 kcal',
                    'carbohydrates': '14.7g',
                    'protein': '2.6g',
                    'sugars': '8.9g',
                    'vitamin_C': '228.3mg',
                },
                'ripe tomato': {
                    'calories': '18 kcal',
                    'carbohydrates': '3.9g',
                    'protein': '0.9g',
                    'sugars': '2.6g',
                    'vitamin_C': '13.7mg',
                },
                'unripe tomato': {
                    'calories': '20 kcal',
                    'carbohydrates': '4.6g',
                    'protein': '1.0g',
                    'sugars': '2.5g',
                    'vitamin_C': '14mg',
                },
                'overripe tomato': {
                    'calories': '22 kcal',
                    'carbohydrates': '4.8g',
                    'protein': '0.8g',
                    'sugars': '3.2g',
                    'vitamin_C': '10mg',
                },
            }

            read_more_screen.populate_table(nutritional_facts, class_name)


if __name__ == '__main__':
    FruitRecognitionApp().run()
