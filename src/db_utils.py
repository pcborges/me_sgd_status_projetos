def softDelete(engine, tableName):
    # Efetuar exclusão lógica dos projetos, alterando o status para 0
    with engine.connect() as conn:
        conn.execute(
            f"update bd_cgpe.{tableName} set in_carga = 0 where in_carga = 9")
        conn.close()
