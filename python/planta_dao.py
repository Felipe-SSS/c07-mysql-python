# planta_dao.py
# EXERCÍCIO: complete cada função no espaço indicado (onde está o TODO).
# Use sempre parâmetros (%s) e feche a conexão no finally.

from mysql.connector import Error
from connection_dao import close_connection, get_connection


# Questão 1: inserir uma planta.
# Deve inserir na tabela planta e devolver o id gerado (cursor.lastrowid).
# Lembre-se do commit!
def inserir_planta(nome, especie, preco, estoque):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()
    sql = "INSERT INTO planta (nome, especie, preco, estoque) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql, (nome, especie, preco, estoque))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Erro ao inserir: {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)



# Questão 2: listar todas as plantas, ordenadas pelo id.
# Deve devolver a lista de tuplas (cursor.fetchall()).
def listar_plantas():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, especie, preco, estoque FROM planta ORDER BY id")
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao listar: {e}")
        return []
    finally:
        close_connection(conn, cursor)


# Questão 3: buscar as plantas de uma espécie.
# Deve devolver a lista de tuplas das plantas cuja espécie seja igual ao parâmetro.
def buscar_por_especie(especie):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    sql = "SELECT id, nome, especie, preco, estoque FROM planta WHERE especie = %s ORDER BY id"
    try:
        cursor.execute(sql, (especie,))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar por espécie: {e}")
        return []
    finally:
        close_connection(conn, cursor)


# Questão 4: atualizar o preço de uma planta pelo id.
# Deve devolver True se alguma linha foi alterada (cursor.rowcount > 0), senão False.
def atualizar_preco(id_planta, novo_preco):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE planta SET preco = %s WHERE id = %s"
    try:
        cursor.execute(sql, (novo_preco, id_planta))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)


# Questão 5: remover uma planta pelo id.
# Deve devolver True se alguma linha foi removida, senão False.
def remover_planta(id_planta):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM planta WHERE id = %s"
    try:
        cursor.execute(sql, (id_planta,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)


# Questão 6 (Desafio): valor total do estoque.
# Deve devolver a soma de preco * estoque de todas as plantas, como float.
# Dica: SELECT COALESCE(SUM(preco * estoque), 0) FROM planta
def valor_total_estoque():
    conn = get_connection()
    if conn is None:
        return 0.0
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COALESCE(SUM(preco * estoque), 0) FROM planta")
        return float(cursor.fetchone()[0])
    except Error:
        return 0.0
    finally:
        close_connection(conn, cursor)
