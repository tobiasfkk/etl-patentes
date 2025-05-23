import xml.etree.ElementTree as ET
import psycopg2
import os

def extract_data_from_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        patents = []
        for patent in root.findall(".//us-patent-application"):
            bibliographic_data = patent.find(".//us-bibliographic-data-application")
            if bibliographic_data is None:
                continue

            title = bibliographic_data.findtext(".//invention-title", default="Unknown Title")
            application = bibliographic_data.find(".//application-reference/document-id")
            country = application.findtext("country", default="Unknown Country")
            doc_number = application.findtext("doc-number", default="Unknown Doc Number")
            application_date = application.findtext("date", default=None)

            inventor = bibliographic_data.find(".//us-parties/inventors/inventor/addressbook")
            first_name = inventor.findtext("first-name", default="Unknown")
            last_name = inventor.findtext("last-name", default="Unknown")

            # Extrair resumo
            abstract_elem = patent.find(".//abstract")
            abstract = " ".join(
                (p.text or "").strip() for p in abstract_elem.findall(".//p")
            ) if abstract_elem is not None else ""
            unique_words = " ".join(set(abstract.split()))

            # Extrair descrição
            description_elem = patent.find(".//description")
            description = " ".join(
                (p.text or "").strip() for p in description_elem.findall(".//p")
            ) if description_elem is not None else ""

            print(f"Extracted data: Title: {title}, Country: {country}, Doc Number: {doc_number}, Application Date: {application_date}, Inventor: {first_name} {last_name}, Abstract: {abstract}, Description: {description}")

            patents.append({
                "title": title,
                "country": country,
                "doc_number": doc_number,
                "application_date": application_date,
                "first_name": first_name,
                "last_name": last_name,
                "abstract": abstract,
                "unique_words": unique_words,
                "description": description
            })

        return patents
    except ET.ParseError as e:
        raise Exception(f"Error parsing XML file '{os.path.basename(file_path)}': {e}")
