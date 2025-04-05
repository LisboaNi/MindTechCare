function atualizarTodosCommits() {
    fetch("/api/employee/github/update-all/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) alert(data.success);
        if (data.errors && data.errors.length > 0) console.warn("Erros:", data.errors);
    })
    .catch(error => console.error("Erro:", error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
