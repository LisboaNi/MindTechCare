from django.urls import path
from .views import (
    BoardTrelloCreateView, BoardTrelloListView, BoardTrelloUpdateView, BoardTrelloDeleteView,
    CardTrelloCreateView, CardTrelloListView, CardTrelloUpdateView, CardTrelloDeleteView,
    AtualizarCardsTrelloView,
)

urlpatterns = [
    # BoardTrello
    path('board/create/', BoardTrelloCreateView.as_view(), name='board-create'),
    path('boards/', BoardTrelloListView.as_view(), name='board-list'),
    path('board/update/<pk>/', BoardTrelloUpdateView.as_view(), name='board-update'),
    path('board/delete/<pk>/', BoardTrelloDeleteView.as_view(), name='board-delete'),

    # # CardTrello
    # path('card/create/', CardTrelloCreateView.as_view(), name='card-create'),
    # path('cards/', CardTrelloListView.as_view(), name='card-list'),
    # path('card/update/<pk>/', CardTrelloUpdateView.as_view(), name='card-update'),
    # path('card/delete/<pk>/', CardTrelloDeleteView.as_view(), name='card-delete'),

    path('boards/<str:board_id>/atualizar/', AtualizarCardsTrelloView.as_view(), name='atualizar-cards-trello'),

]
