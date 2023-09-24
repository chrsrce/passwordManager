import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.switch import Switch
from kivy.properties import NumericProperty

class masterLoginFormat(Screen):

    bad_credentials_counter = NumericProperty(0)
    bad_attempt = False
    too_many_attempts = False
    def button_pressed(self):

        
        master_user = self.ids.username.text
        master_pass = self.ids.password.text
        print(self.ids.username.text)

        
        if master_user == 'admin' and master_pass == 'admin':
            print("correct")

            masterlogin.screen_manager.current = 'Dashboard'
        else:
            self.bad_credentials_counter +=1
            self.wrong_creds = Label(
                text = "Wrong Credentials : try again",
                color = 'AA4A44',
                pos = (0,100)
            )    

 ######################### ######################### 
#########################  PROBLEM ######################### 
# widget wont remove (line 47)
 ######################### ######################### 
            if self.bad_credentials_counter == 1:
                self.add_widget(self.wrong_creds)
                print('once')
            elif self.bad_credentials_counter == 3:
                self.remove_widget(self.wrong_creds)
                print('gi')
 ################################# 
            print(self.bad_credentials_counter)
            if self.bad_credentials_counter == 3:
                self.too_many_attempts = Label(
                text = "Account has been locked out, due to too many attempts...",
                color = 'AA4A44',
                pos = (0,100)       

                )   
            if self.bad_credentials_counter == 3:
                self.add_widget(self.too_many_attempts) 
                self.remove_widget(self.wrong_creds)    
                
          
      #  if self.bad_attempt == True and self.bad_credentials_counter == 1:
      #      self.add_widget(self.wrong_creds)
       # elif self.bad_attempt == True and self.too_many_attempts == True:
       #     self.add_widget(self.too_many_attemps)
       #     print("test")
       #     self.remove_widget(self.wrong_creds)

           
        
    pass

class dashboardFormat(Screen):
    pass

class masterLogin(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.mainscreen = masterLoginFormat()
        screen = Screen(name='Master Login Screen')
        screen.add_widget(self.mainscreen)
        self.screen_manager.add_widget(screen)

        self.dashboard = dashboardFormat()
        screen = Screen(name = 'Dashboard')
        screen.add_widget(self.dashboard)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

class dashboard(App):
    def build(self):

        pass
   
        

        
    



masterlogin = masterLogin()
masterlogin.run()