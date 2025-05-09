CREATE TABLE dim_addresses (
    id SERIAL PRIMARY KEY,
    city_name TEXT,
    geographic_region_name TEXT,
    geographic_region_code TEXT,
    postal_code TEXT,
    name_line_one TEXT,
    name_line_two TEXT,
    address_line_one TEXT,
    country_id INTEGER, -- FK para dim_countries
    FOREIGN KEY (country_id) REFERENCES dim_countries (id)
);