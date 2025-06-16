#!/bin/env python3.12

import os
import json
import sys

# Define la ruta al archivo de configuración JSON
CONFIG_FILE = '/home/administrador/scripts/db_config.json'

try:
    # Abre y lee el archivo JSON
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    # Extrae los datos de configuración del diccionario
    db_host = config.get('db_host')
    db_name = config.get('db_name')
    db_user = config.get('db_user')
    db_password = config.get('db_password')
    
    # Construye la cadena de conexión para pg_dump
    connection_string = f'"host={db_host} user={db_user} dbname={db_name} -f /home/administrador/scripts/db_scada.sql"'
    
    # Se construye el comando de psql
    command = f'PGPASSWORD={db_password} psql -d {connection_string}'
    
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
