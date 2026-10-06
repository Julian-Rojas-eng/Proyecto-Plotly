import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Visualizador Interactivo con Plotly",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Visualizador Interactivo con Plotly")

st.write(
    """
    Aplicación demostrativa desarrollada en Python para explorar
    algunas de las posibilidades de visualización interactiva de Plotly.
    """
)

# Datos de ejemplo incluidos con Plotly
df = px.data.iris()

# --------------------------------------------------
# MENÚ PRINCIPAL
# --------------------------------------------------

st.sidebar.title("🎛️ Panel de control")

seccion = st.sidebar.radio(
    "Selecciona una demostración:",
    [
        "📊 Exploración de datos",
        "📐 Funciones matemáticas",
        "📈 Análisis estadístico"
    ]
)

st.sidebar.divider()

# ==================================================
# 1. EXPLORACIÓN DE DATOS
# ==================================================

if seccion == "📊 Exploración de datos":

    st.header("📊 Exploración de datos")

    st.write(
        """
        Esta sección utiliza **Plotly Express** para explorar
        interactivamente el conjunto de datos Iris.
        """
    )

    tipo_grafico = st.sidebar.selectbox(
        "Tipo de gráfico:",
        [
            "Dispersión",
            "Histograma",
            "Box Plot",
            "Barras",
            "Dispersión 3D"
        ]
    )

    nombres = {
        "sepal_length": "Longitud del sépalo",
        "sepal_width": "Ancho del sépalo",
        "petal_length": "Longitud del pétalo",
        "petal_width": "Ancho del pétalo"
    }

    variables = list(nombres.keys())

    # -------------------------------
    # DISPERSIÓN
    # -------------------------------

    if tipo_grafico == "Dispersión":

        col1, col2 = st.columns(2)

        with col1:
            x = st.selectbox(
                "Variable X:",
                variables,
                format_func=lambda v: nombres[v],
                index=1
            )

        with col2:
            y = st.selectbox(
                "Variable Y:",
                variables,
                format_func=lambda v: nombres[v],
                index=0
            )

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color="species",
            title="Gráfico de dispersión",
            labels={
                x: nombres[x],
                y: nombres[y],
                "species": "Especie"
            },
            hover_data=["species"]
        )

    # -------------------------------
    # HISTOGRAMA
    # -------------------------------

    elif tipo_grafico == "Histograma":

        variable = st.selectbox(
            "Variable:",
            variables,
            format_func=lambda v: nombres[v]
        )

        fig = px.histogram(
            df,
            x=variable,
            color="species",
            title="Distribución de los datos",
            labels={
                variable: nombres[variable],
                "species": "Especie"
            }
        )

    # -------------------------------
    # BOX PLOT
    # -------------------------------

    elif tipo_grafico == "Box Plot":

        variable = st.selectbox(
            "Variable:",
            variables,
            format_func=lambda v: nombres[v]
        )

        fig = px.box(
            df,
            x="species",
            y=variable,
            color="species",
            title="Comparación entre especies",
            labels={
                variable: nombres[variable],
                "species": "Especie"
            }
        )

    # -------------------------------
    # BARRAS
    # -------------------------------

    elif tipo_grafico == "Barras":

        st.subheader("Comparación de promedios entre especies")

        nombres_variables = {
            "Longitud del sépalo": "sepal_length",
            "Ancho del sépalo": "sepal_width",
            "Longitud del pétalo": "petal_length",
            "Ancho del pétalo": "petal_width"
        }

        variable_nombre = st.selectbox(
            "Variable a comparar:",
            list(nombres_variables.keys()),
            key="variable_barras"
        )

        variable = nombres_variables[variable_nombre]

        # Pandas calcula el promedio de la variable para cada especie
        promedios = (
            df.groupby("species", as_index=False)[variable]
            .mean()
        )

        # Plotly crea el gráfico de barras
        fig = px.bar(
            promedios,
            x="species",
            y=variable,
            color="species",
            title=f"Promedio de {variable_nombre} por especie",
            labels={
                "species": "Especie",
                variable: f"Promedio de {variable_nombre}"
            }
        )
    # -------------------------------
    # DISPERSIÓN 3D
    # -------------------------------

    else:

        st.info(
            "Puedes arrastrar el gráfico con el mouse para rotarlo en tres dimensiones."
        )

        fig = px.scatter_3d(
            df,
            x="sepal_length",
            y="sepal_width",
            z="petal_length",
            color="species",
            title="Visualización tridimensional del conjunto Iris",
            labels={
                "sepal_length": "Longitud del sépalo",
                "sepal_width": "Ancho del sépalo",
                "petal_length": "Longitud del pétalo",
                "species": "Especie"
            }
        )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Observaciones", len(df))

    with col2:
        st.metric("Especies", df["species"].nunique())

    with col3:
        st.metric("Variables numéricas", 4)

