from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def main():
    file_path = "data/dados.json"
    raw_data = extract_data(file_path)
    transformed_data = [transform_data(patent) for patent in raw_data]
    load_data(transformed_data)

if __name__ == "__main__":
    main()