from django import forms

class getPlayerInfo(forms.Form):
    player1 = forms.CharField(label='Player 1', max_length=100)
    player2 = forms.CharField(label='Player 2', max_length=100)
    player3 = forms.CharField(label='Player 3', max_length=100)
