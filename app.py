import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
import random

# Configuración de página con diseño ancho
st.set_page_config(
    page_title="Nexus Control Grid",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS personalizados para una interfaz radicalmente diferente
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: #f3f4f6;
    }
    .cyber-card {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        border: 1px solid #1e3a8a;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 0 20px rgba(30, 58, 138, 0.2);
    }
    .terminal-box {
        background-color: #000000;
        border: 1px solid #374151;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar variables de estado
if 'system_status' not in st.session_state:
    st.session_state.system_status = "STANDBY"
if 'last_action' not in st.session_state:
    st.session_state.last_action = "Ninguna"

# Configuración de red MQTT
BROKER = "157.230.214.127"
PORT = 1883
TOPIC_SWITCH = "cmqtt_s"
TOPIC_ANALOG = "cmqtt_a"

# Función de publicación segura
def publish_mqtt(topic, payload_dict):
    try:
        client_id = f"nexus_grid_{random.randint(1000,9999)}"
        client = paho.Client(client_id=client_id, protocol=paho.MQTTv311)
        client.connect(BROKER, PORT, 60)
        message = json.dumps(payload_dict)
        client.publish(topic, message)
        client.disconnect()
        return True
    except Exception as e:
        return str(e)

# --- ENCABEZADO TIPO TERMINAL INDUSTRIAL ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #172554 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0; font-size: 2rem;">⚡ NEXUS // Control Grid IoT</h1>
        <p style="color: #93c5fd; margin: 5px 0 0 0;">Interfaz Centralizada de Actuadores y Telemetría Remota</p>
    </div>
""", unsafe_allow_html=True)

# Pestañas de navegación para una estructura totalmente nueva
tab_control, tab_telemetry, tab_diagnostics = st.tabs(["🎛️ Centro de Mando", "📊 Modulador Analógico", "🛠️ Diagnóstico del Sistema"])

with tab_control:
    st.markdown("### 🔌 Control de Potencia (Actuadores)")
    
    col_btn1, col_btn2, col_info = st.columns([1, 1, 2], gap="medium")
    
    with col_btn1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("#### Estado: ENCENDIDO")
        if st.button('🚀 ACTIVAR SISTEMA (ON)', use_container_width=True):
            res = publish_mqtt(TOPIC_SWITCH, {"Act1": "ON"})
            if res is True:
                st.session_state.system_status = "ON"
                st.session_state.last_action = "Comando ON enviado a cmqtt_s"
                st.success("¡Señal ON enviada!")
            else:
                st.error(f"Error: {res}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_btn2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("#### Estado: APAGADO")
        if st.button('🛑 DETENER SISTEMA (OFF)', use_container_width=True):
            res = publish_mqtt(TOPIC_SWITCH, {"Act1": "OFF"})
            if res is True:
                st.session_state.system_status = "OFF"
                st.session_state.last_action = "Comando OFF enviado a cmqtt_s"
                st.warning("¡Señal OFF enviada!")
            else:
                st.error(f"Error: {res}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown("#### 📋 Registro de Actividad Reciente")
        st.markdown(f"""
            <div class="terminal-box">
                > Estado Actual: {st.session_state.system_status}<br>
                > Última Acción: {st.session_state.last_action}<br>
                > Destino MQTT: {BROKER}:{PORT} [{TOPIC_SWITCH}]
            </div>
        """, unsafe_allow_html=True)

with tab_telemetry:
    st.markdown("### 🎚️ Modulación de Señal Analógica")
    
    col_slider, col_preview = st.columns([2, 1], gap="large")
    
    with col_slider:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        slider_val = st.slider('Ajuste de Salida Variable (0 - 100)', 0.0, 100.0, 50.0, step=0.5)
        
        if st.button('📤 Enviar Valor Analógico al Tópico', use_container_width=True):
            res = publish_mqtt(TOPIC_ANALOG, {"Analog": float(slider_val)})
            if res is True:
                st.success(f"Valor analógico [{slider_val}] despachado con éxito a cmqtt_a")
            else:
                st.error(f"Error de red: {res}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_preview:
        st.metric(label="Valor Seleccionado en Tiempo Real", value=f"{slider_val} units")
        st.info("Este valor se serializa en formato JSON y se transmite instantáneamente por el canal MQTT configurado.")

with tab_diagnostics:
    st.markdown("### ⚙️ Diagnóstico del Entorno de Ejecución")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("Versión de Python en Ejecución:", platform.python_version())
        st.write("Sistema Operativo del Servidor:", platform.system())
    with col_d2:
        st.write("Broker Destino:", BROKER)
        st.write("Puerto Activo:", PORT)

# Pie de página técnico
st.divider()
st.markdown("<p style='text-align: center; color: #4b5563; font-size: 0.75rem;'>Nexus IoT Grid Core • Secure MQTT Communication Layer</p>", unsafe_allow_html=True)
