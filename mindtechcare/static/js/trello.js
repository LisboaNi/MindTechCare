function atualizarCards(employeeId) {
  const btn = document.getElementById("btnAtualizar");
  const icon = document.getElementById("btnIcon");
  const progressBar = document.getElementById("progressBar");
  const progressContainer = document.getElementById("progressContainer");
  const mensagemFinal = document.getElementById("mensagemFinal");
  const mascote = document.getElementById("mascote");

  // Reset inicial
  progressBar.style.width = "0%";
  progressBar.textContent = "0%";
  progressContainer.classList.remove("hidden");
  mensagemFinal.classList.add("hidden");
  mascote.classList.add("hidden");

  // Mostrar a barra
  progressContainer.classList.add("block");

  // Desativa o botão
  btn.classList.add("pointer-events-none", "opacity-60");
  icon.classList.remove("fa-rotate");
  icon.classList.add("fa-spinner", "fa-spin");

  let progress = 0;
  const interval = setInterval(() => {
    if (progress < 90) {
      progress += 10;
      progressBar.style.width = progress + "%";
      progressBar.textContent = progress + "%";
    }
  }, 200);

  fetch(`/board/sync-trello/${employeeId}/`)
    .then((response) => response.json())
    .then((data) => {
      clearInterval(interval);
      progress = 100;
      progressBar.style.width = "100%";
      progressBar.textContent = "100%";

      mensagemFinal.classList.remove("hidden");
      mascote.classList.remove("hidden");

      // Mostra a mensagem final
    })
    .catch((error) => {
      clearInterval(interval);
      console.error("Erro na requisição:", error);
      alert("Erro ao sincronizar os cards.");
    })
    .finally(() => {
      // Restaura botão
      btn.classList.remove("pointer-events-none", "opacity-60");
      icon.classList.remove("fa-spinner", "fa-spin");
      icon.classList.add("fa-rotate");

      // Esconde barra após 2s
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
