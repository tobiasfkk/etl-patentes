import xml.etree.ElementTree as ET
import re

def fix_xml(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove todas as declarações XML (não apenas a primeira)
    content = re.sub(r'<\?xml[^>]+\?>', '', content, flags=re.IGNORECASE)

    # Remove todas as declarações DOCTYPE
    content = re.sub(r'<!DOCTYPE[^>]*>', '', content, flags=re.IGNORECASE)

    # Remover espaços em branco no início e final
    content = content.strip()

    # Envolver o conteúdo em uma tag root
    wrapped_content = f"<root>{content}</root>"

    try:
        root = ET.fromstring(wrapped_content)
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"Arquivo corrigido salvo em: {output_path}")
    except ET.ParseError as e:
        print(f"Erro ao corrigir o XML: {e}")

