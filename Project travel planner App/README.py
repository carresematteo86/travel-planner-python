#EXECUTAR O PROGRAMA COMO UTILIZADOR

1- Clicar em "Utilizador"
2- Inserir os dados "Nome, Idade e Email" e depois clicar em "Marcar viagem"
3- Inserir o Destino da viagem, e procurar

#EXECUTAR O PROGRAMA COMO ADMINISTRADOR

1- Inserir a Password (admin123)
2- Adicionar Sugestões
    a) Inserir os dados "Destino, Reserva e Preço" e depois clicar em "Salvar"
    Carregar Sugestões
    b) Mostra todas as sugestões guardadas pelo administrador


#COMPONENTES

main.py ->
    -função principal que inicia o tkinter
    -contém a classe AppTrivago que contém a interface do programa e as funcionalidades principais

utilizador.py ->
    -inclui a classe user para representar um utilizador do programa
    -atributos: nome, idade, email

planeador.py ->
    -contém a classe VIAGEMCRAZY para representar uma possível viagem
    -atributos: destino, reserva, orçamento

Ficheiros2.py ->
    -tem funções para alterar dados usando JSON
    -funções principais: salvar_dados, carregar_dados