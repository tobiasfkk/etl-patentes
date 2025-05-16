import xml.etree.ElementTree as ET
import os

def extract_data_from_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        patents = []
        for patent in root.findall(".//us-patent-application"):
            data = {
                "author": patent.findtext(".//applicant//name", default="Unknown Author"),
                "title": patent.findtext(".//invention-title", default="Unknown Title"),
                "abstract": patent.findtext(".//abstract", default=""),
                "publication_date": patent.findtext(".//publication-reference//date", default=None),
                "country": patent.findtext(".//residence//country", default="Unknown Country"),
                "category": patent.findtext(".//classification-national//main-classification", default="Unknown Category"),
            }
            patents.append(data)
        return patents
    except ET.ParseError as e:
        raise Exception(f"Error parsing XML file '{os.path.basename(file_path)}': {e}")