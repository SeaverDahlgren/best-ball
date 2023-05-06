from django import forms

class getPlayerInfo(forms.Form):
    player1 = forms.CharField(label='Callaway', max_length=100)
    player2 = forms.CharField(label='Velocity', max_length=100)
    player3 = forms.CharField(label='Titleist', max_length=100)
