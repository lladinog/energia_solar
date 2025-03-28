import pandas as pd
import streamlit as st
import plotly.express as px

class VistaRadiacion:
    def __init__(self, config):
        self.config = config
        self.df = self._cargar_datos()

    def _cargar_datos(self):
        try:
            consumo_path = "csv\\Consumo_RESIDENCIAL.csv"
            radiacion_path = "csv\\Promedio_Radiacion_Solar.csv"

            df_consumo = pd.read_csv(consumo_path)
            df_radiacion = pd.read_csv(radiacion_path)
            df = df_consumo.merge(df_radiacion, on=["Municipios_ID", "Mes"], how="inner")
            return df
        except Exception as e:
            st.error(f"Error al cargar los datos: {str(e)}")
            return pd.DataFrame()

    def mostrar(self):
        if self.df.empty:
            st.warning("No hay datos disponibles para mostrar.")
            return

        st.title("🌞 Radiación Solar")

        # Selección de municipio
        municipios = self.df["Nombre"].unique()
        selected_municipio = st.selectbox("Seleccione un municipio", municipios)

        # Filtrado de datos
        df_municipio = self.df[self.df["Nombre"] == selected_municipio]

        # Gráfico de Barras: Radiación Solar Promedio
        fig1 = px.bar(
            df_municipio,
            x="Mes",
            y="Promedio_Radiacion",
            title=f"Radiación Solar Promedio en {selected_municipio}",
            color="Mes",
            labels={"Promedio_Radiacion": "Radiación Solar (kW/m²)"}
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Gráfico de Línea: Evolución de la Radiación Solar
        fig2 = px.line(
            df_municipio,
            x="Mes",
            y="Promedio_Radiacion",
            title=f"Evolución de la Radiación Solar en {selected_municipio}",
            markers=True,
            line_shape="spline"
        )
        st.plotly_chart(fig2, use_container_width=True)

class VistaConsumo:
    def __init__(self, config):
        self.config = config
        self.df = self._cargar_datos()

    def _cargar_datos(self):
        try:
            consumo_path = "csv\\Consumo_RESIDENCIAL.csv"

            df_consumo = pd.read_csv(consumo_path)
            df_consumo["Consumo_Total"] = pd.to_numeric(df_consumo["Consumo_Total"], errors="coerce")
            df_consumo = df_consumo.dropna(subset=["Consumo_Total"])
            return df_consumo
        except Exception as e:
            st.error(f"Error al cargar los datos: {str(e)}")
            return pd.DataFrame()

    def mostrar(self):
        if self.df.empty:
            st.warning("No hay datos disponibles para mostrar.")
            return

        st.title("⚡ Consumo Energético")

        # Selección de municipio
        municipios = self.df["Nombre"].unique()
        selected_municipio = st.selectbox("Seleccione un municipio", municipios)

        # Filtrado de datos
        df_municipio = self.df[self.df["Nombre"] == selected_municipio]

        # Gráfico de Barras: Comparación de Costos
        fig1 = px.bar(
            df_municipio,
            x="Mes",
            y=["Costo_Energia_Tradicional", "Costo_Energia_Solar"],
            title=f"Comparación de Costos en {selected_municipio}",
            barmode="group",
            labels={"value": "Costo (COP)", "variable": "Fuente de Energía"}
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Gráfico de Línea: Ahorro Energético
        fig2 = px.line(
            df_municipio,
            x="Mes",
            y="Ahorro_Energetico",
            title=f"Ahorro Energético en {selected_municipio}",
            markers=True,
            line_shape="spline"
        )
        st.plotly_chart(fig2, use_container_width=True)

# Cargar datos
@st.cache_data
def load_data():
    consumo_path = "csv\\Consumo_RESIDENCIAL.csv"
    radiacion_path = "csv\\Promedio_Radiacion_Solar.csv"


    try:
        df_consumo = pd.read_csv(consumo_path)
        df_radiacion = pd.read_csv(radiacion_path)
        st.success("Archivos cargados correctamente")
        st.write("Primeras filas de Consumo:")
        st.dataframe(df_consumo.head())
        st.write("Primeras filas de Radiación:")
        st.dataframe(df_radiacion.head())
    except Exception as e:
        st.error(f"Error al cargar los archivos: {e}")

load_data()