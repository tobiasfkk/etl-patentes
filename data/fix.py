def fix_xml(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write("<root>\n")
        for line in infile:
            if line.strip().startswith("<?xml") or line.strip().startswith("<!DOCTYPE"):
                continue
            outfile.write(line)
        outfile.write("</root>\n")
    print(f"Arquivo corrigido salvo em: {output_path}")