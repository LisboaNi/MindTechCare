from django.urls import path
from .views import (
    BoardTrelloCreateView, BoardTrelloListView, BoardTrelloUpdateView, BoardTrelloDeleteView,
    # CardTrelloCreateView, CardTrelloListView, CardTrelloUpdateView, CardTrelloDeleteView,
)
from . import views


urlpatterns = [
    # BoardTrello
    path('create/', BoardTrelloCreateView.as_view(), name='board-create'),
    path('', BoardTrelloListView.as_view(), name='board-list'),
    path('update/<pk>/', BoardTrelloUpdateView.as_view(), name='board-update'),
    path('delete/<pk>/', BoardTrelloDeleteView.as_view(), name='board-delete'),

    # # CardTrello
    # path('card/create/', CardTrelloCreateView.as_view(), name='card-create'),
    # path('cards/', CardTrelloListView.as_view(), name='card-list'),
    # path('card/update/<pk>/', CardTrelloUpdateView.as_view(), name='card-update'),
    # path('card/delete/<pk>/', CardTrelloDeleteView.as_view(), name='card-delete'),

    path('sync-trello/<int:employee_id>/', views.atualizar_cards, name='atualizar-cards-trello'),

]
