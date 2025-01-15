// Função genérica para criar gráficos
function criarGrafico(id, config) {
    const ctx = document.getElementById(id).getContext('2d');
    return new Chart(ctx, config);
}

// Gráfico: Patrimônio ao longo do tempo
const patrimonioCanvas = document.getElementById('grafico-patrimonio');
const patrimonioData = JSON.parse(patrimonioCanvas.dataset.patrimonio);
const meses = JSON.parse(patrimonioCanvas.dataset.meses);

criarGrafico('grafico-patrimonio', {
    type: 'line',
    data: {
        labels: meses,
        datasets: [{
            label: 'Patrimônio',
            data: patrimonioData,
            borderColor: '#1e5ab7',
            backgroundColor: 'rgba(30, 90, 183, 0.2)',
            pointRadius: 5,
            fill: true,
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Gráfico 2: Comparativo entre renda e dívidas
const rendaDividasCanvas = document.getElementById('grafico-renda-dividas');
const rendaData = JSON.parse(rendaDividasCanvas.dataset.renda);
const dividasData = JSON.parse(rendaDividasCanvas.dataset.dividas);

criarGrafico('grafico-renda-dividas', {
    type: 'bar',
    data: {
        labels: JSON.parse(rendaDividasCanvas.dataset.meses),
        datasets: [
            {
                label: 'Renda (R$)',
                data: rendaData,
                backgroundColor: 'rgba(50, 205, 50, 0.5)'
            },
            {
                label: 'Dívidas (R$)',
                data: dividasData,
                backgroundColor: 'rgba(255, 69, 0, 0.5)'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: true } }
    }
});

