function atualizarTodosCommits() {
  const btn = document.getElementById("btnAtualizar");
  const icon = document.getElementById("btnIcon");
  const progressBar = document.getElementById("progressBarGithub");
  const progressContainer = document.getElementById("progressContainerGithub");
  const mensagemFinal = document.getElementById("mensagemFinalGithub");
  const mascote = document.getElementById("mascote");

  // Reset inicial
  progressBar.style.width = "0%";
  progressBar.textContent = "0%";
  progressContainer.classList.remove("hidden");
  mensagemFinal.classList.add("hidden");
  mascote.classList.add("hidden");

  progressContainer.classList.add("block");

  btn.classList.add("pointer-events-none", "opacity-60");
  icon.classList.remove("fa-brands", "fa-github");
  icon.classList.add("fa-solid", "fa-spinner", "fa-spin");

  let progress = 0;
  const interval = setInterval(() => {
    if (progress < 90) {
      progress += 10;
      progressBar.style.width = progress + "%";
      progressBar.textContent = progress + "%";
    }
  }, 200);

  fetch("/github/update-all/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      clearInterval(interval);
      progress = 100;
      progressBar.style.width = "100%";
      progressBar.textContent = "100%";

      mensagemFinal.classList.remove("hidden");
      mascote.classList.remove("hidden");

      if (data.success) console.log(data.success);
      if (data.errors && data.errors.length > 0) console.warn("Erros:", data.errors);
    })
    .catch((error) => {
      clearInterval(interval);
      console.error("Erro:", error);
      alert("Erro ao atualizar os commits.");
    })
    .finally(() => {
      btn.classList.remove("pointer-events-none", "opacity-60");
      icon.classList.remove("fa-solid", "fa-spinner", "fa-spin");
      icon.classList.add("fa-brands", "fa-github");

      setTimeout(() => {
        progressContainer.classList.add("hidden");
        progressContainer.classList.remove("block");
        progressBar.style.width = "0%";
        progressBar.textContent = "0%";
      }, 2);

      setTimeout(() => {
        mensagemFinal.classList.add("hidden");
        mascote.classList.add("hidden");
      }, 2000);
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
