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
        modo_alerta = request.GET.get("modo_alerta", "producao")
        data_limite = now() - timedelta(days=filtro_dias)

        employees = Employee.objects.all()

        grafico_labels = []
        data_commits = []
        data_cards = []
        alert_labels = []
        alert_data = []

        # Contagem dos tipos de alertas
        alerta_sobrecarga = 0
        alerta_exaustao = 0
        alerta_burnout = 0

        for employee in employees:
            commits = AtividadeGitHub.objects.filter(
                employee=employee, data_commit__gte=data_limite
            )
            cards = CardTrello.objects.filter(
                employee=employee, data_criacao__gte=data_limite
            )

            if tipo_atividade == "github":
                cards = CardTrello.objects.none()
            elif tipo_atividade == "trello":
                commits = AtividadeGitHub.objects.none()

            total_commits = commits.count()
            total_cards = cards.count()
            dias_ativos = commits.dates("data_commit", "day").distinct().count()

            alertas = []

            # === ALERTAS - PRODUÇÃO ===
            # # 🚨 Sobrecarga: muitos commits e muitos cards em poucos dias
            # # Condição: mais de 10 commits E mais de 5 cards no período analisado
            # if total_commits > 10 and total_cards > 5:
            #     alertas.append("🚨 Alta atividade detectada — risco de sobrecarga.")
            #     alerta_sobrecarga += 1

            # # ⚠️ Exaustão: frequência alta de commits ao longo de vários dias
            # # Condição: mais de 6 dias ativos E média de commits por dia acima de 8
            # if dias_ativos > 6 and (total_commits / filtro_dias) > 8:
            #     alertas.append("⚠️ Risco de exaustão — considere uma pausa.")
            #     alerta_exaustao += 1

            # # 🧠 Burnout: mudança de padrão — poucos commits com muitos cards
            # # Condição: commits abaixo do esperado, mas cards acima de 5
            # if total_commits < (filtro_dias * 2) and total_cards > 5:
            #     alertas.append("🧠 Mudança repentina de padrão — possível sinal de burnout.")
            #     alerta_burnout += 1

            # ALERTAS - TESTE
            if total_commits >= 10:
                alertas.append(
                    "🚨 (Teste) Alta atividade detectada — risco de sobrecarga."
                )
                alerta_sobrecarga += 1
            if total_commits >= 15:
                alertas.append("⚠️ (Teste) Risco de exaustão — considere uma pausa.")
                alerta_exaustao += 1
            if total_commits >= 17 and total_cards == 0:
                alertas.append(
                    "🧠 (Teste) Mudança repentina de padrão — possível sinal de burnout."
                )
                alerta_burnout += 1

            grafico_labels.append(employee.name)
            data_commits.append(total_commits)
            data_cards.append(total_cards)
            alert_labels.append(employee.name)
            alert_data.append(len(alertas))

            # Atualiza os campos do funcionário
            employee.total_commits = total_commits
            employee.total_cards = total_cards
            employee.alertas = alertas

        # Dados para gráficos gerais
        total_commits_geral = sum(
            data_commits
        )  # Total de commits de todos os funcionários
        total_cards_geral = sum(data_cards)  # Total de cards de todos os funcionários

        # Dados para gráfico de alertas por tipo
        alertas_tipo_labels = ["Sobrecarga", "Exaustão", "Burnout"]
        alertas_tipo_data = [alerta_sobrecarga, alerta_exaustao, alerta_burnout]

        context = {
            "employees": employees,
            "grafico_labels": json.dumps(grafico_labels),
            "grafico_data": json.dumps(data_commits),
            "grafico_cards": json.dumps(data_cards),
            "grafico_alert_labels": json.dumps(alert_labels),
            "grafico_alert_data": json.dumps(alert_data),
            "total_commits_geral": total_commits_geral,  # Total de commits
            "total_cards_geral": total_cards_geral,  # Total de cards
            "alertas_tipo_labels": json.dumps(
                alertas_tipo_labels
            ),  # Labels dos tipos de alertas
            "alertas_tipo_data": json.dumps(
                alertas_tipo_data
            ),  # Dados dos tipos de alertas
        }

        return render(request, "dashboard/geral.html", context)


