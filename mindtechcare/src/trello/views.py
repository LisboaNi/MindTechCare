from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.http import JsonResponse
from .services import sync_trello_cards_for_employee

from .models import BoardTrello, CardTrello
from .forms import BoardTrelloForm, CardTrelloForm
from employees.models import Employee

# CRUD para BoardTrello
class BoardTrelloCreateView(CreateView):
    model = BoardTrello
    form_class = BoardTrelloForm
    template_name = 'trello/board_trello_create.html'
    success_url = reverse_lazy('board-list')

    def form_valid(self, form):
        repo = form.save(commit=False) 
        employee_instance = Employee.objects.get(user=self.request.user)
        repo.employee = employee_instance
        repo.save()
        return super().form_valid(form)

class BoardTrelloListView(ListView):
    model = BoardTrello
    template_name = 'trello/board_trello_list.html'
    context_object_name = 'boards'

    def get_queryset(self):
        # Filtra os boards do funcionário logado
        return BoardTrello.objects.filter(employee__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca o employee logado para passar ao template
        context['employee'] = Employee.objects.get(user=self.request.user)
        return context
    
class BoardTrelloUpdateView(UpdateView):
    model = BoardTrello
    form_class = BoardTrelloForm
    template_name = 'trello/board_trello_update.html'
    success_url = reverse_lazy('board-list')

class BoardTrelloDeleteView(DeleteView):
    model = BoardTrello
    template_name = 'trello/board_trello_confirm_delete.html'
    success_url = reverse_lazy('board-list')

# CRUD para CardTrello
class CardTrelloCreateView(CreateView):
    model = CardTrello
    form_class = CardTrelloForm
    template_name = 'card_trello_create.html'
    success_url = reverse_lazy('card-list')

    def form_valid(self, form):
        repo = form.save(commit=False) 
        employee_instance = Employee.objects.get(user=self.request.user)
        repo.employee = employee_instance
        repo.save()
        return super().form_valid(form)

class CardTrelloListView(ListView):
    model = CardTrello
    template_name = 'card_trello_list.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return CardTrello.objects.filter(board__employee=self.request.user.employee)

class CardTrelloUpdateView(UpdateView):
    model = CardTrello
    form_class = CardTrelloForm
    template_name = 'card_trello_update.html'
    success_url = reverse_lazy('card-list')

class CardTrelloDeleteView(DeleteView):
    model = CardTrello
    template_name = 'card_trello_confirm_delete.html'
    success_url = reverse_lazy('card-list')

# Atualizar Cards do Trello
def atualizar_cards(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        sync_trello_cards_for_employee(employee)
        return JsonResponse({"mensagem": "Sincronização concluída com sucesso!"})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro durante a sincronização."}, status=500)
