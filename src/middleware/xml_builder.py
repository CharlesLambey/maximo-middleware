import xml.etree.ElementTree as ET
from datetime import datetime

NS_SOAP = "http://schemas.xmlsoap.org/soap/envelope/"
NS_MAX = "http://www.ibm.com/maximo"
ET.register_namespace('soapenv', NS_SOAP)
ET.register_namespace('max', NS_MAX)

def build_companies_envelope(record_dict):
    """
    record_dict: dict contenant les champs attendus (extracted from DB)
    Retourne une string XML prête à être postée.
    """
    envelope = ET.Element(f"{{{NS_SOAP}}}Envelope")
    header = ET.SubElement(envelope, f"{{{NS_SOAP}}}Header")
    body = ET.SubElement(envelope, f"{{{NS_SOAP}}}Body")
    create_companies = ET.SubElement(body, f"{{{NS_MAX}}}CreateMXL_COMPANIES")
    mxl_companies_set = ET.SubElement(create_companies, "max:MXL_COMPANIESSet")
    companies = ET.SubElement(mxl_companies_set, "COMPANIES")

    # Exemple d'attribution sécurisée : on vérifie les clés existantes
    def add(tag, key):
        el = ET.SubElement(companies, tag)
        el.text = str(record_dict.get(key, "")) if record_dict.get(key) is not None else ""

    # Champs (ajoute / adapte selon ton schéma)
    add("ADDRESS1", "address1")
    add("ADDRESS2", "address2")
    add("ADDRESS3", "address3")
    add("ADDRESS4", "address4")
    add("ADDRESS5", "address5")
    add("AUTOAPPROVEINV", "autoapproveinv")
    add("COMPANY", "company")
    add("NAME", "name")
    add("CHANGEDATE", "changedate")  # devrait être formaté en ISO

    # Contact example
    compcontact1 = ET.SubElement(companies, "COMPCONTACT")
    contact1 = ET.SubElement(compcontact1, "CONTACT")
    contact1.text = str(record_dict.get("contact1", ""))

    # Retourne la chaîne XML
    xml_string = ET.tostring(envelope, encoding="utf-8", method="xml")
    return xml_string.decode('utf-8')
