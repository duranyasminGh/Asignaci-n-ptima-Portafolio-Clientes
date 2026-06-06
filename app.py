import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Asignación Óptima de Portafolio Clientes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS PERSONALIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .main { background-color: #0d1117; }

    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #0f1923 50%, #0d1117 100%);
    }

    h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif; font-weight: 700; }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4aa, #0096ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8b949e;
        font-weight: 400;
        margin-bottom: 1.5rem;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.02em;
    }

    .info-card {
        background: linear-gradient(135deg, #161b22, #1c2128);
        border: 1px solid #21262d;
        border-left: 3px solid #00d4aa;
        border-radius: 8px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        font-size: 0.92rem;
        color: #c9d1d9;
        line-height: 1.65;
    }

    .info-card strong { color: #00d4aa; }

    .metric-card {
        background: linear-gradient(135deg, #161b22, #1c2128);
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        text-align: center;
    }

    .section-header {
        font-size: 1.15rem;
        font-weight: 600;
        color: #e6edf3;
        border-bottom: 2px solid #00d4aa;
        padding-bottom: 0.4rem;
        margin: 1.6rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tag {
        display: inline-block;
        background: rgba(0, 212, 170, 0.12);
        color: #00d4aa;
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 4px;
        padding: 0.15rem 0.5rem;
        font-size: 0.75rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 500;
        margin-left: 0.5rem;
        vertical-align: middle;
    }

    .upload-zone {
        background: linear-gradient(135deg, #161b22, #1c2128);
        border: 2px dashed #30363d;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        color: #8b949e;
        margin: 1rem 0;
    }

    .upload-zone:hover { border-color: #00d4aa; }

    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #161b22, #1c2128);
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }

    div[data-testid="stMetric"] label {
        color: #8b949e !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-family: 'IBM Plex Mono', monospace !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #00d4aa !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    .sidebar-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8b949e;
        font-family: 'IBM Plex Mono', monospace;
        margin-bottom: 0.3rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #0096ff);
        color: #0d1117;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    .warning-box {
        background: rgba(255, 171, 0, 0.08);
        border: 1px solid rgba(255, 171, 0, 0.3);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #ffab00;
        font-size: 0.88rem;
    }

    .success-box {
        background: rgba(0, 212, 170, 0.08);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #00d4aa;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETA PLOTLY OSCURA
# ─────────────────────────────────────────────
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(family="IBM Plex Sans", color="#c9d1d9"),
        title_font=dict(family="IBM Plex Sans", color="#e6edf3", size=14),
        xaxis=dict(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d"),
        legend=dict(bgcolor="rgba(22,27,34,0.8)", bordercolor="#30363d", borderwidth=1),
        colorway=["#00d4aa", "#0096ff", "#7c3aed", "#f97316", "#ec4899",
                  "#facc15", "#22c55e", "#ef4444", "#06b6d4", "#a855f7"]
    )
)

# ─────────────────────────────────────────────
# ENCABEZADO PRINCIPAL
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">📊 Asignación Óptima de Portafolio Clientes</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Modelo Markowitz aplicado a la concentración comercial · PyMEs LATAM</div>', unsafe_allow_html=True)

# Texto introductorio
st.markdown("""
<div class="info-card">
<strong>¿Qué hace esta herramienta?</strong><br>
Aplica la teoría moderna de portafolios de <strong>Harry Markowitz (1952)</strong> al análisis de la cartera de clientes de una PyME.
En lugar de optimizar activos bursátiles, aquí <em>cada cliente es tratado como un activo</em> y su <em>participación histórica sobre los ingresos totales</em>
representa el rendimiento esperado. El objetivo es encontrar la combinación de pesos por cliente que <strong>minimiza la dependencia comercial
y el riesgo de concentración</strong>, maximizando el índice de Sharpe (Distribución/Riesgo).<br><br>
<strong>Pregunta que responde:</strong> ¿Cuál es la combinación óptima de clientes para reducir dependencia y minimizar riesgo?
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    st.markdown("---")

    st.markdown('<div class="sidebar-label">📁 Archivo de datos</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Carga tu archivo Excel (.xlsx)",
        type=["xlsx"],
        help="Primera columna: Cliente | Columnas siguientes: % participación por período"
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-label">🎲 Simulaciones Monte Carlo</div>', unsafe_allow_html=True)
    n_simulations = st.slider("Número de simulaciones", 500, 10000, 3000, 500,
                               help="Mayor número = frontera más precisa (pero más lento)")

    st.markdown('<div class="sidebar-label">💰 Ingresos totales ($)</div>', unsafe_allow_html=True)
    total_revenue = st.number_input(
        "Ingresos totales del período",
        min_value=0.0,
        value=1_000_000.0,
        step=50_000.0,
        format="%.2f",
        help="Se usará para calcular el monto asignado a cada cliente"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem; color:#8b949e; font-family:'IBM Plex Mono',monospace; line-height:1.6;">
    <strong style="color:#00d4aa;">Formato esperado del Excel:</strong><br>
    • Col 1: Nombre del cliente<br>
    • Col 2+: % participación histórica<br>
    • Mínimo: 3 observaciones<br>
    • Valores: 0–100 o 0.0–1.0
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#484f58; text-align:center; font-family:'IBM Plex Mono',monospace;">
    Teoría de Portafolios · Markowitz 1952<br>
    Aplicación Finanzas Corporativas LATAM
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTADO INICIAL SIN ARCHIVO
# ─────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("""
    <div class="upload-zone">
        <div style="font-size:3rem; margin-bottom:0.8rem;">📂</div>
        <div style="font-size:1.1rem; font-weight:600; color:#c9d1d9; margin-bottom:0.5rem;">
            Carga tu archivo de datos para comenzar
        </div>
        <div style="font-size:0.88rem; color:#484f58;">
            Usa el panel lateral izquierdo → Archivo Excel (.xlsx)<br>
            con la participación histórica de clientes sobre ingresos
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ejemplo de estructura esperada
    st.markdown('<div class="section-header">📋 Estructura esperada del archivo</div>', unsafe_allow_html=True)
    ejemplo = pd.DataFrame({
        "Cliente":       ["Cliente A", "Cliente B", "Cliente C", "Cliente D"],
        "Ene-2023 (%)":  [35.0, 20.0, 25.0, 20.0],
        "Feb-2023 (%)":  [32.0, 23.0, 28.0, 17.0],
        "Mar-2023 (%)":  [30.0, 25.0, 27.0, 18.0],
        "Abr-2023 (%)":  [28.0, 27.0, 26.0, 19.0],
    })
    st.dataframe(ejemplo, use_container_width=True, hide_index=True)
    st.markdown("""
    <div style="font-size:0.82rem; color:#8b949e; margin-top:0.5rem;">
    💡 Los valores pueden estar en formato porcentual (35.0) o decimal (0.35) — la app los normaliza automáticamente.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# CARGA Y VALIDACIÓN DE DATOS
# ─────────────────────────────────────────────
try:
    df_raw = pd.read_excel(uploaded_file, engine="openpyxl")

    if df_raw.shape[1] < 2:
        st.error("❌ El archivo debe tener al menos 2 columnas: Cliente y un período de participación.")
        st.stop()

    col_cliente = df_raw.columns[0]
    cols_periodos = df_raw.columns[1:].tolist()

    if len(cols_periodos) < 3:
        st.error(f"❌ Se requieren mínimo **3 observaciones históricas**. El archivo tiene {len(cols_periodos)}.")
        st.stop()

    df_raw[col_cliente] = df_raw[col_cliente].astype(str).str.strip()
    df_raw = df_raw.set_index(col_cliente)

    for col in cols_periodos:
        df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce")

    df_raw = df_raw.dropna()

    if df_raw.shape[0] < 2:
        st.error("❌ Después de eliminar filas con datos faltantes, quedan menos de 2 clientes. Verifica el archivo.")
        st.stop()

    # Normalizar: si los valores están entre 0-1, convertir a porcentaje
    max_val = df_raw.values.max()
    if max_val <= 1.0:
        df_raw = df_raw * 100

    # df_pct: filas=clientes, columnas=períodos
    df_pct = df_raw.copy()

    n_clientes = df_pct.shape[0]
    n_periodos = df_pct.shape[1]
    clientes = df_pct.index.tolist()

    st.markdown(f"""
    <div class="success-box">
    ✅ Archivo cargado correctamente: <strong>{n_clientes} clientes</strong> · <strong>{n_periodos} períodos históricos</strong>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SECCIÓN 1: DATOS HISTÓRICOS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Participación Histórica por Cliente <span class="tag">% sobre ingresos</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("**Tabla de participaciones históricas (%)**")
    st.dataframe(
        df_pct.style.format("{:.2f}%").background_gradient(cmap="YlOrRd", axis=None),
        use_container_width=True
    )

with col2:
    st.markdown("**Estadísticas descriptivas**")
    desc = df_pct.T.describe().T[["mean", "std", "min", "max"]]
    desc.columns = ["Media %", "Desv. Std %", "Mín %", "Máx %"]
    st.dataframe(desc.style.format("{:.2f}"), use_container_width=True)

# ─────────────────────────────────────────────
# SECCIÓN 2: RETORNO ESPERADO Y RIESGO
# ─────────────────────────────────────────────
try:
    retorno_esperado = df_pct.mean(axis=1)     # media histórica por cliente
    riesgo_cliente   = df_pct.std(axis=1)       # desviación estándar histórica

    st.markdown('<div class="section-header">📈 Retorno Esperado y Riesgo por Cliente</div>', unsafe_allow_html=True)

    df_metricas = pd.DataFrame({
        "Cliente": clientes,
        "Participación Media (%)": retorno_esperado.values,
        "Riesgo / Concentración (Desv. Std %)": riesgo_cliente.values,
        "Coef. Variación (%)": (riesgo_cliente / retorno_esperado * 100).values
    })

    col_m1, col_m2 = st.columns([1.4, 1])

    with col_m1:
        st.dataframe(df_metricas.style.format({
            "Participación Media (%)": "{:.2f}",
            "Riesgo / Concentración (Desv. Std %)": "{:.2f}",
            "Coef. Variación (%)": "{:.1f}"
        }), use_container_width=True, hide_index=True)

    with col_m2:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Participación Media %",
            x=clientes,
            y=retorno_esperado.values,
            marker_color="#00d4aa",
            opacity=0.85
        ))
        fig_bar.add_trace(go.Bar(
            name="Riesgo (Desv. Std %)",
            x=clientes,
            y=riesgo_cliente.values,
            marker_color="#f97316",
            opacity=0.85
        ))
        fig_bar.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            barmode="group",
            title="Retorno vs Riesgo por Cliente",
            height=300,
            margin=dict(l=20, r=20, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error calculando métricas: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SECCIÓN 3: CORRELACIÓN Y COVARIANZA
# ─────────────────────────────────────────────
try:
    df_T = df_pct.T   # períodos × clientes (para calcular correlación entre clientes)
    corr_matrix = df_T.corr()
    cov_matrix  = df_T.cov()

    st.markdown('<div class="section-header">🔗 Matrices de Correlación y Covarianza</div>', unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown("**Matriz de Correlación**")
        st.dataframe(corr_matrix.style.format("{:.3f}").background_gradient(
            cmap="RdYlGn", vmin=-1, vmax=1), use_container_width=True)

        fig_corr = px.imshow(
            corr_matrix,
            color_continuous_scale="RdYlGn",
            zmin=-1, zmax=1,
            text_auto=".2f",
            title="Heatmap de Correlación"
        )
        fig_corr.update_layout(**PLOTLY_TEMPLATE["layout"], height=350,
                               margin=dict(l=10, r=10, t=40, b=10))
        fig_corr.update_coloraxes(colorbar=dict(tickfont=dict(color="#8b949e")))
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_c2:
        st.markdown("**Matriz de Covarianza**")
        st.dataframe(cov_matrix.style.format("{:.3f}").background_gradient(
            cmap="Blues"), use_container_width=True)

        fig_cov = px.imshow(
            cov_matrix,
            color_continuous_scale="Blues",
            text_auto=".2f",
            title="Heatmap de Covarianza"
        )
        fig_cov.update_layout(**PLOTLY_TEMPLATE["layout"], height=350,
                              margin=dict(l=10, r=10, t=40, b=10))
        fig_cov.update_coloraxes(colorbar=dict(tickfont=dict(color="#8b949e")))
        st.plotly_chart(fig_cov, use_container_width=True)

    # Nota interpretativa
    st.markdown("""
    <div class="info-card">
    <strong>Interpretación:</strong> Correlación cercana a <strong>+1</strong> indica que dos clientes tienen comportamientos muy similares
    (alta dependencia conjunta). Correlaciones <strong>bajas o negativas</strong> entre clientes son deseables porque ofrecen
    mayor diversificación comercial y reducen el riesgo de concentración del portafolio.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error en matrices: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SECCIÓN 4: SIMULACIÓN MONTE CARLO
# ─────────────────────────────────────────────
try:
    st.markdown(f'<div class="section-header">🎲 Simulación Monte Carlo <span class="tag">{n_simulations:,} portafolios</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
    <strong>Metodología:</strong> Se generan <em>n</em> combinaciones aleatorias de pesos para cada cliente (normalizados a 100%).
    Para cada portafolio se calcula: <strong>(1)</strong> Participación ponderada esperada,
    <strong>(2)</strong> Riesgo usando la matriz de covarianza (riesgo sistémico de concentración),
    <strong>(3)</strong> Índice de Sharpe = Participación / Riesgo.
    El portafolio óptimo es el de <strong>mayor Sharpe</strong>.
    </div>
    """, unsafe_allow_html=True)

    np.random.seed(42)
    cov_array = cov_matrix.values
    retornos_array = retorno_esperado.values

    port_retornos  = np.zeros(n_simulations)
    port_riesgos   = np.zeros(n_simulations)
    port_sharpes   = np.zeros(n_simulations)
    port_pesos     = np.zeros((n_simulations, n_clientes))

    with st.spinner("Ejecutando simulación Monte Carlo..."):
        for i in range(n_simulations):
            pesos = np.random.random(n_clientes)
            pesos /= pesos.sum()

            ret  = np.dot(pesos, retornos_array)
            var  = np.dot(pesos.T, np.dot(cov_array, pesos))
            risk = np.sqrt(var)
            sharpe = ret / risk if risk > 0 else 0

            port_retornos[i]  = ret
            port_riesgos[i]   = risk
            port_sharpes[i]   = sharpe
            port_pesos[i]     = pesos

    idx_opt = np.argmax(port_sharpes)
    pesos_opt   = port_pesos[idx_opt]
    ret_opt     = port_retornos[idx_opt]
    riesgo_opt  = port_riesgos[idx_opt]
    sharpe_opt  = port_sharpes[idx_opt]

except Exception as e:
    st.error(f"❌ Error en simulación: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SECCIÓN 5: FRONTERA EFICIENTE
# ─────────────────────────────────────────────
try:
    st.markdown('<div class="section-header">📉 Frontera Eficiente Comercial</div>', unsafe_allow_html=True)

    fig_fe = go.Figure()

    # Nube de portafolios
    fig_fe.add_trace(go.Scatter(
        x=port_riesgos,
        y=port_retornos,
        mode="markers",
        marker=dict(
            size=4,
            color=port_sharpes,
            colorscale="Viridis",
            showscale=True,
            opacity=0.55,
            colorbar=dict(
                title=dict(text="Índice Sharpe", font=dict(color="#8b949e")),
                tickfont=dict(color="#8b949e")
            )
        ),
        name="Portafolios simulados",
        hovertemplate="Riesgo: %{x:.2f}%<br>Participación: %{y:.2f}%<extra></extra>"
    ))

    # Portafolio óptimo
    fig_fe.add_trace(go.Scatter(
        x=[riesgo_opt],
        y=[ret_opt],
        mode="markers",
        marker=dict(
            symbol="star",
            size=20,
            color="#ff4444",
            line=dict(color="#ffffff", width=1.5)
        ),
        name=f"⭐ Óptimo (Sharpe: {sharpe_opt:.2f})",
        hovertemplate=f"<b>Portafolio Óptimo</b><br>Riesgo: {riesgo_opt:.2f}%<br>Participación: {ret_opt:.2f}%<br>Sharpe: {sharpe_opt:.2f}<extra></extra>"
    ))

    fig_fe.update_layout(
        **PLOTLY_TEMPLATE["layout"],
        title="Frontera Eficiente — Portafolio de Clientes",
        xaxis_title="Riesgo de Concentración (Desv. Std %)",
        yaxis_title="Participación Esperada (%)",
        height=480,
        margin=dict(l=40, r=40, t=50, b=50)
    )

    st.plotly_chart(fig_fe, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error graficando frontera: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SECCIÓN 6: CARTERA ÓPTIMA
# ─────────────────────────────────────────────
try:
    st.markdown('<div class="section-header">⭐ Cartera Óptima — Asignación por Cliente</div>', unsafe_allow_html=True)

    # Métricas clave
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Participación Óptima", f"{ret_opt:.2f}%", help="Participación ponderada esperada del portafolio óptimo")
    with col_m2:
        st.metric("Riesgo de Concentración", f"{riesgo_opt:.2f}%", help="Desviación estándar del portafolio óptimo")
    with col_m3:
        st.metric("Índice de Sharpe", f"{sharpe_opt:.3f}", help="Participación / Riesgo — mayor es mejor")
    with col_m4:
        st.metric("Ingresos Totales", f"${total_revenue:,.0f}", help="Ingresos ingresados en la barra lateral")

    st.markdown("---")

    # Tabla de asignación óptima
    montos = pesos_opt * total_revenue
    participaciones = pesos_opt * 100

    df_optimo = pd.DataFrame({
        "Cliente": clientes,
        "Peso Óptimo (%)": participaciones,
        "Monto Asignado ($)": montos,
        "Participación Media Histórica (%)": retorno_esperado.values,
        "Riesgo Individual (Desv. Std %)": riesgo_cliente.values,
    })
    df_optimo = df_optimo.sort_values("Peso Óptimo (%)", ascending=False).reset_index(drop=True)

    col_t1, col_t2 = st.columns([1.2, 1])

    with col_t1:
        st.markdown("**Asignación óptima detallada**")
        st.dataframe(
            df_optimo.style.format({
                "Peso Óptimo (%)": "{:.2f}%",
                "Monto Asignado ($)": "${:,.2f}",
                "Participación Media Histórica (%)": "{:.2f}%",
                "Riesgo Individual (Desv. Std %)": "{:.2f}%"
            }).bar(subset=["Peso Óptimo (%)"], color="#00d4aa33"),
            use_container_width=True,
            hide_index=True
        )

    with col_t2:
        st.markdown("**Distribución óptima del portafolio**")
        fig_donut = go.Figure(go.Pie(
            labels=df_optimo["Cliente"],
            values=df_optimo["Peso Óptimo (%)"],
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(size=11, family="IBM Plex Sans"),
            marker=dict(
                colors=["#00d4aa", "#0096ff", "#7c3aed", "#f97316",
                        "#ec4899", "#facc15", "#22c55e", "#ef4444",
                        "#06b6d4", "#a855f7"][:n_clientes],
                line=dict(color="#0d1117", width=2)
            ),
            hovertemplate="<b>%{label}</b><br>Peso: %{value:.2f}%<br>Monto: $%{customdata:,.0f}<extra></extra>",
            customdata=df_optimo["Monto Asignado ($)"]
        ))
        fig_donut.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            title="Distribución Óptima del Presupuesto",
            height=380,
            margin=dict(l=10, r=10, t=40, b=10),
            annotations=[dict(
                text=f"${total_revenue/1e6:.1f}M" if total_revenue >= 1e6 else f"${total_revenue:,.0f}",
                x=0.5, y=0.5,
                font=dict(size=14, color="#e6edf3", family="IBM Plex Mono"),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error en cartera óptima: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SECCIÓN 7: ANÁLISIS COMPARATIVO
# ─────────────────────────────────────────────
try:
    st.markdown('<div class="section-header">🔎 Comparativo: Actual vs Óptimo</div>', unsafe_allow_html=True)

    # Participación actual = promedio histórico normalizado
    pesos_actual = retorno_esperado / retorno_esperado.sum()

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Participación Actual (promedio histórico)",
        x=clientes,
        y=(pesos_actual * 100).values,
        marker_color="#f97316",
        opacity=0.80
    ))
    fig_comp.add_trace(go.Bar(
        name="Asignación Óptima Markowitz",
        x=clientes,
        y=participaciones,
        marker_color="#00d4aa",
        opacity=0.80
    ))
    fig_comp.update_layout(
        **PLOTLY_TEMPLATE["layout"],
        barmode="group",
        title="Participación Actual vs Asignación Óptima por Cliente (%)",
        yaxis_title="Participación (%)",
        xaxis_title="Cliente",
        height=380,
        margin=dict(l=40, r=40, t=50, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Conclusión
    cliente_mas_concentrado = df_optimo.iloc[0]["Cliente"]
    st.markdown(f"""
    <div class="info-card">
    <strong>Conclusión del modelo:</strong><br>
    La cartera óptima sugiere una <strong>participación esperada del {ret_opt:.2f}%</strong> con un riesgo de concentración de
    <strong>{riesgo_opt:.2f}%</strong> y un índice de Sharpe de <strong>{sharpe_opt:.3f}</strong>.
    La mayor asignación recae en <strong>{cliente_mas_concentrado}</strong> con un peso de <strong>{df_optimo.iloc[0]['Peso Óptimo (%)']:.2f}%</strong>.
    Esta distribución minimiza la dependencia comercial individual maximizando la diversificación de ingresos,
    en línea con los principios de la <em>Teoría Moderna de Portafolios</em>.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error en comparativo: {e}")
    st.stop()

# ─────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#484f58; font-size:0.78rem; font-family:'IBM Plex Mono',monospace; padding:0.5rem;">
Modelo de Markowitz aplicado a Portafolio de Clientes · Finanzas Corporativas LATAM ·
Referencia: Markowitz, H. (1952). Portfolio Selection. <em>The Journal of Finance</em>, 7(1), 77–91.
</div>
""", unsafe_allow_html=True)
