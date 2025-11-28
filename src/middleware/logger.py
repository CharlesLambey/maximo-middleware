import os
from datetime import datetime

LOGDIR = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
os.makedirs(LOGDIR, exist_ok=True)

def write_log(filename, content):
    path = os.path.join(LOGDIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def log_response(company, response_text):
    now = datetime.now()
    fname = f"File_log_{now:%d_%m_%Y}.txt"
    content = f"---\n{company}\n{response_text}\n---\n"
    write_log(fname, content)

def log_journal(company, status, message):
    now = datetime.now()
    fname = f"Journale_synchrinisation_maximo_{now:%d_%m_%Y}.txt"
    entry = f"{company} --- {status} --- {message}"
    write_log(fname, entry)