# ==================================================
# 2. FUNCIONES MATEMÁTICAS
# ==================================================

elif seccion == "📐 Funciones matemáticas":

    st.header("📐 Funciones matemáticas")

    st.write(
        """
        En este ejemplo **NumPy realiza los cálculos matemáticos**
        y **Plotly Graph Objects representa el resultado
        de forma interactiva**.
        """
    )

    st.latex(
        r"y = A\sin(Bx)e^{-Cx}"
    )

    amplitud = st.sidebar.slider(
        "Amplitud (A)",
        min_value=0.5,
        max_value=5.0,
        value=2.0,
        step=0.1
    )

    frecuencia = st.sidebar.slider(
        "Frecuencia (B)",
        min_value=0.5,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    decaimiento = st.sidebar.slider(
        "Decaimiento (C)",
        min_value=0.0,
        max_value=0.5,
        value=0.10,
        step=0.01
    )

    x = np.linspace(0, 20, 500)

    y = (
        amplitud
        * np.sin(frecuencia * x)
        * np.exp(-decaimiento * x)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Función"
        )
    )

    fig.update_layout(
        title="Función matemática interactiva",
        xaxis_title="x",
        yaxis_title="y",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Parámetros actuales")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Amplitud A", f"{amplitud:.1f}")

    with col2:
        st.metric("Frecuencia B", f"{frecuencia:.1f}")

    with col3:
        st.metric("Decaimiento C", f"{decaimiento:.2f}")

    st.caption(
        "Los valores son calculados con NumPy y visualizados con Plotly."
    )

# ==================================================
# 3. ANÁLISIS ESTADÍSTICO
# ==================================================

else:

    st.header("📈 Análisis estadístico")

    st.write(
        """
        Pandas calcula las medidas estadísticas y Plotly permite
        visualizar interactivamente la distribución de los datos.
        """
    )

    nombres = {
        "sepal_length": "Longitud del sépalo",
        "sepal_width": "Ancho del sépalo",
        "petal_length": "Longitud del pétalo",
        "petal_width": "Ancho del pétalo"
    }

    variable = st.selectbox(
        "Selecciona una variable:",
        list(nombres.keys()),
        format_func=lambda v: nombres[v]
    )

    serie = df[variable]

    # Cálculos realizados por Pandas
    media = serie.mean()
    mediana = serie.median()
    desviacion = serie.std()
    minimo = serie.min()
    maximo = serie.max()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Media", f"{media:.2f}")

    with col2:
        st.metric("Mediana", f"{mediana:.2f}")

    with col3:
        st.metric(
            "Desv. estándar",
            f"{desviacion:.2f}"
        )

    with col4:
        st.metric("Mínimo", f"{minimo:.2f}")

    with col5:
        st.metric("Máximo", f"{maximo:.2f}")

    fig = px.histogram(
        df,
        x=variable,
        color="species",
        marginal="box",
        title=f"Distribución de {nombres[variable]}",
        labels={
            variable: nombres[variable],
            "species": "Especie"
        }
    )

    # Línea de la media
    fig.add_vline(
        x=media,
        line_dash="dash",
        annotation_text=f"Media = {media:.2f}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Las medidas estadísticas son calculadas con Pandas; "
        "Plotly se utiliza para su representación gráfica."
    )