from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from WikiGame import Proccessus
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock

class MainScreen(GridLayout,Proccessus):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.StartGame()

        # fonction déclenché toutes les secondes
        Clock.schedule_interval(self.Timer, 1)

        # fond d'écran
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos, source='1.jpg')

        self.bind(size=self._update_rect, pos=self._update_rect)

    
    def Defeat(self,dt):
        # défaite affichage
        Widget.clear_widgets(self)
        self.cols = 1
        # nombre de tours en 10 minutes
        self.add_widget(Label(text='Vous avez perdu !', font_size='60sp', bold=True))
        self.add_widget(Label(text='Vous avez effectué {} tours en 10 minutes !'.format(self.tour), font_size='60sp', bold=True))
        self.add_widget(Label(text='Historique : ', font_size='40sp', bold=True))
        # historique
        for index in range(0,len(self.lastPage)):
            self.add_widget(Label(text='- Tour n°{} : {}'.format(index+1, self.lastPage[index][1]), font_size='20sp', bold=True))
        self.Footer()

    
    def Timer(self, dt):
        # timer déclenché chaque seconde
        minutes = self.timer[0]
        secondes = self.timer[1]
        secondes += 1

        if secondes == 60:
            secondes = 0
            minutes += 1
        
        self.timer = (minutes, secondes)
        
        # recherche le temps écoulé et le modifie
        for child in self.children:
            if "Temps de jeu : " in child.text:
                child.text = 'Temps de jeu : {} min {} sec'.format(self.timer[0], self.timer[1])

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def StartGame(self):
        self.cols = 5
        self.timer = (0,0)
        self.page = 1
        self.tour = 1
        error = True
        while error:
            self.lastPage = []
            try:
                self.pageDepart = Proccessus.ChooseRandomPage(self)
                self.pageCible = Proccessus.ChooseRandomPage(self)
                self.pageActuelle = self.pageDepart

                self.lastPage.append(self.pageActuelle)

                self.Recharge()

                error = False
                Clock.schedule_once(self.Defeat, 605)
            except UnicodeEncodeError:
                print("Oups ! Il y a eu un problème dans le choix des pages ! Je ré-essaye...")
                error = True


    def Footer(self):
        # footer
        echap = Label(text='Cliquez sur "Echap" pour sortir du jeu...', italic=True)
        copyrightLabel = Label(text='Copyright © 2020 Lou BÉGÉ', italic=True)

        self.add_widget(echap)
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        self.add_widget(copyrightLabel)

    def Header(self):
        # le header
        # le nombre de tour
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='WikiGame', font_size='40sp', bold=True))
        self.add_widget(Label(text='-----------------------', bold=True))
        self.add_widget(Label(text='Tour n°{}'.format(self.tour), font_size='40sp', bold=True))
        self.add_widget(Label(text=''))

        # bouton recommencé
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        buttonRestart = Button(text='Recommencer')
        buttonRestart.bind(on_press=self.Restart)
        self.add_widget(buttonRestart)
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

        # temps écoulé
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        tempsDeJeu = Label(text='Temps de jeu : {} min {} sec'.format(self.timer[0], self.timer[1]), bold=True)
        self.add_widget(tempsDeJeu)
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

        # page de départ + page arrivé
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Départ : '+self.pageDepart[1], font_size='18sp', bold=True, underline=True))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Cible : '+self.pageCible[1], font_size='18sp', bold=True, underline=True))
        self.add_widget(Label(text=''))

        # page actuelle
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Actuelle : '+self.pageActuelle[1], font_size='18sp', bold=True, underline=True))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

    def Restart(self,instance):
        # relance le jeu
        self.StartGame()

    def ButtonList(self):
        self.myList = Proccessus.GetUrl(self, self.pageActuelle[0].replace(' ','_'))
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
                button = Button(text="0{} : {}".format(number,self.myList[target][1]))
            else:
                button = Button(text="{} : {}".format(number,self.myList[target][1]))

            button.bind(on_press=self.ButtonPress)
            self.add_widget(button)
        
        self.RetourChariot(20-maxi)
        self.ButtonsNavigation()

    def ButtonPress(self, instance):
        # si un des boutons correspondant aux urls est press
        choice = int(instance.text.split(':')[0])
        self.page = 1
        self.pageActuelle = self.myList[choice-1]
        self.lastPage.append(self.pageActuelle)
        # vérifie si on a gagné
        if self.pageActuelle[1] == self.pageCible[1]:
            self.Victory()
        else:
            self.tour += 1
            self.Recharge()
    
    
    def Victory(self):
        # supprime tout ce qu'il y a sur la page
        Widget.clear_widgets(self)
        self.cols = 1
        # affiche el nombre de tours en x minutes
        self.add_widget(Label(text='Victoire en {} tours et en {} min {} sec !'.format(self.tour, self.timer[0], self.timer[1]), font_size='60sp', bold=True))
        # affiche l'historique
        self.add_widget(Label(text='Historique : ', font_size='40sp', bold=True))
        for index in range(0,len(self.lastPage)):
            self.add_widget(Label(text='- Tour n°{} : {}'.format(index+1, self.lastPage[index][1]), font_size='20sp', bold=True))
        self.Footer()

    def RetourPress(self, instance):
        # prend la page précédente
        self.lastPage.pop()
        self.pageActuelle = self.lastPage[len(self.lastPage)-1]
        self.Recharge()

    def NavigationPress(self, instance):
        # si c'est la bouton précédent
        if "-1" in instance.text:
            self.page -= 1
            self.Recharge()
        # si c'est le bouton suivant
        elif "-2" in instance.text:
            self.page += +1
            self.Recharge()

    def Recharge(self):
        # Supprime tout ce qu'il y a sur la page
        # recharge la page Header + liste des boutons + footer
        Widget.clear_widgets(self)
        self.Header()
        self.ButtonList()
        self.Footer()

    def ButtonRetour(self):
        # vérifie si ce n'est pa le premier
        # -> ajoute un bouton retour qui déclenchera RetourPress
        if len(self.lastPage) != 1:
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
            buttonRetour = Button(text='00 : Retour')
            buttonRetour.bind(on_press=self.RetourPress)
            self.add_widget(buttonRetour)
            self.add_widget(Label(text=''))
            self.add_widget(Label(text=''))
    
    # permet de remplir une ligne
    def RetourChariot(self,number):
        if number != 0:
            for target_list in range(number%5):
                self.add_widget(Label(text=''))

    def ButtonsNavigation(self):
        # bouton lien précédent -> on click déclenche NavigationPress
        buttonPrecedent = Button(text='-1 : Liens précédents')
        buttonPrecedent.bind(on_press=self.NavigationPress)

        # bouton lien suivant -> on click déclenche NavigationPress
        buttonSuivant = Button(text='-2 : Liens suivants')
        buttonSuivant.bind(on_press=self.NavigationPress)

        # crée la ligne correspondante avec bouton précédent et suivant
        self.add_widget(Label(text=''))
        if self.page != 1:
            self.add_widget(buttonPrecedent)
        else:
            self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

        if len(self.myList) > (20*self.page):
            self.add_widget(buttonSuivant)
        else:
            self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))

class MyApp(App):

    def build(self):
        return MainScreen()

if __name__ == '__main__':
    Window.fullscreen = 'auto'
    MyApp().run()