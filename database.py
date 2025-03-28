import mysql.connector
import pandas as pd
from mysql.connector import Error
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = self._create_connection()
    
    def _create_connection(self):
        """Establece conexión con la base de datos MySQL"""
        try:
            return mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None
    
    def get_radiacion_municipio(self, municipio_id, mes, año):
        """Obtiene datos de radiación solar para un municipio"""
        query = """
        SELECT Fecha, Radiacion_solar 
        FROM Radiacion_Solar
        WHERE Municipios_ID = %s
        AND MONTH(Fecha) = %s
        AND YEAR(Fecha) = %s
        ORDER BY Fecha
        """
        try:
            return pd.read_sql_query(query, self.connection, 
                                   params=(municipio_id, mes, año))
        except Error as e:
            print(f"Error obteniendo radiación: {e}")
            return pd.DataFrame()
    
    def get_promedio_radiacion(self, municipio_id, mes):
        """Obtiene el promedio histórico de radiación"""
        query = """
        SELECT Promedio_Radiacion
        FROM Promedio_Radiacion_Solar
        WHERE Municipios_ID = %s AND Mes = %s
        """
        try:
            return pd.read_sql_query(query, self.connection,
                                   params=(municipio_id, mes)).iloc[0,0]
        except:
            return None
    
    def get_consumo_departamento(self, departamento_id, mes, año):
        """Obtiene datos de consumo para un departamento"""
        query = """
        SELECT Mes, Consumo_Total, Promedio_Consumo, Valor_Facturado
        FROM Promedio_Consumo_Energetico_Residencial
        WHERE Departamento_ID = %s
        AND MONTH(Mes) = %s
        AND YEAR(Mes) = %s
        """
        try:
            return pd.read_sql_query(query, self.connection,
                                   params=(departamento_id, mes, año))
        except Error as e:
            print(f"Error obteniendo consumo: {e}")
            return pd.DataFrame()
    
    def get_municipio_coords(self, municipio_id):
        """Obtiene coordenadas de un municipio"""
        query = """
        SELECT Nombre, Latitud, Longitud
        FROM Municipios
        WHERE ID = %s
        """
        try:
            return pd.read_sql_query(query, self.connection,
                                   params=(municipio_id,)).iloc[0]
        except:
            return None
    
    def close(self):
        """Cierra la conexión"""
        if self.connection:
            self.connection.close()

    def get_consumo_historico(self, departamento_id, meses_atras=5):
        """Obtiene datos históricos de consumo"""
        query = """
        SELECT 
            DATE_FORMAT(Mes, '%%Y-%%m') as Periodo,
            AVG(CAST(Consumo_Total AS DECIMAL)) as Consumo_Total,
            AVG(CAST(Promedio_Consumo AS DECIMAL)) as Promedio_Consumo
        FROM Promedio_Consumo_Energetico_Residencial
        WHERE Departamento_ID = %s
        AND Mes >= DATE_SUB(
            (SELECT MAX(Mes) FROM Promedio_Consumo_Energetico_Residencial WHERE Departamento_ID = %s), 
            INTERVAL %s MONTH
        )
        GROUP BY Periodo
        ORDER BY Periodo
        """
        try:
            return pd.read_sql_query(
                query, 
                self.connection,
                params=(departamento_id, departamento_id, meses_atras)
            )
        except Error as e:
            print(f"Error obteniendo histórico consumo: {e}")
            return pd.DataFrame()
        
    def get_region_coords(self, region_id, es_municipio=True):
        """Obtiene coordenadas de una región"""
        table = "Municipios" if es_municipio else "Departamentos"
        query = f"""
        SELECT Nombre, Latitud, Longitud 
        FROM {table}
        WHERE ID = %s
        """
        try:
            return pd.read_sql_query(query, self.connection, params=(region_id,)).iloc[0]
        except:
            return None
    
    def get_consumo_comparativo(self, departamento_id=None):
        """Obtiene datos comparativos de consumo"""
        if departamento_id is None:
            query = """
            SELECT d.Nombre as Departamento, 
                   AVG(CAST(p.Promedio_Consumo AS DECIMAL)) as Consumo_Promedio
            FROM Promedio_Consumo_Energetico_Residencial p
            JOIN Departamentos d ON p.Departamento_ID = d.ID
            GROUP BY d.Nombre
            ORDER BY Consumo_Promedio DESC
            LIMIT 10
            """
            params = None
        else:
            query = """
            SELECT YEAR(Mes) as Anio, 
                   AVG(CAST(Promedio_Consumo AS DECIMAL)) as Consumo_Promedio
            FROM Promedio_Consumo_Energetico_Residencial
            WHERE Departamento_ID = %s
            GROUP BY Anio
            ORDER BY Anio
            """
            params = (departamento_id,)
        
        try:
            return pd.read_sql_query(query, self.connection, params=params)
        except Exception as e:
            print(f"Error obteniendo comparativo consumo: {e}")
            return pd.DataFrame()
        
    def get_radiacion_data(self, municipio_id, año=None, mes=None):
        """Obtiene datos de radiación con nombres de columnas consistentes"""
        query = """
        SELECT 
            Fecha,
            Radiacion_solar as radiacion,
            /* otras columnas si las hay */
        FROM Radiacion_Solar
        WHERE Municipios_ID = %s
        """
        params = [municipio_id]
        
        if año is not None:
            query += " AND YEAR(Fecha) = %s"
            params.append(año)
            
            if mes is not None:
                query += " AND MONTH(Fecha) = %s"
                params.append(mes)
        
        query += " ORDER BY Fecha"
        
        try:
            return pd.read_sql_query(query, self.connection, params=params)
        except Exception as e:
            print(f"Error obteniendo datos de radiación: {e}")
            return pd.DataFrame(columns=['Fecha', 'radiacion'])  # Devuelve DF con columnas esperadas