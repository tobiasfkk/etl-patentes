CREATE TABLE IF NOT EXISTS dim_countries (
    id SERIAL PRIMARY KEY,
    country_code TEXT NOT NULL, -- Código do país (ex: "US")
    country_name TEXT NOT NULL -- Nome do país (ex: "United States")
);

CREATE TABLE IF NOT EXISTS dim_business_entity_status (
    id SERIAL PRIMARY KEY,
    status_name TEXT NOT NULL -- Nome do status (ex: "Regular Undiscounted", "Small")
);

CREATE TABLE IF NOT EXISTS dim_inventors (
    id SERIAL PRIMARY KEY,
    inventor_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_applicants (
    id SERIAL PRIMARY KEY,
    applicant_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_cpc_classification (
    id SERIAL PRIMARY KEY,
    classification_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_examiners (
    id SERIAL PRIMARY KEY,
    examiner_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_addresses (
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

CREATE TABLE IF NOT EXISTS fact_patents (
    id SERIAL PRIMARY KEY,
    application_number TEXT NOT NULL,
    filing_date DATE NOT NULL,
    earliest_publication_date DATE,
    invention_title TEXT NOT NULL,
    application_status TEXT,
    customer_number INTEGER,
    group_art_unit TEXT,
    docket_number TEXT,
    inventor_id INTEGER,
    applicant_id INTEGER,
    examiner_id INTEGER,
    business_entity_status_id INTEGER,
    cpc_classification_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);