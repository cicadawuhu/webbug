import os

def delete_old_file():
    files = os.listdir('price_now')
    for item in files:
        os.remove('price_now\\%s' % item)