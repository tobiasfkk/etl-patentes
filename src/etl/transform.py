from datetime import datetime

def transform_data(patent):
    # Transform data for dimension tables
    inventors = [{"inventor_name": inventor["inventorNameText"]} for inventor in patent["applicationMetaData"].get("inventorBag", [])]
    applicant = {"applicant_name": patent["applicationMetaData"].get("firstApplicantName") or "Unknown Applicant"}  # Fallback value
    cpc_classifications = [{"classification_code": code} for code in patent["applicationMetaData"].get("cpcClassificationBag", [])]
    examiner = {"examiner_name": patent["applicationMetaData"].get("examinerNameText") or "Unknown Examiner"}  # Fallback value
    business_entity_status = {"status_name": patent["applicationMetaData"]["entityStatusData"].get("businessEntityStatusCategory")}

    # Transform data for the fact table
    fact = {
        "application_number": patent.get("applicationNumberText"),
        "filing_date": datetime.strptime(patent["applicationMetaData"].get("filingDate"), "%Y-%m-%d") if patent["applicationMetaData"].get("filingDate") else None,
        "earliest_publication_date": datetime.strptime(patent["applicationMetaData"].get("earliestPublicationDate"), "%Y-%m-%d") if patent["applicationMetaData"].get("earliestPublicationDate") else None,
        "invention_title": patent["applicationMetaData"].get("inventionTitle"),
        "application_status": patent["applicationMetaData"].get("applicationStatusDescriptionText"),
        "customer_number": patent["applicationMetaData"].get("customerNumber"),
        "group_art_unit": patent["applicationMetaData"].get("groupArtUnitNumber"),
        "docket_number": patent["applicationMetaData"].get("docketNumber"),
    }

    return {
        "fact": fact,
        "inventors": inventors,
        "applicant": applicant,
        "cpc_classifications": cpc_classifications,
        "examiner": examiner,
        "business_entity_status": business_entity_status,
    }