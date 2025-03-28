# Configuración de la base de datos
DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': 'lala',
            'database': 'energia_solar'
         }

MESES_NOMBRES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
class DashboardConfig:
     
    def __init__(self):
        self.region_actual = {"id": -1, "nombre": "Colombia"}
        self.fecha_actual = {"año": -1, "mes": 0}
        self.vista_actual = None
        self._version = 0  # Añadimos un contador de versiones
         # Configuración de la base de datos
    
    def actualizar_region(self, region):
        self.region_actual = region
        self._incrementar_version()
    
    def actualizar_fecha(self, anio, mes):
        self.fecha_actual = {"año": anio, "mes": mes}
        self._incrementar_version()
    
    def actualizar_vista(self, vista):
        self.vista_actual = vista
        self._incrementar_version()
    
    def _incrementar_version(self):
        self._version += 1
    
    def obtener_version(self):
        return self._version

    def obtener_region(self):
        return self.region_actual

    def obtener_fecha(self):
        return self.fecha_actual
    
    def obtener_vista_actual(self):
        return self.vista_actual
