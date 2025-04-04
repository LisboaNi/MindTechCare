from django import forms
from .models import CardTrello, BoardTrello

class BoardTrelloForm(forms.ModelForm):
    class Meta:
        model = BoardTrello
        fields = ['nome_board', 'trello_board_id', 'trello_token']

class CardTrelloForm(forms.ModelForm):
    class Meta:
        model = CardTrello
        fields = ['board', 'nome_card', 'data_criacao', 'trello_card_id']
