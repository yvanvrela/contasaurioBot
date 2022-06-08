import os
from bs4 import BeautifulSoup
# from msilib.schema import Error
import re
import requests
import zipfile
from dataBase.postgre_service import all_contribuyentes, put_contribuyente0

from export_files import delete_file

PATH = 'archives/rucs'
SET_URL = 'https://www.set.gov.py'
URL = 'https://www.set.gov.py/portal/PARAGUAY-SET/InformesPeriodicos?folder-id=repository:collaboration:/sites/PARAGUAY-SET/categories/SET/Informes%20Periodicos/listado-de-ruc-con-sus-equivalencias'

# Para soporte de SSL
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


def download_zips(url_list: list) -> zip:
    try:
        print('Descargando archivos...')
        for url in url_list:

            page = requests.get(url)

            patron = '/(\w*).zip'
            ruc = re.findall(patron, url)[0]

            filename = f'{PATH}/{ruc}.zip'

            with open(filename, 'wb') as output_file:
                output_file.write(page.content)

        print('Descarga completada')
    except:
        print('error')


def find_zip_url(url: str) -> list:

    page_ruc = requests.get(url)

    soup = BeautifulSoup(page_ruc.content, 'html.parser')

    links_ruc_page = soup.find_all('div', class_='heading')

    links_page_zip = [
        f'{SET_URL}{page.find("a").get("href")}' for page in links_ruc_page]

    list_url_zip = []

    for link in links_page_zip:

        page_download_zip = requests.get(link)
        soup = BeautifulSoup(page_download_zip.content, 'html.parser')

        url_zip = soup.find('a', class_='btn btn-primary').get('href')
        url_zip = f'{SET_URL}{url_zip}'

        list_url_zip.append(url_zip)

    return list_url_zip


def read_file(path: str) -> dict:

    contribuyentes = []
    with open(path, 'r', encoding='utf-8') as f:

        for line in f:

            if not line.strip():
                continue

            data = line.split('|')

            fullname = data[1]

            if ',' in fullname:

                # -> (lastname, name)
                list_fullname = fullname.split(',')

                # -> 'name, lastname'
                fullname = f'{list_fullname[1]}, {list_fullname[0]}'

            contribuyentes.append(
                {
                    'ci': data[0],
                    'fullname': fullname,
                    'dv': data[2],
                    'ruc': f'{data[0]}-{data[2]}',
                }
            )

    return contribuyentes


def scan_files(file_extension='.txt', end_ruc=None | str) -> list:
    path_rucs = PATH

    if end_ruc is not None:

        if end_ruc == '*':
            with os.scandir(path_rucs) as ficheros:
                files = [
                    f'{path_rucs}/{fichero.name}' for fichero in ficheros if fichero.is_file() and fichero.name.endswith(file_extension)]

            return files
        else:

            filename = f'{path_rucs}/ruc{end_ruc}.txt'

            return filename
    else:

        with os.scandir(path_rucs) as ficheros:
            files = [
                f'{path_rucs}/{fichero.name}' for fichero in ficheros if fichero.is_file() and fichero.name.endswith(file_extension)]

        return files


def unzipping_files() -> None:
    paths_zip = scan_files('.zip')
    for path in paths_zip:
        with zipfile.ZipFile(path, 'r') as zip_reference:
            zip_reference.extractall(PATH)

        delete_file(path)


def search_contribuyente(ruc: str) -> dict | None:
    """
    Retorna un diccionario con los datos, si encuentra el ruc en los archivos
    sino retorna un None.
    Tambien puede discriminar guiones (-)
    param: 12345-1 or 12345
    return: dict
    >>> search_contribuyente('12345')
        {
            'ci':'12345',
            'fullname':'Juan Perez',
            'ruc': '12345-1',
        }
    >>> search_contribuyente('12345')
        None
    """

    ruc_reference = ruc

    if '-' in ruc_reference:

        # 12345-6 -> 5
        end_ruc = re.findall('(\d-)', ruc_reference)[0]

        path_data = scan_files(end_ruc=end_ruc)

        data_contribuyentes = read_file(path_data)

        filtered_data = list(filter(
            lambda contribuyente: contribuyente['ruc'] == ruc_reference, data_contribuyentes))

        if filtered_data:
            contribuyente = dict(filtered_data[0])

            return contribuyente
        else:
            return None
    else:

        # 12345 -> 5
        end_ruc = re.findall('\d*(\d)', ruc_reference)[0]

        path_data = scan_files(end_ruc=end_ruc)

        data_contribuyentes = read_file(path_data)

        filtered_data = list(filter(
            lambda contribuyente: contribuyente['ci'] == ruc_reference, data_contribuyentes))

        if filtered_data:
            contribuyente = dict(filtered_data[0])

            return contribuyente
        else:
            return None


# urls_zip = find_zip_url(URL)
# download_zips(urls_zip)

# unzipping_files()

ruc = '1235450'

contribuyente = search_contribuyente(ruc)

if contribuyente is not None:

    print(contribuyente['fullname'])