class DashboardFuncionarioView(View):
    def get(self, request, pk):
        filtro_dias = int(request.GET.get("data", 7))
        tipo_atividade = request.GET.get("tipo", "todos")
        modo_alerta = request.GET.get("modo_alerta", "producao")
        data_limite = now() - timedelta(days=filtro_dias)

        employee = get_object_or_404(Employee, pk=pk)

        # Obtendo os commits por dia
        commits_por_dia = []
        dias_commits = []
        for i in range(filtro_dias):
            dia = data_limite + timedelta(days=i)
            count_commits = AtividadeGitHub.objects.filter(
                employee=employee, data_commit__date=dia.date()
            ).count()
            commits_por_dia.append(count_commits)
            dias_commits.append(dia.strftime("%Y-%m-%d"))

        # Obtendo os cards por dia
        cards_por_dia = []
        dias_cards = []
        for i in range(filtro_dias):
            dia = data_limite + timedelta(days=i)
            count_cards = CardTrello.objects.filter(
                employee=employee, data_criacao__date=dia.date()
            ).count()
            cards_por_dia.append(count_cards)
            dias_cards.append(dia.strftime("%Y-%m-%d"))

        # Filtra commits e cards conforme o tipo de atividade
        if tipo_atividade == "github":
            cards_por_dia = [0] * filtro_dias
        elif tipo_atividade == "trello":
            commits_por_dia = [0] * filtro_dias

        total_commits = sum(commits_por_dia)
        total_cards = sum(cards_por_dia)
        dias_ativos = len([commit for commit in commits_por_dia if commit > 0])

        alertas = []
        cont_alertas = {"Sobrecarga": 0, "Exaustão": 0, "Burnout": 0}

        # ALERTAS - PRODUÇÃO
        # # Sobrecarga: Um alto número de commits (por exemplo, mais de 10) pode ser um indicativo de que o colaborador está
        # # trabalhando em excesso. Normalmente, a sobrecarga ocorre quando a pessoa se dedica intensamente,
        # # realizando muitas tarefas, como commits, sem dar tempo para pausas adequadas.
        # if total_commits >= 10:
        #     alertas.append("🚨 Alta atividade detectada — risco de sobrecarga.")
        #     cont_alertas["Sobrecarga"] += 1

        # # Exaustão: Quando a quantidade de commits começa a se acumular em um nível alto (15 ou mais commits),
        # # pode ser um sinal de exaustão. O número de commits por dia pode ser um indicador de que o colaborador está
        # # trabalhando de forma insustentável por um período longo, o que pode levar à exaustão.
        # if total_commits >= 15:
        #     alertas.append("⚠️ Risco de exaustão — considere uma pausa.")
        #     cont_alertas["Exaustão"] += 1

        # # Burnout: O burnout é um estado de esgotamento extremo. Isso pode ser detectado por uma combinação de muitos commits
        # # (mais de 17, por exemplo) sem a criação de cards no Trello. A falta de diversificação de atividades, como a ausência de
        # # novos cards enquanto os commits continuam a ser feitos, pode indicar que a pessoa está apenas focada em atividades
        # # repetitivas e cansativas, sem pausas ou mudança de tarefas, o que é um sinal claro de burnout.
        # if total_commits >= 17 and total_cards == 0:
        #     alertas.append("🧠 Mudança repentina de padrão — possível sinal de burnout.")
        #     cont_alertas["Burnout"] += 1

        # ALERTAS - TESTE
        if total_commits >= 10:
            alertas.append("🚨 (Teste) Alta atividade detectada — risco de sobrecarga.")
            cont_alertas["Sobrecarga"] += 1
        if total_commits >= 15:
            alertas.append("⚠️ (Teste) Risco de exaustão — considere uma pausa.")
            cont_alertas["Exaustão"] += 1
        if total_commits >= 17 and total_cards == 0:
            alertas.append(
                "🧠 (Teste) Mudança repentina de padrão — possível sinal de burnout."
            )
            cont_alertas["Burnout"] += 1

        grafico_alert_labels = list(cont_alertas.keys())
        grafico_alert_data = list(cont_alertas.values())

        employee.total_commits = total_commits
        employee.total_cards = total_cards
        employee.alertas = alertas

        context = {
            "employee": employee,
            "alertas": alertas,
            "grafico_alert_labels": json.dumps(grafico_alert_labels),
            "grafico_alert_data": json.dumps(grafico_alert_data),
            "total_commits": total_commits,
            "total_cards": total_cards,
            "dias_commits": json.dumps(dias_commits),
            "commits_data": json.dumps(commits_por_dia),
            "dias_cards": json.dumps(dias_cards),
            "cards_data": json.dumps(cards_por_dia),
        }

        return render(request, "dashboard/funcionario.html", context)
