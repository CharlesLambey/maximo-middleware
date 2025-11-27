import pyodbc
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.txt')

def read_config_file(path=CONFIG_PATH):
    """
    Lit le fichier config (clé=valeur) et renvoie un dict.
    """
    cfg = {}
    if not os.path.exists(path):
        return cfg
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                cfg[k.strip()] = v.strip().rstrip(';')
    return cfg

def build_connection_string(cfg):
    # Attend que cfg contienne DRIVER, SERVER, DATABASE, UID, PWD
    return ';'.join([
        f"DRIVER={cfg.get('DRIVER','')}",
        f"SERVER={cfg.get('SERVER','')}",
        f"DATABASE={cfg.get('DATABASE','')}",
        f"UID={cfg.get('UID','')}",
        f"PWD={cfg.get('PWD','')}",
        f"TrustServerCertificate={cfg.get('TrustServerCertificate','yes')}"
    ])

def connect():
    cfg = read_config_file()
    if not cfg:
        raise FileNotFoundError("Fichier de configuration introuvable : config/config.txt")
    conn_str = build_connection_string(cfg)
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        return conn
    except Exception as e:
        raise
