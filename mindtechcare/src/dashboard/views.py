from django.views import View
from django.utils.timezone import now, timedelta
from django.shortcuts import render, get_object_or_404
from employees.models import Employee
from github.models import AtividadeGitHub
from trello.models import CardTrello
import json

class DashboardGeralView(View):
    def get(self, request):
        filtro_dias = int(request.GET.get("data", 7))
        tipo_atividade = request.GET.get("tipo", "todos")
        data_limite = now() - timedelta(days=filtro_dias)

        employees = Employee.objects.all()

        grafico_labels = []
        data_commits = []
        data_cards = []
        alert_labels = []
        alert_data = []

        for employee in employees:
            commits = AtividadeGitHub.objects.filter(employee=employee, data_commit__gte=data_limite)
            cards = CardTrello.objects.filter(employee=employee, data_criacao__gte=data_limite)

            # Filtro por tipo
            if tipo_atividade == "github":
                cards = []
            elif tipo_atividade == "trello":
                commits = []

            total_commits = commits.count()
            total_cards = cards.count()

            # --- ALERTAS ---
            alertas = []
            dias_ativos = commits.dates("data_commit", "day").distinct().count()

            if total_commits > 10 and total_cards > 5:
                alertas.append("🚨 Alta atividade detectada — risco de sobrecarga.")
            if dias_ativos > 6 and (total_commits / filtro_dias) > 8:
                alertas.append("⚠️ Risco de exaustão — considere uma pausa.")
            if (total_commits < (filtro_dias * 2)) and total_cards > 5:
                alertas.append("🧠 Mudança repentina de padrão — possível sinal de burnout.")

            # Dados para os gráficos
            grafico_labels.append(employee.name)
            data_commits.append(total_commits)
            data_cards.append(total_cards)
            alert_labels.append(employee.name)
            alert_data.append(len(alertas))  # total de alertas

            # Atributos extras pro template
            employee.total_commits = total_commits
            employee.total_cards = total_cards
            employee.alertas = alertas

        context = {
            'employees': employees,
            'grafico_labels': json.dumps(grafico_labels),
            'grafico_data': json.dumps(data_commits),
            'grafico_cards': json.dumps(data_cards),
            'grafico_alert_labels': json.dumps(alert_labels),
            'grafico_alert_data': json.dumps(alert_data),
        }

        return render(request, "dashboard/geral.html", context)

class DashboardFuncionarioView(View):
    def get(self, request, pk):
        filtro_dias = int(request.GET.get("data", 7))
        tipo_atividade = request.GET.get("tipo", "todos")
        data_limite = now() - timedelta(days=filtro_dias)

        employee = get_object_or_404(Employee, pk=pk)
        commits = AtividadeGitHub.objects.filter(employee=employee, data_commit__gte=data_limite)
        cards = CardTrello.objects.filter(employee=employee, data_criacao__gte=data_limite)

        if tipo_atividade == "github":
            cards = []
        elif tipo_atividade == "trello":
            commits = []

        total_commits = commits.count()
        total_cards = cards.count()
        dias_ativos = commits.dates("data_commit", "day").distinct().count()

        alertas = []
        cont_alertas = {
            "Sobrecarga": 0,
            "Exaustão": 0,
            "Burnout": 0
        }

        if total_commits > 10 and total_cards > 5:
            alertas.append("🚨 Alta atividade detectada — risco de sobrecarga.")
            cont_alertas["Sobrecarga"] += 1
        if dias_ativos > 6 and (total_commits / filtro_dias) > 8:
            alertas.append("⚠️ Risco de exaustão — considere uma pausa.")
            cont_alertas["Exaustão"] += 1
        if (total_commits < (filtro_dias * 2)) and total_cards > 5:
            alertas.append("🧠 Mudança repentina de padrão — possível sinal de burnout.")
            cont_alertas["Burnout"] += 1

        # Dados para o gráfico de alertas
        grafico_alert_labels = list(cont_alertas.keys())
        grafico_alert_data = list(cont_alertas.values())

        employee.total_commits = total_commits
        employee.total_cards = total_cards
        employee.alertas = alertas

        context = {
            "employee": employee,
            "grafico_alert_labels": json.dumps(grafico_alert_labels),
            "grafico_alert_data": json.dumps(grafico_alert_data),
        }

        return render(request, "dashboard/funcionario.html", context)