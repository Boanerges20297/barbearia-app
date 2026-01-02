async function carregarAgendamentos() {
    const resposta = await fetch("http://127.0.0.1:5001/agendamentos"); // Ajuste se sua rota for diferente
    const agendamentos = await resposta.json();
    const lista = document.getElementById("listaAgendamentos");
    lista.innerHTML = "";

    for (const ag of agendamentos) {
        const li = document.createElement("li");

        // Texto descritivo
        const texto = document.createTextNode(
            `${ag.data} às ${ag.horario} - Cliente: ${ag.cliente_nome || ag.id_cliente
            } `
        );

        // Botão de Editar
        const btnEditar = document.createElement("button");
        const btnExcluir = document.createElement('button');
        btnEditar.textContent = "Editar";
        btnEditar.style.marginLeft = "10px";
        btnExcluir.textContent = 'Excluir';
        btnExcluir.style.color = 'red';
        btnExcluir.style.marginLeft = '10px';
        btnEditar.onclick = () => abrirModal(ag);
        btnExcluir.onclick = () => dispararExclusao(ag.id);

        li.appendChild(texto);
        li.appendChild(btnEditar);
        li.appendChild(btnExcluir);
        lista.appendChild(li);
    }
}

// Abre o modal e preenche os dados atuais
function abrirModal(agendamento) {
    document.getElementById("edit-id").value = agendamento.id;
    document.getElementById("edit-data").value = agendamento.data;
    document.getElementById("edit-horario").value = agendamento.horario;
    document.getElementById("modalEdicao").style.display = "block";
}

function fecharModal() {
    document.getElementById("modalEdicao").style.display = "none";
}

// A Ponte com o Backend (PUT)
async function confirmarEdicao() {
    const id = document.getElementById("edit-id").value;
    const dados = {
        id_cliente: 1,
        data: document.getElementById("edit-data").value,
        horario: document.getElementById("edit-horario").value,
        // Mantemos valores padrão para os campos que não estamos editando visualmente ainda
        id_barbeiro: 1,
        id_servico: 1,
    };

    try {
        const response = await fetch(
            `http://127.0.0.1:5001/editar-agendamento/${id}`,
            {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dados),
            }
        );

        const result = await response.json();

        if (response.ok) {
            alert("Atualizado com sucesso!");
            fecharModal();
            carregarAgendamentos(); // Atualiza a lista no fundo
        } else {
            alert(
                "Erro: " + (result.erros || result.erro || "Falha desconhecida")
            );
        }
    } catch (e) {
        console.error(e);
        alert("Erro de conexão com o servidor.");
    }
}

// Fechar modal se clicar fora dele (UX Polida)
window.onclick = function (event) {
    const modal = document.getElementById("modalEdicao");
    if (event.target == modal) {
        fecharModal();
    }
};

async function fazerAgendamento() {
    // 1. Pegar os valores dos inputs do HTML
    const inputCliente = Math.random() + 1;
    const inputHorario = document.getElementById("horarioInput").value;
    const inputData = document.getElementById("dataInput").value; // Essa é a data do calendário

    // 2. Montar o pacote para enviar (mudamos o nome da variável para evitar conflito)
    const pacoteEnvio = {
        id_cliente: inputCliente,
        horario: inputHorario,
        data: inputData,
    };

    // 3. Enviar para o Back-end
    const response = await fetch("http://127.0.0.1:5001/agendar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(pacoteEnvio), // Usamos o novo nome aqui
    });

    const result = await response.json();
    const feedbackEl = document.getElementById("feedback");

    if (response.ok) {
        feedbackEl.textContent = "Sucesso: " + result.mensagem;
        feedbackEl.className = "success";
        carregarAgendamentos(); // Atualiza a lista na hora
    } else {
        feedbackEl.textContent = "Erro: " + result.erro;
        feedbackEl.className = "error";
    }
    // Limpa a mensagem depois de alguns segundos
    setTimeout(() => {
        feedbackEl.textContent = "";
        feedbackEl.className = "";
    }, 5000);

}

async function dispararExclusao(id) {
    if (!confirm("Deseja realmente cancelar o agendamento?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:5001/deletar-agendamento/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Barbeiro-ID': '1' // Simulando que o barbeiro logado é o ID 1
            }
        });
    } catch (error) {
        console.error("Erro na deleção:", error);
        alert("Erro de conexão com o servidor.");
    }
}

carregarAgendamentos();