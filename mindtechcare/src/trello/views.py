from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from .models import BoardTrello, CardTrello, AtividadeTrello
from .forms import BoardTrelloForm, CardTrelloForm, AtividadeTrelloForm
from employees.models import Employee
from .integrations import get_trello_cards
from django.http import JsonResponse


# CRUD para BoardTrello
class BoardTrelloCreateView(CreateView):
    model = BoardTrello
    form_class = BoardTrelloForm
    template_name = 'trello/board_trello_create.html'
    success_url = reverse_lazy('board-list')

class BoardTrelloListView(ListView):
    model = BoardTrello
    template_name = 'board_trello_list.html'
    context_object_name = 'boards'

class BoardTrelloUpdateView(UpdateView):
    model = BoardTrello
    form_class = BoardTrelloForm
    template_name = 'board_trello_update.html'
    success_url = reverse_lazy('board-list')

class BoardTrelloDeleteView(DeleteView):
    model = BoardTrello
    template_name = 'board_trello_confirm_delete.html'
    success_url = reverse_lazy('board-list')

# CRUD para CardTrello
class CardTrelloCreateView(CreateView):
    model = CardTrello
    form_class = CardTrelloForm
    template_name = 'card_trello_create.html'
    success_url = reverse_lazy('card-list')

class CardTrelloListView(ListView):
    model = CardTrello
    template_name = 'card_trello_list.html'
    context_object_name = 'cards'

class CardTrelloUpdateView(UpdateView):
    model = CardTrello
    form_class = CardTrelloForm
    template_name = 'card_trello_update.html'
    success_url = reverse_lazy('card-list')

class CardTrelloDeleteView(DeleteView):
    model = CardTrello
    template_name = 'card_trello_confirm_delete.html'
    success_url = reverse_lazy('card-list')

# CRUD para AtividadeTrello
class AtividadeTrelloCreateView(CreateView):
    model = AtividadeTrello
    form_class = AtividadeTrelloForm
    template_name = 'atividade_trello_create.html'
    success_url = reverse_lazy('atividade-list')

class AtividadeTrelloListView(ListView):
    model = AtividadeTrello
    template_name = 'atividade_trello_list.html'
    context_object_name = 'atividades'

class AtividadeTrelloUpdateView(UpdateView):
    model = AtividadeTrello
    form_class = AtividadeTrelloForm
    template_name = 'atividade_trello_update.html'
    success_url = reverse_lazy('atividade-list')

class AtividadeTrelloDeleteView(DeleteView):
    model = AtividadeTrello
    template_name = 'atividade_trello_confirm_delete.html'
    success_url = reverse_lazy('atividade-list')

class AtualizarCardsTrelloView(View):
    def get(self, request, board_id):
        try:
            board = BoardTrello.objects.get(trello_board_id=board_id)
        except BoardTrello.DoesNotExist:
            return JsonResponse({"error": "Board não encontrado."}, status=404)

        token = request.GET.get('token')  # Pegando o token via parâmetros de query
        api_key = request.GET.get('api_key')  # Pegando a chave da API via parâmetros de query

        if not token or not api_key:
            return JsonResponse({"error": "Token ou chave de API não fornecidos."}, status=400)

        cards = get_trello_cards(board_id, token, api_key)

        if "error" in cards:
            return JsonResponse(cards, status=400)

        for card in cards:
            # Criar ou atualizar o card no banco de dados
            if not CardTrello.objects.filter(trello_card_id=card["id"]).exists():
                employee = Employee.objects.get(id=card.get("employee_id"))  # Obtendo o employee, supondo que você tenha uma relação
                CardTrello.objects.create(
                    employee=employee,
                    board=board,
                    nome_card=card["name"],
                    data_criacao=card["dateLastActivity"],  # Supondo que "dateLastActivity" seja a data de criação
                    trello_card_id=card["id"]
                )

            # Criar atividades para os cards
            if card.get("activities"):  # Supondo que 'activities' seja um campo que tenha atividades associadas ao card
                for activity in card["activities"]:
                    if not AtividadeTrello.objects.filter(nome_card=card["name"], data_atividade=activity["date"]).exists():
                        AtividadeTrello.objects.create(
                            employee=employee,
                            nome_card=card["name"],
                            data_atividade=activity["date"]
                        )

        return JsonResponse({"message": "Cards e atividades atualizados com sucesso!"}, status=200)