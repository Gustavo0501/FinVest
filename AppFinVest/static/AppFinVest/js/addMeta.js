// Seleciona o botão de adicionar meta
const botaoAdicionar = document.querySelector('.botao-adicionar');
console.log("Botão adicionar selecionado:", botaoAdicionar);

// Seleciona o formulário de adicionar meta
const formularioAdicionar = document.getElementById('form-adicionar-meta');
console.log("Formulário selecionado:", formularioAdicionar);

// Seleciona o botão de cancelar dentro do formulário
const botaoCancelar = document.querySelector('.botao-cancelar');
console.log("Botão cancelar selecionado:", botaoCancelar);

// Exibe o formulário ao clicar no botão de adicionar
botaoAdicionar.addEventListener('click', function () {
    console.log("Botão adicionar clicado!");
    formularioAdicionar.style.display = 'block';
});

// Oculta o formulário ao clicar no botão de cancelar
botaoCancelar.addEventListener('click', function () {
    console.log("Botão cancelar clicado!");
    formularioAdicionar.style.display = 'none';
});