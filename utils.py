import pandas as pd
from database import DatabaseManager

# Diccionario global para nombres de meses
MESES_NOMBRES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def obtener_departamentos():
    """Obtiene lista de departamentos desde la base de datos"""
    db = DatabaseManager()
    query = "SELECT ID, Nombre FROM Departamentos ORDER BY Nombre"
    try:
        result = pd.read_sql_query(query, db.connection)
        # Guardamos tanto nombres como IDs para referencia
        global departamentos
        departamentos = result.to_dict('records')
        return ["Todos"] + result['Nombre'].tolist()
    except Exception as e:
        print(f"Error obteniendo departamentos: {e}")
        return ["Todos"]
    finally:
        db.close()

def obtener_municipios(departamento_nombre="Todos"):
    """Obtiene municipios de un departamento"""
    db = DatabaseManager()
    
    if departamento_nombre == "Todos":
        query = "SELECT ID, Nombre FROM Municipios ORDER BY Nombre"
        params = None
    else:
        # Buscamos el ID del departamento
        depto_id = next((d['ID'] for d in departamentos if d['Nombre'] == departamento_nombre), None)
        if not depto_id:
            return ["Todos"]
        
        query = "SELECT ID, Nombre FROM Municipios WHERE Departamento_ID = %s ORDER BY Nombre"
        params = (depto_id,)
    
    try:
        result = pd.read_sql_query(query, db.connection, params=params)
        # Guardamos municipios para referencia
        global municipios
        municipios = result.to_dict('records')
        return ["Todos"] + result['Nombre'].tolist()
    except Exception as e:
        print(f"Error obteniendo municipios: {e}")
        return ["Todos"]
    finally:
        db.close()

def obtener_anios(tabla='Radiacion_Solar'):
    """Obtiene años disponibles en la base de datos"""
    db = DatabaseManager()
    query = f"""
    SELECT DISTINCT YEAR(Fecha) as anio 
    FROM {tabla}
    ORDER BY anio DESC
    """
    try:
        result = pd.read_sql_query(query, db.connection)
        return ["Todos"] + [str(int(row['anio'])) for row in result.to_dict('records')]
    except Exception as e:
        print(f"Error obteniendo años disponibles: {e}")
        return ["Todos"]
    finally:
        db.close()

def obtener_meses(tabla='Radiacion_Solar', anio=None):
    """Obtiene meses disponibles para un año específico"""
    if anio == "Todos" or not anio:
        return ["Todos"] + list(MESES_NOMBRES.values())
    
    db = DatabaseManager()
    query = f"""
    SELECT DISTINCT MONTH(Fecha) as mes 
    FROM {tabla}
    WHERE YEAR(Fecha) = %s
    ORDER BY mes
    """
    
    try:
        result = pd.read_sql_query(query, db.connection, params=(int(anio),))
        meses_numeros = [int(row['mes']) for row in result.to_dict('records')]
        return ["Todos"] + [MESES_NOMBRES[mes] for mes in meses_numeros]
    except Exception as e:
        print(f"Error obteniendo meses disponibles: {e}")
        return ["Todos"] + list(MESES_NOMBRES.values())
    finally:
        db.close()

def obtener_mensaje_fecha(fecha_actual):
    """Genera mensaje descriptivo de la fecha seleccionada"""
    if not fecha_actual or fecha_actual.get('año', -1) == -1:
        return "Todos los registros disponibles"
    
    msj_año = f"Año {fecha_actual['año']}" if fecha_actual.get('año', 0) != 0 else ""
    msj_mes = f", mes {fecha_actual['mes']}" if fecha_actual.get('mes', 0) != 0 else ""
    
    return f"Fecha seleccionada: {msj_año}{msj_mes}" if msj_año or msj_mes else "Todos los registros disponibles"

def actualizar_region_actual(departamento, municipio):
    """Obtiene el ID de la región seleccionada"""
    try:
        if municipio != "Todos":
            municipio_id = next((m['ID'] for m in municipios if m['Nombre'] == municipio), None)
            if municipio_id:
                return {"id": municipio_id, "nombre": municipio}
        
        if departamento != "Todos":
            departamento_id = next((d['ID'] for d in departamentos if d['Nombre'] == departamento), None)
            if departamento_id:
                return {"id": departamento_id, "nombre": departamento}
        
        return {"id": -1, "nombre": "Colombia"}
    except Exception as e:
        print(f"Error actualizando región: {e}")
        return {"id": -1, "nombre": "Colombia"}