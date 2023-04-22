from dbcontroller import *

def check_login(username, password):
    if doc_login(username, password):
        return 2
    elif pat_login(username, password):
        return 1
    else:
        return 0


def create_account(username, password, role):
    if role == 'Doctor':
        insert_doc(username, password)
        return 2
    elif role == 'Patient':
        insert_pat(username, password)
        return 1
    else:
        return 0

