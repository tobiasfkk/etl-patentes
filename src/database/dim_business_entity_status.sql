CREATE TABLE dim_business_entity_status (
    id SERIAL PRIMARY KEY,
    status_name TEXT NOT NULL -- Nome do status (ex: "Regular Undiscounted", "Small")
);