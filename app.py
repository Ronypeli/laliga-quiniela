# app.py - App web para móvil
import streamlit as st
from datetime import datetime
import requests
import json

# === CONFIGURACIÓN API ===
API_KEY = "6ef105812ccfbff01bb97394e344e896"
HOST = "https://v3.football.api-sports.io"
HEADERS = {
    'x-apisports-key': API_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

# === OBTENER JORNADA ACTUAL ===
def obtener_jornada():
    # Simulación de jornada según fecha
    from datetime import datetime
    hoy = datetime.now()
    if hoy.month == 8 and hoy.day >= 30:
        return "3"
    elif hoy.month == 9 and hoy.day >= 13:
        return "4"
    return "3"  # por defecto

JORNADA = obtener_jornada()

# === OBTENER PARTIDOS ===
def obtener_partidos():
    url = f"{HOST}/fixtures"
    params = {
        "league": 140,
        "season": 2025,
        "round": f"Regular Season - {JORNADA}"
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        if "response" in data:
            return [
                {"local": p["teams"]["home"]["name"], "visitante": p["teams"]["away"]["name"]}
                for p in data["response"]
            ]
    except:
        pass
    # Datos de respaldo si falla la API
    return [
        {"local": "Elche", "visitante": "Levante"},
        {"local": "Valencia", "visitante": "Getafe"},
        {"local": "Alavés", "visitante": "Atlético"},
        {"local": "Oviedo", "visitante": "Real Sociedad"},
        {"local": "Girona", "visitante": "Sevilla"},
        {"local": "Real Madrid", "visitante": "Mallorca"},
        {"local": "Celta", "visitante": "Villarreal"},
        {"local": "Betis", "visitante": "Athletic"},
        {"local": "Espanyol", "visitante": "Osasuna"},
        {"local": "Rayo", "visitante": "Barcelona"}
    ]

# === INTERFAZ WEB ===
st.set_page_config(page_title="🎯 Quiniela Automática", layout="centered")
st.title("🎯 Quiniela LaLiga - Jornada " + JORNADA)
st.write(f"📅 Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

partidos = obtener_partidos()

st.markdown("### 🔮 Pronóstico Automático")
for i, p in enumerate(partidos, 1):
    # Aquí iría el modelo, pero usamos un ejemplo
    pred = "2" if "Real" in p["local"] or "Barcelona" in p["visitante"] else "X"
    if "Elche" in p["local"]: pred = "2"
    if "Rayo" in p["local"] and "Barcelona" in p["visitante"]: pred = "X"
    st.write(f"**{i}. {p['local']} vs {p['visitante']}** → `{pred}`")

st.markdown("### 💡 Dobles Sugeridos")
st.write("• Valencia vs Getafe → X/2")
st.write("• Betis vs Athletic → X/1")
st.write("• Rayo vs Barcelona → X/2")

st.markdown("### 🏆 Pleno al 15")
st.success("**Resultado sugerido: 1 - 1**")

st.markdown("---")
st.caption("App creada con ❤️ | Actualización automática")
