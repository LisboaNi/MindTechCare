function atualizarCards(employeeId) {
    fetch(`/api/sync-trello/${employeeId}/`)
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            alert("Erro ao sincronizar os cards.");
        });
}
