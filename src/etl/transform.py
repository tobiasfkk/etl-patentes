from datetime import datetime

def transform_data(patent):
    # Transformar dados para tabelas de dimensão
    inventors = [{"inventor_name": inventor["inventorNameText"]} for inventor in patent["applicationMetaData"].get("inventorBag", [])]
    applicant = {"applicant_name": patent["applicationMetaData"].get("firstApplicantName")}
    cpc_classifications = [{"classification_code": code} for code in patent["applicationMetaData"].get("cpcClassificationBag", [])]
    examiner = {"examiner_name": patent["applicationMetaData"].get("examinerNameText")}
    business_entity_status = {"status_name": patent["applicationMetaData"]["entityStatusData"].get("businessEntityStatusCategory")}

    # Transformar dados para a tabela de fato
    fact = {
        "application_number": patent.get("applicationNumberText"),
        "filing_date": datetime.strptime(patent["applicationMetaData"].get("filingDate"), "%Y-%m-%d"),
        "earliest_publication_date": datetime.strptime(patent["applicationMetaData"].get("earliestPublicationDate"), "%Y-%m-%d"),
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