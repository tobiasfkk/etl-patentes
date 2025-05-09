CREATE TABLE dim_countries (
    id SERIAL PRIMARY KEY,
    country_code TEXT NOT NULL, -- Código do país (ex: "US")
    country_name TEXT NOT NULL -- Nome do país (ex: "United States")
);