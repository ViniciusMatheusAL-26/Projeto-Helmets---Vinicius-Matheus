import base64
import sqlite3
from flask import Flask, redirect, render_template, request, url_for

# Alterado para 'Helmets Race Store' conforme solicitado e corrigido o __name__
app = Flask("Helmets Race Store")


def conexao():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("admin/index.html")


# ================= CATEGORIAS =================


@app.route("/listar_categorias")
def listarCategoria():
    conn = conexao()
    categoria = conn.execute("select * from categoria").fetchall()
    conn.close()
    return render_template("admin/listar_categoria.html", categorias=categoria)


@app.route("/cadastrar_categorias", methods=["GET", "POST"])
def cadastrarCategoria():
    if request.method == "POST":
        nome_categoria = request.form.get("nome_categoria")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo")

        imagem = request.files.get("imagem")
        imagem_base64 = ""
        if imagem and imagem.filename != "":
            imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")

        if nome_categoria:
            conn = conexao()
            conn.execute(
                "INSERT INTO categoria (nome, descricao, ativo, imagem ) VALUES (?, ?, ?, ?)",
                (nome_categoria, descricao, ativo, imagem_base64),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("listarCategoria"))

    return render_template("admin/cadastrar_categoria.html")


@app.route("/editarcategoria/<int:id>", methods=["GET", "POST"])
def editarCategoria(id):
    conn = conexao()

    if request.method == "POST":
        nome_categoria = request.form.get("nome_categoria")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo")
        imagem = request.files.get("imagem")

        if nome_categoria:
            if imagem and imagem.filename != "":
                imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
                conn.execute(
                    "UPDATE categoria SET nome=?, descricao=?, ativo=?, imagem=? WHERE id=?",
                    (nome_categoria, descricao, ativo, imagem_base64, id),
                )
            else:
                conn.execute(
                    "UPDATE categoria SET nome=?, descricao=?, ativo=? WHERE id=?",
                    (nome_categoria, descricao, ativo, id),
                )
            conn.commit()
            conn.close()
            return redirect(url_for("listarCategoria"))

    categoria = conn.execute(
        "select * from categoria where id=?", (id,)
    ).fetchone()
    conn.close()
    return render_template("admin/editar_categoria.html", categoria=categoria)


@app.route("/excluir_categoria/<int:id>", methods=["GET", "POST"])
def excluirCategoria(id):
    conn = conexao()
    if request.method == "POST":
        conn.execute("DELETE FROM categoria WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("listarCategoria"))

    categoria = conn.execute(
        "SELECT * FROM categoria WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    return render_template("admin/excluir_categoria.html", categoria=categoria)


# ================= PRODUTOS =================


@app.route("/listar_produtos")
def listarProduto():
    conn = conexao()

    # Busca todas as categorias para renderizar os blocos separados na tela
    categorias = conn.execute("SELECT * FROM categoria").fetchall()

    # Busca os produtos trazendo também o nome da categoria relacionada via INNER JOIN
    produtos = conn.execute(
        """
        SELECT produto.*, categoria.nome AS nome_categoria 
        FROM produto 
        LEFT JOIN categoria ON produto.id_categoria = categoria.id
    """
    ).fetchall()

    conn.close()
    return render_template(
        "admin/listar_produto.html", produtos=produtos, categorias=categorias
    )


@app.route("/cadastrar_produto", methods=["GET", "POST"])
def cadastrarProduto():
    conn = conexao()

    if request.method == "POST":
        nome_produto = request.form.get("nome_produto")
        preco = request.form.get("preco")
        ativo = request.form.get("ativo")
        id_categoria = request.form.get("id_categoria")  # Nova captura

        imagem = request.files.get("imagem")
        imagem_base64 = ""
        if imagem and imagem.filename != "":
            imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")

        if nome_produto:
            conn.execute(
                "INSERT INTO produto (nome, preco, ativo, imagem, id_categoria ) VALUES (?, ?, ?, ?, ?)",
                (nome_produto, preco, ativo, imagem_base64, id_categoria),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("listarProduto"))

    # Carrega as categorias existentes para exibir no campo <select> do formulário
    categorias = conn.execute("SELECT * FROM categoria").fetchall()
    conn.close()
    return render_template(
        "admin/cadastrar_produto.html", categorias=categorias
    )


@app.route("/editarproduto/<int:id>", methods=["GET", "POST"])
def editarProduto(id):
    conn = conexao()

    if request.method == "POST":
        nome_produto = request.form.get("nome_produto")
        preco = request.form.get("preco")
        ativo = request.form.get("ativo")
        categoria_id = request.form.get("categoria_id")  # Nova captura
        imagem = request.files.get("imagem")

        if nome_produto:
            if imagem and imagem.filename != "":
                imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
                conn.execute(
                    "UPDATE produto SET nome=?, preco=?, ativo=?, imagem=?, id_categoria=? WHERE id=?",
                    (
                        nome_produto,
                        preco,
                        ativo,
                        imagem_base64,
                        categoria_id,
                        id,
                    ),
                )
            else:
                conn.execute(
                    "UPDATE produto SET nome=?, preco=?, ativo=?, id_categoria=? WHERE id=?",
                    (nome_produto, preco, ativo, categoria_id, id),
                )
            conn.commit()
            conn.close()
            return redirect(url_for("listarProduto"))

    produto = conn.execute("select * from produto where id=?", (id,)).fetchone()
    categorias = conn.execute("SELECT * FROM categoria").fetchall()
    conn.close()
    return render_template(
        "admin/editar_produto.html", produto=produto, categorias=categorias
    )


@app.route("/excluir_produto/<int:id>", methods=["GET", "POST"])
def excluirProduto(id):
    conn = conexao()
    if request.method == "POST":
        conn.execute("DELETE FROM produto WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("listarProduto"))

    produto = conn.execute("SELECT * FROM produto WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("admin/excluir_produto.html", produto=produto)


if __name__ == "__main__":
    app.run(debug=True, port=5005)