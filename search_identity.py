# from msilib.schema import
import requests


def search_identity_number(identity_number: str) -> str:
    """
        Recibe un numero de documento,
        realiza la consulta a la página del mec,
        retorna el n° de cedula y el nombre.
    """
    try:
        link = f"https://www.mec.gov.py/cms_v4/denuncias/buscar_persona?documento={identity_number.strip()}"

        response = requests.get(link).json()

        if response is not None:

            data = {
                'fullname': f"{response['nombre_persona']}, {response['apellido_persona']}",
                'ci': response['id_persona']
            }

            return data
        else:
            return response
    except:
        print('error')

