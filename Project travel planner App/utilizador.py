class User:
    """Representa um utilizador da aplicação."""

    def __init__(self, nome, idade, email):
        self.nome = nome
        self.idade = idade
        self.email = email

    def exibir(self):
        print(f"Nome: {self.nome}, Idade: {self.idade}, Email: {self.email}")

    def __repr__(self):
        return f"User(nome={self.nome!r}, idade={self.idade}, email={self.email!r})"
