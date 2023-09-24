from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class Format(Widget):
    def button_pressed(self):
        print(self.ids.username.text)
    pass

class passwordManager(App):
    def build(self):
        

        return Format()

    
   
        

        
    

if __name__ == "__main__":
    passwordManager().run()