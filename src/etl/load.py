from src.utils.db_connection import get_db_connection
from collections import Counter

def load_data(transformed_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        print(f"Loading {len(transformed_data)} records into the database...")

        for data in transformed_data:
            print(f"\n--- Inserting data: {data['title']} ---")

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
                        patent_id, word_id, word_count, date_id, country_id, author_id
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (patent_id, word_id, count, date_id, country_id, author_id))

        connection.commit()
        cursor.close()
        connection.close()
        print("Data loaded successfully.")
    except Exception as e:
        print("Error during load_data:", e)
        raise
