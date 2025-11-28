from .db import connect, read_config_file
from .xml_builder import build_companies_envelope
from .soap_client import post_xml, is_test_mode
from .logger import log_response, log_journal
import sys

def fetch_records(cursor, database, dossier):
    # Exemple générique de lecture 
    query = f"SELECT TOP 10 * FROM [{database}].[{dossier}].[YBPS];"
    cursor.execute(query)
    return cursor.fetchall()

def record_to_dict(record):
    # Convertit un tuple pyodbc.Row en dict minimal (exemple)
    columns = [col[0] for col in record.cursor_description] if hasattr(record, 'cursor_description') else []
    # Ici on retourne un dict fictif pour la doc publique
    try:
        return {
            "address1": getattr(record, 'address1', '') if hasattr(record, 'address1') else record[0],
            "company": getattr(record, 'company', '') if hasattr(record, 'company') else record[13] if len(record) > 13 else ''
        }
    except Exception:
        return {}

def main():
    # Chargement config et connexion
    cfg = read_config_file()
    test = cfg.get('TEST_MODE', 'True').lower() in ('1','true','yes')

    try:
        conn = connect()
    except Exception as e:
        print("Impossible de se connecter (mode public/demo).", e)
        # En mode demo, on peut simuler des enregistrements
        conn = None

    if conn:
        cursor = conn.cursor()
        dossier = cfg.get('Dossier', 'DEMO_DOSSIER')
        database = cfg.get('Bd', 'DEMO_DB')
        rows = fetch_records(cursor, database, dossier)
    else:
        # Mode demo / test : on construit des enregistrements factices
        rows = [
            ('Adr1_demo','Adr2','','','','','','','','','','','','COMP001','CRY','CUR','','','','','','','','','','','','','','','','','','','','','Contact','Position'),
        ]

    for record in rows:
        rec = record_to_dict(record)
        xml_payload = build_companies_envelope(rec)
        resp = post_xml(xml_payload)
        response_text = resp.text if hasattr(resp, 'text') else str(resp)
        company = rec.get('company', 'UNKNOWN')
        log_response(company, response_text)
        # Extraire statut/message basique (démo)
        status = "OK" if "OK" in response_text else "ERROR"
        message = "Simulated" if test else response_text[:200]
        log_journal(company, status, message)
        # Optionnel: update DB (non activé dans cette version)

if __name__ == "__main__":
    main()
