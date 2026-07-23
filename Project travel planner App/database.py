"""
Módulo de acesso à base de dados (SQLite).

Substitui o antigo Ficheiros2.py (que guardava tudo num ficheiro JSON).
Usa sqlite3, que já vem incluído no Python, sem instalações extra.
"""

import sqlite3
import os
import json

# Caminho absoluto -> o ficheiro da BD é sempre criado ao lado deste script,
# independentemente da pasta a partir da qual o programa é executado.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "viagens.db")


def conectar():
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    """Cria as tabelas da aplicação, caso ainda não existam."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sugestoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destino TEXT NOT NULL,
            reserva TEXT NOT NULL,
            orcamento TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viagens_marcadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilizador_id INTEGER NOT NULL,
            sugestao_id INTEGER,
            destino_procurado TEXT,
            FOREIGN KEY (utilizador_id) REFERENCES utilizadores (id),
            FOREIGN KEY (sugestao_id) REFERENCES sugestoes (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilizador_id INTEGER NOT NULL,
            sugestao_id INTEGER NOT NULL,
            data_reserva TEXT NOT NULL,
            FOREIGN KEY (utilizador_id) REFERENCES utilizadores (id),
            FOREIGN KEY (sugestao_id) REFERENCES sugestoes (id)
        )
    """)

    conn.commit()
    conn.close()


# ---------- Utilizadores ----------

def guardar_utilizador(nome, idade, email):
    """Guarda um utilizador na BD e devolve o id gerado."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO utilizadores (nome, idade, email) VALUES (?, ?, ?)",
        (nome, idade, email),
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id


# ---------- Sugestões ----------

def guardar_sugestao(destino, reserva, orcamento):
    """Guarda uma nova sugestão de viagem (usado pelo administrador)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sugestoes (destino, reserva, orcamento) VALUES (?, ?, ?)",
        (destino, reserva, orcamento),
    )
    conn.commit()
    conn.close()


def carregar_sugestoes():
    """Devolve todas as sugestões guardadas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, destino, reserva, orcamento FROM sugestoes")
    linhas = cursor.fetchall()
    conn.close()
    return [
        {"id": l[0], "Destino": l[1], "Reserva": l[2], "Orçamento": l[3]}
        for l in linhas
    ]


def procurar_por_destino(destino):
    """
    Procura sugestões cujo destino contenha o texto pesquisado
    (pesquisa parcial, não é preciso escrever o nome todo/exato).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, destino, reserva, orcamento FROM sugestoes "
        "WHERE LOWER(destino) LIKE ?",
        (f"%{destino.lower()}%",),
    )
    linhas = cursor.fetchall()
    conn.close()
    return [
        {"id": l[0], "Destino": l[1], "Reserva": l[2], "Orçamento": l[3]}
        for l in linhas
    ]


# ---------- Viagens marcadas (liga utilizador -> pesquisa/sugestão) ----------

def registar_viagem_marcada(utilizador_id, sugestao_id, destino_procurado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO viagens_marcadas (utilizador_id, sugestao_id, destino_procurado) "
        "VALUES (?, ?, ?)",
        (utilizador_id, sugestao_id, destino_procurado),
    )
    conn.commit()
    conn.close()


# ---------- Reservas (o utilizador escolhe e reserva um quarto/opção) ----------

def criar_reserva(utilizador_id, sugestao_id):
    """Confirma a reserva de uma sugestão específica para um utilizador."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reservas (utilizador_id, sugestao_id, data_reserva) "
        "VALUES (?, ?, datetime('now', 'localtime'))",
        (utilizador_id, sugestao_id),
    )
    conn.commit()
    conn.close()


def utilizador_ja_reservou(utilizador_id, sugestao_id):
    """Verifica se este utilizador já reservou esta sugestão específica."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM reservas WHERE utilizador_id = ? AND sugestao_id = ?",
        (utilizador_id, sugestao_id),
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def carregar_reservas_utilizador(utilizador_id):
    """Devolve todas as reservas confirmadas de um utilizador."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.id, s.destino, s.reserva, s.orcamento, r.data_reserva
        FROM reservas r
        JOIN sugestoes s ON r.sugestao_id = s.id
        WHERE r.utilizador_id = ?
        ORDER BY r.data_reserva DESC
        """,
        (utilizador_id,),
    )
    linhas = cursor.fetchall()
    conn.close()
    return [
        {"id": l[0], "Destino": l[1], "Reserva": l[2], "Orçamento": l[3], "Data": l[4]}
        for l in linhas
    ]


def carregar_todas_reservas():
    """Devolve todas as reservas de todos os utilizadores (visão do administrador)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.id, u.nome, u.email, s.destino, s.reserva, s.orcamento, r.data_reserva
        FROM reservas r
        JOIN utilizadores u ON r.utilizador_id = u.id
        JOIN sugestoes s ON r.sugestao_id = s.id
        ORDER BY r.data_reserva DESC
        """
    )
    linhas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": l[0],
            "Nome": l[1],
            "Email": l[2],
            "Destino": l[3],
            "Reserva": l[4],
            "Orçamento": l[5],
            "Data": l[6],
        }
        for l in linhas
    ]


# ---------- Migração dos dados antigos (dados.json) ----------

def migrar_json_para_bd(caminho_json=None):
    """
    Se existir um dados.json antigo e a tabela de sugestões estiver vazia,
    migra o conteúdo para a base de dados. Corre em segurança: se o ficheiro
    não existir ou estiver corrompido, simplesmente não faz nada.
    """
    if caminho_json is None:
        caminho_json = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "dados.json"
        )

    if not os.path.exists(caminho_json):
        return 0

    if carregar_sugestoes():
        # já há dados na BD, não voltar a migrar
        return 0

    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, OSError):
        # ficheiro corrompido ou ilegível -> ignora em vez de rebentar
        return 0

    count = 0
    for d in dados:
        try:
            guardar_sugestao(d["Destino"], d["Reserva"], d["Orçamento"])
            count += 1
        except KeyError:
            continue

    return count
