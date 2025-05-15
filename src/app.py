import os
from etl.extract import extract_data_from_xml
from etl.transform import transform_data
from etl.load import load_data
from src.utils.db_connection import get_db_connection

def main():
    try:
        print("Starting ETL process...")
        create_tables()
        file_path = "data/dados.xml"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")

        print("Extracting data...")
        raw_data = extract_data_from_xml(file_path)
        print(f"Extracted {len(raw_data)} records.")

        print("Transforming data...")
        transformed_data = [transform_data(patent) for patent in raw_data]
        print(f"Transformed {len(transformed_data)} records.")

        print("Loading data into the database...")
        load_data(transformed_data)
        print("ETL process completed successfully.")
    except Exception as e:
        print(f"Error during ETL process: {e}")

def create_tables():
    try:
        print("Initializing database schema...")
        with open("src/database/init_schema.sql", "r") as file:
            sql_commands = file.read().split(";")  # Split script into individual commands

        connection = get_db_connection()
        cursor = connection.cursor()

        for command in sql_commands:
            command = command.strip()  # Remove extra whitespace
            if command:  # Ignore empty commands
                try:
                    print(f"Executing SQL command: {command[:50]}...")  # Log command
                    cursor.execute(command)
                except Exception as e:
                    print(f"Error executing command: {command[:50]}... Error: {e}")

        connection.commit()
        cursor.close()
        connection.close()
        print("Database schema initialized successfully.")
    except Exception as e:
        print(f"Error initializing database schema: {e}")
        raise

if __name__ == "__main__":
    main()