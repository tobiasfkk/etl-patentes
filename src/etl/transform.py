from collections import Counter
import re

def transform_data(patent):
    # Processar palavras do abstract
    abstract = patent["abstract"]
    words = re.findall(r"\b\w+\b", abstract.lower())  # Extrair palavras
    word_counts = Counter(words)  # Contar ocorrências

    # Processar data de publicação
    publication_date = patent["publication_date"]
    if publication_date:
        year, month, day = int(publication_date[:4]), int(publication_date[4:6]), int(publication_date[6:8])
    else:
        year, month, day = None, None, None

    # Dados transformados
    return {
        "fact": {
            "author_name": patent["author"],
            "invention_title": patent["title"],
            "publication_date": publication_date,
            "country": patent["country"],
            "category": patent["category"],
        },
        "words": word_counts,
        "date": {"year": year, "month": month, "day": day}
    }