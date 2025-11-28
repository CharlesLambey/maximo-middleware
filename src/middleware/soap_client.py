import os
import requests
from ..middleware.db import read_config_file

def get_endpoint_from_config():
    cfg = read_config_file()
    return cfg.get('MAXIMO_ENDPOINT', 'https://maximo.example.com/api/soap?wsdl')

def is_test_mode():
    cfg = read_config_file()
    return cfg.get('TEST_MODE', 'False').lower() in ('1','true','yes')

def post_xml(xml_string, action="CreateMXL_COMPANIES", timeout=30):
    """
    Envoie la requête SOAP. En mode test, retourne une réponse simulée.
    """
    if is_test_mode():
        # Simuler une réponse
        class FakeResponse:
            status_code = 200
            text = """<response><STATUT>OK</STATUT><MESSAGE>Simulated OK</MESSAGE><COMPANY>TEST</COMPANY></response>"""
        return FakeResponse()

    url = get_endpoint_from_config()
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': action
    }
    resp = requests.post(url, data=xml_string.encode('utf-8'), headers=headers, timeout=timeout)
    return resp
