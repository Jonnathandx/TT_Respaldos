#!/bin/python3.12

import os
import json
import sys

# Define la ruta al archivo de configuración JSON
CONFIG_FILE = '/home/administrador/scripts/config.json'

try:
    # Abre y lee el archivo JSON
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Extrae los datos de configuración del diccionario
    db_host = config.get('db_host')
    db_port = config.get('db_port')
    db_name = config.get('db_name')
    db_user = config.get('db_user')
    db_password = config.get('db_password')
    output_file = config.get('output_file')

    # Verifica que se hayan leído todos los datos necesarios
    if not all([db_host, db_port, db_name, db_user, db_password, output_file]):
        print(f"Error: Faltan parámetros de configuración en '{CONFIG_FILE}'.", file=sys.stderr)
        sys.exit(1) # Sale con código de error

    # Construye la cadena de conexión para pg_dump
    connection_string = f'"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"'

    # Construye el comando completo de pg_dump
    command = f'pg_dump -d {connection_string} -f {output_file}'

    # Ejecuta el comando en el sistema operativo
    result = os.system(command)

    # Verifica el código de salida del comando
    if result == 0:
        print("Copia de seguridad de la base de datos completada con éxito.")
    else:
        print(f"Error: pg_dump falló con código de salida {result}.", file=sys.stderr)
        sys.exit(result) # Sale con el código de error de pg_dump

except FileNotFoundError:
    print(f"Error: El archivo de configuración '{CONFIG_FILE}' no fue encontrado.", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: No se pudo decodificar el archivo JSON '{CONFIG_FILE}'. Verifica el formato.", file=sys.stderr)
    sys.exit(1)
except KeyError as e:
    print(f"Error: Falta la clave '{e}' en el archivo de configuración '{CONFIG_FILE}'.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}", file=sys.stderr)
    sys.exit(1)

# Si todo fue bien, sale con código de éxito (0)
sys.exit(0)
