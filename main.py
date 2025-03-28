import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard Energía Solar", layout="wide")

# Conectar a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="lala",
        database="energia_solar"
    )

# Cargar datos de la tabla de promedios de radiación solar
@st.cache_data
def cargar_promedio_radiacion():
    conn = conectar_db()
    query = "SELECT d.Nombre AS Departamento, p.Mes, AVG(p.Promedio_Radiacion) AS Radiacion_Promedio FROM Promedio_Radiacion_Solar p JOIN Municipios m ON p.Municipios_ID = m.ID JOIN Departamentos d ON m.Departamento_ID = d.ID GROUP BY d.Nombre, p.Mes;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Cargar datos de la tabla de consumo energético
@st.cache_data
def cargar_promedio_consumo():
    conn = conectar_db()
    query = "SELECT d.Nombre AS Departamento, p.Mes, AVG(p.Consumo_Total) AS Consumo_Promedio FROM Promedio_Consumo_Energetico_Residencial p JOIN Departamentos d ON p.Departamento_ID = d.ID GROUP BY d.Nombre, p.Mes;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Cargar datos
df_radiacion = cargar_promedio_radiacion()
df_consumo = cargar_promedio_consumo()

# 📊 Resumen General
st.title("🌞 Dashboard Energía Solar en Colombia")

col1, col2 = st.columns(2)
col1.metric("🌞 Promedio Radiación Solar", round(df_radiacion["Radiacion_Promedio"].mean(), 2))
col2.metric("⚡ Promedio Consumo Energético", round(df_consumo["Consumo_Promedio"].mean(), 2))

# 📌 Mapa de Radiación Solar
st.subheader("Mapa de Radiación Solar Promedio por Departamento")
fig_map = px.choropleth(df_radiacion, locations="Departamento", locationmode="country names",
                        color="Radiacion_Promedio", hover_name="Departamento",
                        title="Radiación Solar en Colombia")
st.plotly_chart(fig_map, use_container_width=True)

# 📌 Gráfico de consumo energético
st.subheader("Consumo Energético Promedio por Departamento")
fig_consumo = px.bar(df_consumo, x="Departamento", y="Consumo_Promedio", title="Consumo Energético")
st.plotly_chart(fig_consumo, use_container_width=True)
