from app.database import engine

try:
    with engine.connect() as conexao:
        print("Conexão com o PostgreSQL realizada com sucesso!")

except Exception as erro:
    print("Erro ao conectar com o banco:")
    print(erro)