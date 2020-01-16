from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from WikiGame import Proccessus

class MainScreen(GridLayout,Proccessus):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cols = 5

        self.page = 1
        self.tour = 1
        self.lastPage = []

        self.pageDepart = Proccessus.ChooseRandomPage(self)
        self.pageCible = Proccessus.ChooseRandomPage(self)
        self.pageActuelle = self.pageDepart

        self.lastPage.append(self.pageActuelle)

        self.Recharge() 

    def Header(self):
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='WikiGame', font_size='40sp'))
        self.add_widget(Label(text='-----------------------'))
        self.add_widget(Label(text='Tour n°{}'.format(self.tour), font_size='40sp'))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        buttonRestart = Button(text='Recommencer', background_normal="1.jpg")
        buttonRestart.bind(on_press=self.Restart)
        self.add_widget(buttonRestart)
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Départ : '+self.pageDepart))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Cible : '+self.pageCible))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Actuelle : '+self.pageActuelle))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

    def Restart(self,instance):
        self.pageDepart = Proccessus.ChooseRandomPage(self)
        self.pageCible = Proccessus.ChooseRandomPage(self)
        self.pageActuelle = self.pageDepart

        self.Recharge()

    def ButtonList(self):
        self.myList = Proccessus.GetUrl(self, self.pageActuelle.replace(' ','_'))
        self.ButtonRetour()
        if len(self.myList) < 20:
            mini = 0
            maxi = len(self.myList)
        else:
            mini = (self.page-1)*20
            if len(self.myList) < self.page*20:
                maxi = len(self.myList)
            else:
                maxi = self.page*20
        for target in range(mini,maxi):
            number = target+1
            if number < 10:
                button = Button(text="0{} : {}".format(number,self.myList[target][1]), background_down="2.jpg")
            else:
                button = Button(text="{} : {}".format(number,self.myList[target][1]), background_down="2.jpg")

            button.bind(on_press=self.ButtonPress)
            self.add_widget(button)
        
        self.RetourChariot(20-maxi)
        self.ButtonsNavigation()

    def ButtonPress(self, instance):
        choice = int(instance.text.split(':')[0])
        self.choice = None
        self.page = 1
        self.pageActuelle = self.myList[choice-1][0]
        self.lastPage.append(self.pageActuelle)
        if self.pageActuelle == self.pageCible:
            self.Victory()
        else:
            self.tour += 1
            self.Recharge()
    
    def Victory(self):
        self.add_widget(Label(text='Victoire en {} tours !'.format(self.tour)))

    def RetourPress(self, instance):
        self.lastPage.pop()
        self.pageActuelle = self.lastPage[len(self.lastPage)-1]
        self.Recharge()

    def NavigationPress(self, instance):
        if "-1" in instance.text:
            self.page -= 1
            self.Recharge()
        elif "-2" in instance.text:
            self.page += +1
            self.Recharge()

    def Recharge(self):
        Widget.clear_widgets(self)
        self.Header()
        self.ButtonList()

    def ButtonRetour(self):
        if len(self.lastPage) != 1:
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            buttonRetour = Button(text='00 : Retour', background_normal="1.jpg")
            buttonRetour.bind(on_press=self.RetourPress)
            self.add_widget(buttonRetour)
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
    
    def RetourChariot(self,number):
        if number != 0:
            for target_list in range(number%5):
                self.add_widget(Label(text=''))

    def ButtonsNavigation(self):
        buttonPrecedent = Button(text='-1 : Liens précédents', background_normal="1.jpg")
        buttonPrecedent.bind(on_press=self.NavigationPress)

        buttonSuivant = Button(text='-2 : Liens suivants', background_normal="1.jpg")
        buttonSuivant.bind(on_press=self.NavigationPress)

        if self.page != 1 and len(self.myList) > (20*self.page):
            self.add_widget(Label(text=''))
            self.add_widget(buttonPrecedent)
            self.add_widget(Label(text=''))
            self.add_widget(buttonSuivant)
            self.add_widget(Label(text=''))

        elif self.page == 1 and len(self.myList) > (20*self.page):
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            self.add_widget(buttonSuivant)
            self.add_widget(Label(text=''))

        elif self.page != 1 and len(self.myList) <= (20*self.page):
            self.add_widget(Label(text=''))
            self.add_widget(buttonPrecedent)
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))

class MyApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()