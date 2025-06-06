from src.utils.db_connection import get_db_connection
from collections import Counter
from datetime import datetime

def load_data(transformed_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        print(f"Loading {len(transformed_data)} records into the database...")

        for data in transformed_data:

            source_file = data['source_file']
            doc_number = data['doc_number']

            # Verifica se a patente com esse doc_number já foi inserida a partir desse mesmo arquivo
            cursor.execute("""
                           SELECT 1
                           FROM staging_patents
                           WHERE doc_number = %s
                             AND source_file = %s LIMIT 1;
                           """, (doc_number, source_file))

            if cursor.fetchone():
                print(f"Patente {doc_number} do arquivo {source_file} já existe na staging. Pulando...")
                continue  # pula para o próximo item

            print(f"\n--- Inserting data: {data['title']} ---")

            # Inserção na Staging Area
            cursor.execute("INSERT INTO staging_patents (doc_number, invention_title, country, application_date, author_name, abstract_text, abstract_words, description_text, category, source_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                           (
                               data['doc_number'],
                               data['title'],
                               data['country'],
                               f"{data['date']['year']}-{data['date']['month']:02d}-{data['date']['day']:02d}" if
                               data['date']['year'] else None,
                               data['author_name'],
                               data['abstract'],
                               data['abstract_words'],
                               data['description'],
                               data['category'],
                               data['source_file']
                           ))

            # Autor
            cursor.execute("SELECT id FROM dim_authors WHERE author_name = %s;", (data['author_name'],))
            res = cursor.fetchone()
            if res:
                author_id = res['id']
            else:
                cursor.execute("INSERT INTO dim_authors (author_name) VALUES (%s);", (data['author_name'],))
                cursor.execute("SELECT id FROM dim_authors WHERE author_name = %s;", (data['author_name'],))
                author_id = cursor.fetchone()['id']
            print(f"Author ID: {author_id}")

            # País
            cursor.execute("SELECT id FROM dim_countries WHERE country_name = %s;", (data['country'],))
            res = cursor.fetchone()
            if res:
                country_id = res['id']
            else:
                cursor.execute("INSERT INTO dim_countries (country_name) VALUES (%s);", (data['country'],))
                cursor.execute("SELECT id FROM dim_countries WHERE country_name = %s;", (data['country'],))
                country_id = cursor.fetchone()['id']
            print(f"Country ID: {country_id}")

            # Categoria
            cursor.execute("SELECT id FROM dim_categories WHERE category_name = %s;", (data['category'],))
            res = cursor.fetchone()
            if res:
                category_id = res['id']
            else:
                cursor.execute("INSERT INTO dim_categories (category_name) VALUES (%s);", (data['category'],))
                cursor.execute("SELECT id FROM dim_categories WHERE category_name = %s;", (data['category'],))
                category_id = cursor.fetchone()['id']
            print(f"Category ID: {category_id}")

            # Data
            day, month, year = data['date']['day'], data['date']['month'], data['date']['year']
            cursor.execute("SELECT id FROM dim_date WHERE day = %s AND month = %s AND year = %s;", (day, month, year))
            res = cursor.fetchone()
            if res:
                date_id = res['id']
            else:
                cursor.execute("INSERT INTO dim_date (day, month, year) VALUES (%s, %s, %s);", (day, month, year))
                cursor.execute("SELECT id FROM dim_date WHERE day = %s AND month = %s AND year = %s;", (day, month, year))
                date_id = cursor.fetchone()['id']
            print(f"Date ID: {date_id}")

            # Patente
            cursor.execute("SELECT id FROM dim_patents WHERE invention_title = %s;", (data['title'],))
            res = cursor.fetchone()
            if res:
                patent_id = res['id']
            else:
                cursor.execute(
                    "INSERT INTO dim_patents (invention_title, doc_number, abstract_text, description_text) VALUES (%s, %s, %s, %s);",
                    (data['title'], data['doc_number'], data['abstract'], data['description'])
                )
                cursor.execute("SELECT id FROM dim_patents WHERE invention_title = %s;", (data['title'],))
                patent_id = cursor.fetchone()['id']
            print(f"Patent ID: {patent_id}")

            # Contar quantas vezes cada palavra aparece no abstract
            word_counts = Counter(data['abstract_words'])

            word_ids = {}  # Mapeia a palavra para seu ID
            for word, count in word_counts.items():
                cursor.execute("SELECT id FROM dim_words WHERE word = %s;", (word,))
                res = cursor.fetchone()
                if res:
                    word_id = res['id']
                else:
                    cursor.execute("INSERT INTO dim_words (word) VALUES (%s);", (word,))
                    cursor.execute("SELECT id FROM dim_words WHERE word = %s;", (word,))
                    word_id = cursor.fetchone()['id']
                word_ids[word] = (word_id, count)
            print(f"Unique words in abstract: {len(word_ids)}")

            # Fato
            for word, (word_id, count) in word_ids.items():
                cursor.execute("""
                    INSERT INTO fact_patents (
                        patent_id, word_id, word_count, date_id, country_id, author_id, category_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (patent_id, word_id, count, date_id, country_id, author_id, category_id))

        connection.commit()
        cursor.close()
        connection.close()
        print("Data loaded successfully.")
    except Exception as e:
        print("Error during load_data:", e)
        raise
