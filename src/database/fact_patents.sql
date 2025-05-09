CREATE TABLE fact_patents (
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