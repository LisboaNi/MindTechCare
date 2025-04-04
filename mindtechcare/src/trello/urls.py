from django.urls import path
from .views import (
    BoardTrelloCreateView, BoardTrelloListView, BoardTrelloUpdateView, BoardTrelloDeleteView,
    CardTrelloCreateView, CardTrelloListView, CardTrelloUpdateView, CardTrelloDeleteView,
    AtividadeTrelloCreateView, AtividadeTrelloListView, AtividadeTrelloUpdateView, AtividadeTrelloDeleteView,
    AtualizarCardsTrelloView,
)

urlpatterns = [
    # BoardTrello
    path('board/create/', BoardTrelloCreateView.as_view(), name='board-create'),
    path('boards/', BoardTrelloListView.as_view(), name='board-list'),
    path('board/update/<pk>/', BoardTrelloUpdateView.as_view(), name='board-update'),
    path('board/delete/<pk>/', BoardTrelloDeleteView.as_view(), name='board-delete'),

    # CardTrello
    path('card/create/', CardTrelloCreateView.as_view(), name='card-create'),
    path('cards/', CardTrelloListView.as_view(), name='card-list'),
    path('card/update/<pk>/', CardTrelloUpdateView.as_view(), name='card-update'),
    path('card/delete/<pk>/', CardTrelloDeleteView.as_view(), name='card-delete'),

    # AtividadeTrello
    path('atividade/create/', AtividadeTrelloCreateView.as_view(), name='atividade-create'),
    path('atividades/', AtividadeTrelloListView.as_view(), name='atividade-list'),
    path('atividade/update/<pk>/', AtividadeTrelloUpdateView.as_view(), name='atividade-update'),
    path('atividade/delete/<pk>/', AtividadeTrelloDeleteView.as_view(), name='atividade-delete'),

    path('atualizar-cards-trello/<str:board_id>/', AtualizarCardsTrelloView.as_view(), name='atualizar-cards-trello'),

]
