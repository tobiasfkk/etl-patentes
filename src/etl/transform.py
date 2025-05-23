from datetime import datetime
import re

def transform_data(patent):
    try:
        # Transformar nome do autor
        author_name = f"{patent['first_name']} {patent['last_name']}".strip()

        # Transformar data de publicação
        application_date = patent['application_date']

        if application_date:
            date_obj = datetime.strptime(application_date, "%Y%m%d")
            day, month, year = date_obj.day, date_obj.month, date_obj.year
        else:
            day, month, year = None, None, None

        # Dividir resumo em palavras únicas
        # words = set(patent['abstract'].split())
        words = re.findall(r'\b\w+\b', patent['abstract'].lower())

        # Retornar dados transformados
        return {
            "doc_number": patent['doc_number'],
            "title": patent['title'],
            "country": patent['country'],
            "author_name": author_name,
            "date": {"day": day, "month": month, "year": year},
            "abstract": patent['abstract'],
            "abstract_words": words,
            "description": patent['description']
        }
    except Exception as e:
        raise Exception(f"Error transforming data: {e}")