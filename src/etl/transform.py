from collections import Counter
import re

def transform_data(patent):
    # Processar palavras do abstract
    abstract = patent["abstract"]
    words = re.findall(r"\b\w+\b", abstract.lower())  # Extrair palavras
    word_counts = Counter(words)  # Contar ocorrências

    # Dados transformados
    return {
        "fact": {
            "author_name": patent["author"],
            "invention_title": patent["title"],
            "publication_date": patent["publication_date"],
            "country": patent["country"],
            "category": patent["category"],
        },
        "words": word_counts
    }