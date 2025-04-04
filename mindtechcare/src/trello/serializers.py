from rest_framework import serializers
from .models import BoardTrello, CardTrello, AtividadeTrello

class BoardTrelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardTrello
        fields = ['id', 'nome_board', 'trello_board_id']

class CardTrelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardTrello
        fields = ['id', 'nome_card', 'data_criacao', 'trello_card_id', 'board', 'employee']

class AtividadeTrelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeTrello
        fields = ['id', 'nome_card', 'data_atividade', 'employee']
