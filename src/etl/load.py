from utils.db_connection import get_db_connection

def insert_and_get_id(cursor, table, data, unique_field):
    # Verifica se o registro já existe
    cursor.execute(f"SELECT id FROM {table} WHERE {unique_field} = %s", (data[unique_field],))
    result = cursor.fetchone()
    if result:
        return result["id"]
    # Insere o registro e retorna o ID
    columns = ", ".join(data.keys())
    values = ", ".join([f"%({key})s" for key in data.keys()])
    query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
    cursor.execute(query, data)
    return cursor.fetchone()["id"]

def load_data(transformed_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    for data in transformed_data:
        # Inserir nas tabelas de dimensão
        inventor_ids = [insert_and_get_id(cursor, "dim_inventors", inventor, "inventor_name") for inventor in data["inventors"]]
        applicant_id = insert_and_get_id(cursor, "dim_applicants", data["applicant"], "applicant_name")
        cpc_classification_ids = [insert_and_get_id(cursor, "dim_cpc_classification", cpc, "classification_code") for cpc in data["cpc_classifications"]]
        examiner_id = insert_and_get_id(cursor, "dim_examiners", data["examiner"], "examiner_name")
        business_entity_status_id = insert_and_get_id(cursor, "dim_business_entity_status", data["business_entity_status"], "status_name")

        # Inserir na tabela de fato
        fact = data["fact"]
        fact["inventor_id"] = inventor_ids[0] if inventor_ids else None  # Relacionar o primeiro inventor
        fact["applicant_id"] = applicant_id
        fact["examiner_id"] = examiner_id
        fact["business_entity_status_id"] = business_entity_status_id
        fact["cpc_classification_id"] = cpc_classification_ids[0] if cpc_classification_ids else None  # Relacionar a primeira classificação CPC

        columns = ", ".join(fact.keys())
        values = ", ".join([f"%({key})s" for key in fact.keys()])
        query = f"INSERT INTO fact_patents ({columns}) VALUES ({values})"
        cursor.execute(query, fact)

    connection.commit()
    cursor.close()
    connection.close()