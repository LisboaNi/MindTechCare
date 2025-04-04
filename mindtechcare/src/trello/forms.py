from django import forms
from .models import BoardTrello, CardTrello, AtividadeTrello

class BoardTrelloForm(forms.ModelForm):
    class Meta:
        model = BoardTrello
        fields = ['nome_board', 'trello_board_id']

class CardTrelloForm(forms.ModelForm):
    class Meta:
        model = CardTrello
        fields = ['employee', 'board', 'nome_card', 'data_criacao', 'trello_card_id']

class AtividadeTrelloForm(forms.ModelForm):
    class Meta:
        model = AtividadeTrello
        fields = ['employee', 'nome_card', 'data_atividade']
