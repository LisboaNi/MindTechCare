from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class BuyAccessView(LoginRequiredMixin, View):
    template_name = "plan/buy_access.html"

    def get(self, request):
        # Defina seus planos de forma simples, sem usar um modelo no banco de dados
        planos = [
            {"nome": "Plano Essência", "preco": 0.00, "max_funcionarios": 5},
            {"nome": "Plano Crescimento", "preco": 80.00, "max_funcionarios": 7},
            {"nome": "Plano Vitalidade", "preco": 190.00, "max_funcionarios": 15},
            {"nome": "Plano Evolução", "preco": 350.00, "max_funcionarios": 30},
        ]
        return render(request, self.template_name, {"planos": planos})

    def post(self, request):
        plano_id = request.POST.get("plano_id")

        if plano_id:
            # Converte o plano_id para um dicionário de plano correspondente
            planos = [
                {"nome": "Plano Essência", "preco": 0.00, "max_funcionarios": 5},
                {"nome": "Plano Crescimento", "preco": 80.00, "max_funcionarios": 7},
                {"nome": "Plano Vitalidade", "preco": 190.00, "max_funcionarios": 15},
                {"nome": "Plano Evolução", "preco": 350.00, "max_funcionarios": 30},
            ]
            plano = planos[int(plano_id)]  # Encontra o plano selecionado

            empresa = request.user.usermodel  # Conta da empresa logada
            empresa.max_funcionarios = plano[
                "max_funcionarios"
            ]  # Atualiza o número máximo de funcionários permitido
            empresa.save()

            # Redireciona para a lista de funcionários ou outra página de sua escolha
            return redirect("employee_list")

        return render(request, self.template_name, {"error": "Selecione um plano."})
