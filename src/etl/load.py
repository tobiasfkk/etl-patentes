from src.utils.db_connection import get_db_connection

def insert_and_get_id(cursor, table, data, unique_field):
    cursor.execute(f"SELECT id FROM {table} WHERE {unique_field} = %s", (data[unique_field],))
    result = cursor.fetchone()
    if result:
        return result["id"]
    columns = ", ".join(data.keys())
    values = ", ".join([f"%({key})s" for key in data.keys()])
    query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
    cursor.execute(query, data)
    return cursor.fetchone()["id"]

def load_data(transformed_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    for data in transformed_data:
        # Inserir autor, país e categoria
        author_id = insert_and_get_id(cursor, "dim_authors", {"author_name": data["fact"]["author_name"]}, "author_name")
        country_id = insert_and_get_id(cursor, "dim_countries", {"country_name": data["fact"]["country"]}, "country_name")
        category_id = insert_and_get_id(cursor, "dim_categories", {"category_name": data["fact"]["category"]}, "category_name")

        # Inserir na tabela de patentes
        patent_data = {
            "invention_title": data["fact"]["invention_title"],
            "abstract_text": data["fact"]["abstract"],
        }
        patent_id = insert_and_get_id(cursor, "dim_patents", patent_data, "invention_title")

        # Inserir na tabela fato
        for word, count in data["words"].items():
            word_id = insert_and_get_id(cursor, "dim_words", {"word": word}, "word")
            fact_data = {
                "category_id": category_id,
                "patent_id": patent_id,
                "word_id": word_id,
                "word_count": count,
                "date_id": None,  # Ajustar para inserir a data corretamente
                "country_id": country_id,
                "author_id": author_id,
            }
            columns = ", ".join(fact_data.keys())
            values = ", ".join([f"%({key})s" for key in fact_data.keys()])
            query = f"INSERT INTO fact_patents ({columns}) VALUES ({values})"
            cursor.execute(query, fact_data)

    connection.commit()
    cursor.close()
    connection.close()