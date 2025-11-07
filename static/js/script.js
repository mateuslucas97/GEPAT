function salvarPatrimonio() {
    const patrimonioId = document.getElementById('patrimonioId').value;
    const formData = {
        numero_patrimonio: document.getElementById('numeroPatrimonio').value,
        descricao: document.getElementById('descricao').value,
        status: document.getElementById('status').value,
        localizacao: document.getElementById('localizacao').value
    };

    const url = patrimonioId ? `/api/patrimonios/${patrimonioId}` : '/api/patrimonios';
    const method = patrimonioId ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Erro ao salvar patrimônio');
    });
}

function editarPatrimonio(id) {
    // Buscar dados do patrimônio (em uma implementação real, faria uma requisição AJAX)
    // Por simplicidade, vamos recarregar a página com parâmetros
    window.location.href = `/patrimonios/editar/${id}`;
}

function deletarPatrimonio(id) {
    if (confirm('Tem certeza que deseja excluir este patrimônio?')) {
        fetch(`/api/patrimonios/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao deletar patrimônio');
        });
    }
}

// Limpar formulário quando modal for fechado
document.getElementById('modalPatrimonio').addEventListener('hidden.bs.modal', function () {
    document.getElementById('formPatrimonio').reset();
    document.getElementById('patrimonioId').value = '';
    document.getElementById('modalTitle').textContent = 'Novo Patrimônio';
});