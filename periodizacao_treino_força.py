import streamlit as st
import pandas as pd
import json
import os

# -------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (MOBILE-FIRST)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Sistema Definitivo de Força & Tendões",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# ESTILIZAÇÃO VISUAL (CSS ADAPTÁVEL PARA SMARTPHONES)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Reduz margens no celular para aproveitar toda a tela */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }
    /* Cartões de exercícios */
    .workout-card {
        background-color: #1a1c24;
        border: 1px solid #2d313e;
        border-left: 5px solid #ff4b4b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        color: #f0f2f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.25);
    }
    .tendon-card {
        background-color: #132226;
        border: 1px solid #1f444c;
        border-left: 5px solid #00d4ff;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 14px;
        color: #e6f9ff;
    }
    .acc-card {
        background-color: #181920;
        border: 1px solid #2b2d38;
        border-left: 5px solid #10b981;
        border-radius: 10px;
        padding: 13px;
        margin-bottom: 10px;
        color: #e2e8f0;
    }
    .badge-main {
        background-color: #ff4b4b;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-tendon {
        background-color: #00d4ff;
        color: #001f26;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-acc {
        background-color: #10b981;
        color: #022c22;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .weight-highlight {
        font-size: 1.55rem;
        font-weight: 800;
        color: #ff9f1c;
        margin: 6px 0;
    }
    .plate-box {
        background-color: #262936;
        padding: 7px 12px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.92rem;
        color: #cbd5e1;
        margin-top: 6px;
        border: 1px dashed #475569;
    }
    .metric-mini {
        background-color: #1e212b;
        border: 1px solid #323746;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    .metric-mini .label {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .metric-mini .val {
        font-size: 1.25rem;
        font-weight: 800;
        color: #f8fafc;
    }
    /* Botões maiores para toque no celular */
    .stButton > button {
        min-height: 46px;
        font-weight: 600;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# PERSISTÊNCIA LOCAL DE DADOS (JSON)
# -------------------------------------------------------------
ARQUIVO_CONFIG = "treino_config.json"

DADOS_PADRAO = {
    "ciclo": 1,
    "semana_atual": 1,
    "barra_kg": 20.0,
    "sq_1rm": 90.0,
    "bp_1rm": 80.0,
    "dl_1rm": 140.0,
    "ohp_base": 45.0,
    "farmer_halt": 28.0
}

def carregar_config():
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return {**DADOS_PADRAO, **dados}
        except Exception:
            return DADOS_PADRAO.copy()
    return DADOS_PADRAO.copy()

def salvar_config():
    dados = {
        "ciclo": st.session_state.ciclo,
        "semana_atual": st.session_state.semana_atual,
        "barra_kg": st.session_state.barra_kg,
        "sq_1rm": st.session_state.sq_1rm,
        "bp_1rm": st.session_state.bp_1rm,
        "dl_1rm": st.session_state.dl_1rm,
        "ohp_base": st.session_state.ohp_base,
        "farmer_halt": st.session_state.farmer_halt
    }
    try:
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception:
        pass

# -------------------------------------------------------------
# AUTENTICAÇÃO COM SENHA (STREAMLIT SECRETS)
# -------------------------------------------------------------
def verificar_autenticacao():
    """Autenticação otimizada para teclado mobile com formulário."""
    if st.session_state.get("autenticado", False):
        return True

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("## 🔒 Sistema de Força & Tendões")
        st.caption("Acesso exclusivo. Digite sua credencial configurada no Streamlit Secrets.")
        with st.form("form_login", clear_on_submit=True):
            senha_digitada = st.text_input("Palavra-passe", type="password", placeholder="Digite a senha...")
            submit = st.form_submit_button("🔓 Entrar no Treinamento", use_container_width=True)
            if submit:
                senha_correta = st.secrets.get("app_password", "")
                if senha_digitada == senha_correta:
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("❌ Palavra-passe incorreta.")
    return False

if not verificar_autenticacao():
    st.stop()

# -------------------------------------------------------------
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# -------------------------------------------------------------
if "dados_carregados" not in st.session_state:
    cfg_salva = carregar_config()
    for chave, valor in cfg_salva.items():
        st.session_state[chave] = valor
    st.session_state.dados_carregados = True

# -------------------------------------------------------------
# FUNÇÕES DE CÁLCULO BIOMECÂNICO E ANILHAS
# -------------------------------------------------------------
def arredondar_carga(peso, passo=2.5):
    return round(peso / passo) * passo

def calcular_anilhas(peso_total, barra=20.0):
    if peso_total <= barra:
        return "Apenas a barra vazia"
    peso_lado = (peso_total - barra) / 2.0
    anilhas = [25.0, 20.0, 15.0, 10.0, 5.0, 2.5, 1.25]
    resultado = []
    restante = peso_lado
    for anilha in anilhas:
        qtd = int(restante // anilha)
        if qtd > 0:
            resultado.append(f"{qtd}×{anilha:g}kg")
            restante = round(restante - (qtd * anilha), 2)
    return " + ".join(resultado) + " (cada lado)"

def gerar_rampagem(nome, carga_alvo, barra=20.0):
    if "terra" in nome.lower() or "deadlift" in nome.lower():
        p1 = max(60.0, arredondar_carga(carga_alvo * 0.50))
        p2 = arredondar_carga(carga_alvo * 0.68)
        p3 = arredondar_carga(carga_alvo * 0.82)
        p4 = arredondar_carga(carga_alvo * 0.92)
        etapas = [
            {"Etapa": "1. Base (45cm)", "Carga": f"{p1:.1f} kg", "Reps": "5 reps", "Anilhas / Lado": calcular_anilhas(p1, barra), "Foco Neural": "Posição de cunha e puxar a folga da barra"},
            {"Etapa": "2. Aquecimento", "Carga": f"{p2:.1f} kg", "Reps": "3 reps", "Anilhas / Lado": calcular_anilhas(p2, barra), "Foco Neural": "Aceleração máxima do chão"},
            {"Etapa": "3. Aproximação", "Carga": f"{p3:.1f} kg", "Reps": "2 reps", "Anilhas / Lado": calcular_anilhas(p3, barra), "Foco Neural": "Bracing abdominal 360°"},
            {"Etapa": "4. Potenciação (PAP)", "Carga": f"{p4:.1f} kg", "Reps": "1 rep", "Anilhas / Lado": calcular_anilhas(p4, barra), "Foco Neural": "Despertar unidades motoras IIx sem fadigar"}
        ]
    else:
        p1 = max(barra + 5.0, arredondar_carga(carga_alvo * 0.50))
        p2 = arredondar_carga(carga_alvo * 0.70)
        p3 = arredondar_carga(carga_alvo * 0.88)
        etapas = [
            {"Etapa": "1. Calibragem", "Carga": f"{barra:.1f} kg", "Reps": "2×6 reps", "Anilhas / Lado": "Barra vazia", "Foco Neural": "Padrão articular e pausa no fundo"},
            {"Etapa": "2. Aquecimento", "Carga": f"{p1:.1f} kg", "Reps": "5 reps", "Anilhas / Lado": calcular_anilhas(p1, barra), "Foco Neural": "Descida controlada (3s), subida explosiva"},
            {"Etapa": "3. Aproximação", "Carga": f"{p2:.1f} kg", "Reps": "3 reps", "Anilhas / Lado": calcular_anilhas(p2, barra), "Foco Neural": "Taxa de disparo máxima (CAT)"},
            {"Etapa": "4. Potenciação (PAP)", "Carga": f"{p3:.1f} kg", "Reps": "1 rep", "Anilhas / Lado": calcular_anilhas(p3, barra), "Foco Neural": "Sentir o peso com velocidade alta"}
        ]
    return pd.DataFrame(etapas)

# -------------------------------------------------------------
# MATRIZ DE PERIODIZAÇÃO DE 8 SEMANAS (FORÇA + TENDÕES)
# -------------------------------------------------------------
def obter_dados_semana(num_semana, sq, bp, dl, ohp, farmer):
    """
    Retorna toda a programação da semana escolhida (1 a 8).
    Bloco 1 (Sem 1-3): Acumulação Estrutural e HSR (Espessamento Tendíneo)
    Sem 4: Deload Estrutural
    Bloco 2 (Sem 5-7): Intensificação Neural e Desinibição de OTG (Força Bruta)
    Sem 8: Deload Neural & Supercompensação
    """
    mapa = {
        1: {
            "titulo": "Semana 1 — Base Estrutural & Tensão Tendínea (77,5%)",
            "bloco": "BLOCO 1: REMODELAGEM DE COLÁGENO & BASE MIOFIBRILAR",
            "foco_tendao": "Cadência Excêntrica: Desça a barra em 3 segundos controlados em todas as séries para estimular a síntese de colágeno tipo I.",
            "sq_main": (0.775, "4 séries × 4 reps", "RPE 7.0", None),
            "bp_main": (0.775, "5 séries × 4 reps", "RPE 7.0", None),
            "dl_main": (0.775, "3 séries × 4 reps", "RPE 7.0", None),
            "bp_pausa": (0.65, "4 séries × 3 reps (Pausa 3s no peito)", "RPE 6.5"),
            "pullup": "4 séries × 4 reps (Peso corporal — descida em 3s)",
            "farmer": f"Halteres de {arredondar_carga(farmer):.1f} kg (3 × 30 metros — postura alta)",
            "ohp": f"{arredondar_carga(ohp * 0.95):.1f} kg (3 séries × 5 reps)",
            "row": f"{arredondar_carga(bp * 0.725):.1f} kg (3 séries × 5 reps explosivas)",
            "curl": "Halteres moderados: 3 × 8 reps (3s na descida — proteção do bíceps distal)",
            "bulg": "Halteres 16 kg (3 × 5 reps/perna — pausa de 1s no fundo)",
            "pelv": f"{arredondar_carga(sq * 0.88):.1f} kg (3 × 6 reps — trava 2s no topo)",
            "dips": "3 séries × 5 reps (Peso corporal — descida controlada)",
            "core_seg": "Pallof Press Isométrico: 3 × 15s por lado",
            "core_qui": "Ab Wheel (Rodinha) ou Prancha RKC: 3 × 8 reps / 25s",
            "core_sex": "Hollow Rock Estático: 3 × 30 segundos"
        },
        2: {
            "titulo": "Semana 2 — Densidade Miofibrilar & Carga Lenta (82,5%)",
            "bloco": "BLOCO 1: REMODELAGEM DE COLÁGENO & BASE MIOFIBRILAR",
            "foco_tendao": "Deformação Mecânica Ideal: Cargas acima de 80% atingem os 5% de strain necessários para alinhar e engrossar os feixes tendíneos.",
            "sq_main": (0.825, "4 séries × 3 reps", "RPE 7.5", None),
            "bp_main": (0.825, "5 séries × 3 reps", "RPE 7.5", None),
            "dl_main": (0.825, "3 séries × 3 reps", "RPE 7.5", None),
            "bp_pausa": (0.675, "4 séries × 3 reps (Pausa 3s no peito)", "RPE 7.0"),
            "pullup": "4 séries × 5 reps (Peso corporal — +1 rep por série)",
            "farmer": f"Halteres de {arredondar_carga(farmer + 2.0):.1f} kg (3 × 30 metros)",
            "ohp": f"{arredondar_carga(ohp):.1f} kg (3 séries × 5 reps)",
            "row": f"{arredondar_carga(bp * 0.75):.1f} kg (3 séries × 5 reps)",
            "curl": "Halteres: 3 × 8 reps (3s descida — aumente 1-2 kg se estiver leve)",
            "bulg": "Halteres 18 kg (3 × 5 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 0.92):.1f} kg (3 × 6 reps)",
            "dips": "3 séries × 5 reps (+2,5 kg a 5 kg no cinto)",
            "core_seg": "Pallof Press Isométrico: 3 × 18s por lado",
            "core_qui": "Ab Wheel (Rodinha): 3 × 10 reps controladas",
            "core_sex": "Hollow Rock Estático: 3 × 35 segundos"
        },
        3: {
            "titulo": "Semana 3 — Choque Estrutural (85%)",
            "bloco": "BLOCO 1: REMODELAGEM DE COLÁGENO & BASE MIOFIBRILAR",
            "foco_tendao": "Rigidez de Mola: Controle a transição excêntrica-concêntrica sem relaxar no fundo do movimento.",
            "sq_main": (0.85, "5 séries × 2 reps", "RPE 8.0", None),
            "bp_main": (0.85, "5 séries × 2 reps", "RPE 8.0", None),
            "dl_main": (0.85, "4 séries × 2 reps", "RPE 8.0", None),
            "bp_pausa": (0.70, "4 séries × 2 reps (Pausa 3s no peito)", "RPE 7.5"),
            "pullup": "4 séries × 4 reps (+2,5 kg a 5 kg no cinto)",
            "farmer": f"Halteres de {arredondar_carga(farmer + 4.0):.1f} kg (3 × 25 metros pesados)",
            "ohp": f"{arredondar_carga(ohp + 2.5):.1f} kg (3 séries × 4 reps)",
            "row": f"{arredondar_carga(bp * 0.78):.1f} kg (4 séries × 4 reps)",
            "curl": "Halteres pesados: 3 × 6 reps (3s na descida)",
            "bulg": "Halteres 20 kg (3 × 5 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 0.98):.1f} kg (3 × 5 reps)",
            "dips": "3 séries × 5 reps (+5 kg no cinto)",
            "core_seg": "Pallof Press Isométrico: 3 × 20s por lado (carga alta)",
            "core_qui": "Ab Wheel (Rodinha): 3 × 10 reps (pausa 1s esticado)",
            "core_sex": "Hollow Rock Estático: 3 × 40 segundos"
        },
        4: {
            "titulo": "Semana 4 — Deload Estrutural & Maturação Tendínea (65%)",
            "bloco": "TRANSIÇÃO: SUPERCOMPENSAÇÃO DO TECIDO CONJUNTIVO",
            "foco_tendao": "Semana de Ouro para os Tendões: Mantenha as isometrias de aquecimento e reduza a carga na barra para o colágeno consolidar.",
            "sq_main": (0.65, "3 séries × 3 reps", "RPE 5.0", None),
            "bp_main": (0.65, "3 séries × 3 reps", "RPE 5.0", None),
            "dl_main": (0.65, "2 séries × 2 reps", "RPE 5.0", None),
            "bp_pausa": (0.55, "3 séries × 2 reps (Pausa 3s)", "RPE 4.5"),
            "pullup": "2 séries × 4 reps (Peso corporal)",
            "farmer": f"Halteres de {arredondar_carga(farmer * 0.75):.1f} kg (2 × 25 metros)",
            "ohp": f"{arredondar_carga(ohp * 0.75):.1f} kg (2 séries × 5 reps)",
            "row": f"{arredondar_carga(bp * 0.55):.1f} kg (2 séries × 5 reps)",
            "curl": "Halteres leves: 2 × 10 reps (irrigação sanguínea)",
            "bulg": "Halteres 12 kg (2 × 5 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 0.65):.1f} kg (2 × 5 reps)",
            "dips": "2 séries × 5 reps (Peso corporal)",
            "core_seg": "Pallof Press: 2 × 12s por lado",
            "core_qui": "Prancha RKC: 2 × 20s",
            "core_sex": "Hollow Rock: 2 × 20 segundos"
        },
        5: {
            "titulo": "Semana 5 — Entrada Neural & Potenciação (85% + Single 90%)",
            "bloco": "BLOCO 2: INTENSIFICAÇÃO NEURAL & FORÇA MÁXIMA",
            "foco_tendao": "Recrutamento de Alto Limiar: A repetição única a 90% ensina o SNC a disparar fibras IIx sem fadiga metabólica.",
            "sq_main": (0.85, "3 séries × 2 reps", "RPE 8.0", (0.90, "1 × 1 (Single Neural)", "RPE 8.5")),
            "bp_main": (0.85, "4 séries × 2 reps", "RPE 8.0", (0.90, "1 × 1 (Single Neural)", "RPE 8.5")),
            "dl_main": (0.85, "2 séries × 2 reps", "RPE 8.0", (0.90, "1 × 1 (Single Neural)", "RPE 8.5")),
            "bp_pausa": (0.70, "5 séries × 2 reps (Pausa 3s — subida explosiva)", "RPE 7.5"),
            "pullup": "4 séries × 4 reps (+5 kg no cinto)",
            "farmer": f"Halteres de {arredondar_carga(farmer + 4.0):.1f} kg (3 × 30 metros)",
            "ohp": f"{arredondar_carga(ohp + 2.5):.1f} kg (3 séries × 4 reps)",
            "row": f"{arredondar_carga(bp * 0.78):.1f} kg (3 séries × 4 reps)",
            "curl": "Halteres pesados: 3 × 6 reps (3s descida)",
            "bulg": "Halteres 20 kg (3 × 4 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 1.0):.1f} kg (3 × 5 reps)",
            "dips": "3 séries × 4 reps (+7,5 kg no cinto)",
            "core_seg": "Pallof Press: 3 × 15s/lado (carga alta)",
            "core_qui": "Ab Wheel: 3 × 10 reps",
            "core_sex": "Hollow Rock: 3 × 35 segundos"
        },
        6: {
            "titulo": "Semana 6 — Desinibição de OTG (88% + Single 92,5%)",
            "bloco": "BLOCO 2: INTENSIFICAÇÃO NEURAL & FORÇA MÁXIMA",
            "foco_tendao": "Redução do Freio Golgiano: Cargas a 92,5% dessensibilizam os Órgãos Tendinosos de Golgi, liberando força reprimida.",
            "sq_main": (0.88, "3 séries × 2 reps", "RPE 8.5", (0.925, "1 × 1 (Single Pesada)", "RPE 9.0")),
            "bp_main": (0.88, "3 séries × 2 reps", "RPE 8.5", (0.925, "1 × 1 (Single Pesada)", "RPE 9.0")),
            "dl_main": (0.88, "2 séries × 2 reps", "RPE 8.5", (0.925, "1 × 1 (Single Pesada)", "RPE 9.0")),
            "bp_pausa": (0.725, "5 séries × 2 reps (Pausa 3s cravados)", "RPE 7.5"),
            "pullup": "4 séries × 3 reps (+7,5 kg no cinto)",
            "farmer": f"Halteres de {arredondar_carga(farmer + 6.0):.1f} kg (3 × 25 metros)",
            "ohp": f"{arredondar_carga(ohp + 5.0):.1f} kg (3 séries × 3 a 4 reps)",
            "row": f"{arredondar_carga(bp * 0.80):.1f} kg (3 séries × 4 reps)",
            "curl": "Halteres: 3 × 6 reps (foco isométrico no meio)",
            "bulg": "Halteres 22 kg (3 × 4 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 1.05):.1f} kg (3 × 4 reps)",
            "dips": "3 séries × 4 reps (+10 kg no cinto)",
            "core_seg": "Pallof Press: 3 × 15s/lado (máxima tensão)",
            "core_qui": "Ab Wheel: 3 × 12 reps",
            "core_sex": "Hollow Rock: 3 × 40 segundos"
        },
        7: {
            "titulo": "Semana 7 — Pico Absoluto de Força Pura (90% + Single 95%)",
            "bloco": "BLOCO 2: INTENSIFICAÇÃO NEURAL & FORÇA MÁXIMA",
            "foco_tendao": "Ápice do Mesociclo: Volume reduzido e intensidade máxima. Descanse 5 minutos completos antes da Single de 95%.",
            "sq_main": (0.90, "2 séries × 1 rep", "RPE 8.5", (0.95, "1 × 1 (Pico Neural 95%)", "RPE 9.0-9.5")),
            "bp_main": (0.90, "2 séries × 1 rep", "RPE 8.5", (0.95, "1 × 1 (Pico Neural 95%)", "RPE 9.0-9.5")),
            "dl_main": (0.90, "2 séries × 1 rep", "RPE 8.5", (0.95, "1 × 1 (Pico Neural 95%)", "RPE 9.0-9.5")),
            "bp_pausa": (0.725, "4 séries × 2 reps (Pausa 3s — velocidade total)", "RPE 7.5"),
            "pullup": "3 séries × 3 reps (+10 kg no cinto)",
            "farmer": f"Halteres de {arredondar_carga(farmer + 8.0):.1f} kg (2 × 25 metros — recorde de pegada)",
            "ohp": f"{arredondar_carga(ohp + 5.0):.1f} kg (3 séries × 3 reps)",
            "row": f"{arredondar_carga(bp * 0.825):.1f} kg (3 séries × 3 reps)",
            "curl": "Halteres: 2 × 6 reps (sem fadigar para o próximo treino)",
            "bulg": "Halteres 22 kg (2 × 4 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 1.05):.1f} kg (2 × 4 reps)",
            "dips": "3 séries × 3 a 4 reps (+10 a 12,5 kg no cinto)",
            "core_seg": "Pallof Press: 3 × 15s/lado",
            "core_qui": "Ab Wheel: 3 × 8 reps",
            "core_sex": "Hollow Rock: 3 × 40 segundos"
        },
        8: {
            "titulo": "Semana 8 — Deload Neural & Preparação de Novo Ciclo (70%)",
            "bloco": "CONSOLIDAÇÃO: REGENERAÇÃO DO SNC PARA SUBIR OS 1RMs",
            "foco_tendao": "Supercompensação Final: Conclua esta semana leve e clique em 'Avançar Ciclo' no menu lateral para subir todas as cargas.",
            "sq_main": (0.70, "3 séries × 2 reps", "RPE 5.0", None),
            "bp_main": (0.70, "3 séries × 2 reps", "RPE 5.0", None),
            "dl_main": (0.70, "2 séries × 1 rep", "RPE 5.0", None),
            "bp_pausa": (0.50, "3 séries × 2 reps (Pausa 3s)", "RPE 4.5"),
            "pullup": "2 séries × 4 reps (Peso corporal)",
            "farmer": f"Halteres de {arredondar_carga(farmer * 0.70):.1f} kg (2 × 20 metros)",
            "ohp": f"{arredondar_carga(ohp * 0.70):.1f} kg (2 séries × 5 reps)",
            "row": f"{arredondar_carga(bp * 0.55):.1f} kg (2 séries × 5 reps)",
            "curl": "Halteres leves: 2 × 10 reps",
            "bulg": "Halteres 12 kg (2 × 5 reps/perna)",
            "pelv": f"{arredondar_carga(sq * 0.60):.1f} kg (2 × 5 reps)",
            "dips": "2 séries × 5 reps (Peso corporal)",
            "core_seg": "Pallof Press: 2 × 12s/lado",
            "core_qui": "Prancha RKC: 2 × 20s",
            "core_sex": "Hollow Rock: 2 × 20 segundos"
        }
    }
    return mapa[num_semana]

# -------------------------------------------------------------
# BARRA LATERAL: CONTROLE DE 1RMs E AVANÇO DE CICLO
# -------------------------------------------------------------
with st.sidebar:
    st.markdown(f"### ⚙️ Ajuste de Cargas (Ciclo {st.session_state.ciclo})")
    st.caption("Altere qualquer valor abaixo para recalcular instantaneamente as 8 semanas.")

    novo_barra = st.number_input("Peso da Barra Olímpica (kg)", value=float(st.session_state.barra_kg), step=2.5)
    novo_sq = st.number_input("1RM Agachamento Livre (kg)", value=float(st.session_state.sq_1rm), step=2.5)
    novo_bp = st.number_input("1RM Supino Reto (kg)", value=float(st.session_state.bp_1rm), step=2.5)
    novo_dl = st.number_input("1RM Levantamento Terra (kg)", value=float(st.session_state.dl_1rm), step=2.5)
    novo_ohp = st.number_input("Carga Base Desenv. Militar (kg)", value=float(st.session_state.ohp_base), step=2.5)
    novo_farmer = st.number_input("Halter Base Farmer's Walk (kg)", value=float(st.session_state.farmer_halt), step=2.0)

    # Verifica mudanças e salva automaticamente
    if (novo_barra != st.session_state.barra_kg or novo_sq != st.session_state.sq_1rm or
        novo_bp != st.session_state.bp_1rm or novo_dl != st.session_state.dl_1rm or
        novo_ohp != st.session_state.ohp_base or novo_farmer != st.session_state.farmer_halt):
        st.session_state.barra_kg = novo_barra
        st.session_state.sq_1rm = novo_sq
        st.session_state.bp_1rm = novo_bp
        st.session_state.dl_1rm = novo_dl
        st.session_state.ohp_base = novo_ohp
        st.session_state.farmer_halt = novo_farmer
        salvar_config()

    st.divider()
    st.markdown("#### 🚀 Evolução de Macrociclo")
    st.caption("Ao concluir a Semana 8, avance o ciclo para aplicar a sobrecarga progressiva:")
    if st.button("🔥 Avançar Ciclo (+5kg SQ/DL | +2.5kg BP/OHP)", use_container_width=True):
        st.session_state.ciclo += 1
        st.session_state.semana_atual = 1
        st.session_state.sq_1rm += 5.0
        st.session_state.dl_1rm += 5.0
        st.session_state.bp_1rm += 2.5
        st.session_state.ohp_base += 2.5
        st.session_state.farmer_halt += 2.0
        salvar_config()
        st.success(f"Ciclo {st.session_state.ciclo} iniciado!")
        st.rerun()

    st.divider()
    if st.button("🔒 Terminar Sessão (Sair)", use_container_width=True):
        st.session_state["autenticado"] = False
        st.rerun()

# -------------------------------------------------------------
# CABEÇALHO E PAINEL COMPACTO DE 1RMs (MOBILE-FRIENDLY)
# -------------------------------------------------------------
st.markdown(f"## ⚡ Força Pura & Blindagem de Tendões — Ciclo {st.session_state.ciclo}")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-mini"><div class="label">Agachamento</div><div class="val">{st.session_state.sq_1rm:.1f} kg</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-mini"><div class="label">Supino Reto</div><div class="val">{st.session_state.bp_1rm:.1f} kg</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-mini"><div class="label">Terra (Deadlift)</div><div class="val">{st.session_state.dl_1rm:.1f} kg</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-mini"><div class="label">Militar (OHP)</div><div class="val">{st.session_state.ohp_base:.1f} kg</div></div>', unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------------
# NAVEGAÇÃO PRINCIPAL POR ABAS
# -------------------------------------------------------------
aba_treino, aba_tendoes, aba_projecao, aba_cf = st.tabs([
    "🏋️ Treino do Dia",
    "🧬 Protocolo de Tendões & Colágeno",
    "📈 Projeção de Força (1 Ano)",
    "🏃 CrossFit & Recuperação"
])

# =============================================================
# ABA 1: TREINO DO DIA (8 SEMANAS + FILTRO MOBILE POR DIA)
# =============================================================
with aba_treino:
    col_sem_sel, col_dia_sel = st.columns([1.2, 1.8])
    
    with col_sem_sel:
        opcoes_semanas = [
            "Semana 1 (77.5% - Base & Tendão)",
            "Semana 2 (82.5% - Carga Lenta)",
            "Semana 3 (85.0% - Choque Estrutural)",
            "Semana 4 (65.0% - Deload Tendíneo)",
            "Semana 5 (85% + 90% - Entrada Neural)",
            "Semana 6 (88% + 92.5% - Desinibição OTG)",
            "Semana 7 (90% + 95% - Pico Absoluto)",
            "Semana 8 (70.0% - Supercompensação)"
        ]
        idx_padrao = int(st.session_state.semana_atual) - 1
        sem_escolhida_str = st.selectbox("📅 Escolha a Semana (1 a 8):", opcoes_semanas, index=idx_padrao)
        num_semana = int(sem_escolhida_str.split()[1])
        if num_semana != st.session_state.semana_atual:
            st.session_state.semana_atual = num_semana
            salvar_config()

    with col_dia_sel:
        dia_filtro = st.radio(
            "📱 Selecione o Dia para Focar na Tela:",
            ["Seg (Agacho)", "Ter (Supino)", "Qui (Terra)", "Sex (Potência)", "Ver Todos"],
            horizontal=True
        )

    cfg = obter_dados_semana(
        num_semana,
        st.session_state.sq_1rm,
        st.session_state.bp_1rm,
        st.session_state.dl_1rm,
        st.session_state.ohp_base,
        st.session_state.farmer_halt
    )

    st.markdown(f"**{cfg['bloco']}** — *{cfg['titulo']}*")
    st.info(f"🧬 **Diretriz Biomecânica da Semana:** {cfg['foco_tendao']}")

    # Função auxiliar para renderizar cada dia com visual limpo no celular
    def renderizar_segunda():
        sq_peso = arredondar_carga(st.session_state.sq_1rm * cfg["sq_main"][0])
        st.markdown("### 🦵 Segunda-Feira: Agachamento, Tração & Pegada")
        
        # Card Tendão Pré-Treino
        st.markdown("""
        <div class="tendon-card">
            <span class="badge-tendon">1. Ativação de Tendões (Pré-Barra)</span>
            <p style="margin-top:8px; margin-bottom:4px;"><b>• Nutrição (45m antes):</b> 15g Colágeno Tipo 1 + 100mg Vitamina C</p>
            <p style="margin-bottom:4px;"><b>• Tendão Patelar:</b> Wall Sit (Cadeirinha isométrica a 90°) — 2 × 40 segundos</p>
            <p style="margin-bottom:0px;"><b>• Tendão de Aquiles:</b> Isometria de Panturrilha Unipodal no degrau — 2 × 30s/pé</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔥 Ver Rampagem de Aquecimento do Agachamento", expanded=False):
            st.dataframe(gerar_rampagem("Agachamento", sq_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        # Card Exercício Principal
        single_html = ""
        if cfg["sq_main"][3]:
            sq_single = arredondar_carga(st.session_state.sq_1rm * cfg["sq_main"][3][0])
            single_html = f"""
            <hr style="border-color:#333; margin:10px 0;">
            <span class="badge-main">Single de Pico Neural</span>
            <div class="weight-highlight">{sq_single:.1f} kg — {cfg['sq_main'][3][1]} ({cfg['sq_main'][3][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(sq_single, st.session_state.barra_kg)}</div>
            """

        st.markdown(f"""
        <div class="workout-card">
            <span class="badge-main">2. Levantamento Principal</span>
            <h4 style="margin:6px 0 2px 0;">Agachamento Livre (Back Squat)</h4>
            <div class="weight-highlight">{sq_peso:.1f} kg — {cfg['sq_main'][1]} ({cfg['sq_main'][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(sq_peso, st.session_state.barra_kg)}</div>
            <p style="font-size:0.85rem; color:#94a3b8; margin-top:8px; margin-bottom:0;">⏱️ Descanso: 3 a 5 min | Descida controlada (2-3s), subida explosiva.</p>
            {single_html}
        </div>
        """, unsafe_allow_html=True)

        # Acessórios
        st.markdown(f"""
        <div class="acc-card">
            <span class="badge-acc">3. Dorsais & Cotovelos</span>
            <h5 style="margin:5px 0;">Barra Fixa Pronada (Pull-ups)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['pullup']} | ⏱️ Descanso: 2 min</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">4. Pegada Brutal, Antebraço & Trapézio</span>
            <h5 style="margin:5px 0;">Caminhada do Fazendeiro (Heavy Farmer's Walk)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['farmer']} | Segure com força máxima sem deixar o ombro cair.</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">5. Estabilidade de Core</span>
            <h5 style="margin:5px 0;">{cfg['core_seg']}</h5>
            <p style="margin:0;">Trave glúteos e abdômen resistindo à rotação da polia/elástico.</p>
        </div>
        """, unsafe_allow_html=True)

    def renderizar_terca():
        bp_peso = arredondar_carga(st.session_state.bp_1rm * cfg["bp_main"][0])
        st.markdown("### 💪 Terça-Feira: Supino Força, Ombros & Blindagem de Bíceps")

        st.markdown("""
        <div class="tendon-card">
            <span class="badge-tendon">1. Ativação de Tendões (Pré-Barra)</span>
            <p style="margin-top:8px; margin-bottom:4px;"><b>• Descompressão & Pegada:</b> Dead Hang (Suspensão passiva na barra fixa) — 2 × 35 segundos</p>
            <p style="margin-bottom:0px;"><b>• Manguito Rotador:</b> Rotação externa isométrica com elástico — 2 × 20s segurando no final</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔥 Ver Rampagem de Aquecimento do Supino Reto", expanded=False):
            st.dataframe(gerar_rampagem("Supino Reto", bp_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        single_html = ""
        if cfg["bp_main"][3]:
            bp_single = arredondar_carga(st.session_state.bp_1rm * cfg["bp_main"][3][0])
            single_html = f"""
            <hr style="border-color:#333; margin:10px 0;">
            <span class="badge-main">Single de Pico Neural</span>
            <div class="weight-highlight">{bp_single:.1f} kg — {cfg['bp_main'][3][1]} ({cfg['bp_main'][3][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(bp_single, st.session_state.barra_kg)}</div>
            """

        st.markdown(f"""
        <div class="workout-card">
            <span class="badge-main">2. Levantamento Principal</span>
            <h4 style="margin:6px 0 2px 0;">Supino Reto com Barra (Bench Press)</h4>
            <div class="weight-highlight">{bp_peso:.1f} kg — {cfg['bp_main'][1]} ({cfg['bp_main'][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(bp_peso, st.session_state.barra_kg)}</div>
            <p style="font-size:0.85rem; color:#94a3b8; margin-top:8px; margin-bottom:0;">⏱️ Descanso: 3 a 5 min | Escápulas retraídas e pés cravados no chão.</p>
            {single_html}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="acc-card">
            <span class="badge-acc">3. Força Vertical de Ombros</span>
            <h5 style="margin:5px 0;">Desenvolvimento Militar em Pé (OHP)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['ohp']} | 💿 {calcular_anilhas(float(cfg['ohp'].split()[0]), st.session_state.barra_kg)}</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">4. Tração Horizontal Explosiva</span>
            <h5 style="margin:5px 0;">Pendlay Row (Remada Curvada saindo do chão)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['row']} | 💿 {calcular_anilhas(float(cfg['row'].split()[0]), st.session_state.barra_kg)}</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">5. Blindagem do Tendão Distal do Bíceps</span>
            <h5 style="margin:5px 0;">Rosca Martelo com Halteres (Excêntrica Lenta)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['curl']}</p>
        </div>
        """, unsafe_allow_html=True)

    def renderizar_quinta():
        dl_peso = arredondar_carga(st.session_state.dl_1rm * cfg["dl_main"][0])
        st.markdown("### ⚡ Quinta-Feira: Levantamento Terra & Cadeia Posterior")

        st.markdown("""
        <div class="tendon-card">
            <span class="badge-tendon">1. Ativação de Tendões & Core (Pré-Barra)</span>
            <p style="margin-top:8px; margin-bottom:4px;"><b>• Isquiotibiais Proximais:</b> Ponte de Glúteo Unilateral Isométrica — 2 × 30s por perna</p>
            <p style="margin-bottom:0px;"><b>• Coluna Lombar:</b> Bird-Dog travado (3s no topo) — 2 × 6 reps por lado</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔥 Ver Rampagem de Aquecimento do Levantamento Terra", expanded=False):
            st.dataframe(gerar_rampagem("Levantamento Terra", dl_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        single_html = ""
        if cfg["dl_main"][3]:
            dl_single = arredondar_carga(st.session_state.dl_1rm * cfg["dl_main"][3][0])
            single_html = f"""
            <hr style="border-color:#333; margin:10px 0;">
            <span class="badge-main">Single de Pico Neural</span>
            <div class="weight-highlight">{dl_single:.1f} kg — {cfg['dl_main'][3][1]} ({cfg['dl_main'][3][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(dl_single, st.session_state.barra_kg)}</div>
            """

        st.markdown(f"""
        <div class="workout-card">
            <span class="badge-main">2. Levantamento Principal</span>
            <h4 style="margin:6px 0 2px 0;">Levantamento Terra (Deadlift)</h4>
            <div class="weight-highlight">{dl_peso:.1f} kg — {cfg['dl_main'][1]} ({cfg['dl_main'][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(dl_peso, st.session_state.barra_kg)}</div>
            <p style="font-size:0.85rem; color:#94a3b8; margin-top:8px; margin-bottom:0;">⏱️ Descanso: 4 a 5 min | Pouse a barra no solo a cada repetição (Dead Stop).</p>
            {single_html}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="acc-card">
            <span class="badge-acc">3. Força Unilateral & Estabilidade Pélvica</span>
            <h5 style="margin:5px 0;">Agachamento Búlgaro com Halteres</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['bulg']}</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">4. Bloqueio Final de Quadril (Lockout)</span>
            <h5 style="margin:5px 0;">Elevação Pélvica com Barra (Hip Thrust)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['pelv']} | 💿 {calcular_anilhas(float(cfg['pelv'].split()[0]), st.session_state.barra_kg)}</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">5. Blindagem Anti-Extensão Lombar</span>
            <h5 style="margin:5px 0;">{cfg['core_qui']}</h5>
            <p style="margin:0;">Mantenha costelas fechadas e glúteos contraídos o tempo inteiro.</p>
        </div>
        """, unsafe_allow_html=True)

    def renderizar_sexta():
        bp_pausa_peso = arredondar_carga(st.session_state.bp_1rm * cfg["bp_pausa"][0])
        st.markdown("### 🎯 Sexta-Feira: Supino Pausado (Força de Arrancada) & Tríceps")

        st.markdown("""
        <div class="tendon-card">
            <span class="badge-tendon">1. Preparação de Tendão Peitoral & Tríceps</span>
            <p style="margin-top:8px; margin-bottom:4px;"><b>• Escápulas:</b> Band Pull-Apart — 2 × 15 repetições pausando 1s aberto</p>
            <p style="margin-bottom:0px;"><b>• Cotovelos:</b> Sustentação isométrica no topo das paralelas — 2 × 25 segundos</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔥 Ver Rampagem do Supino Pausado", expanded=False):
            st.dataframe(gerar_rampagem("Supino Pausado", bp_pausa_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="workout-card">
            <span class="badge-main">2. Levantamento Técnico / Taxa de Disparo</span>
            <h4 style="margin:6px 0 2px 0;">Supino Reto com Pausa de 3 Segundos no Peito</h4>
            <div class="weight-highlight">{bp_pausa_peso:.1f} kg — {cfg['bp_pausa'][1]} ({cfg['bp_pausa'][2]})</div>
            <div class="plate-box">💿 Barra: {calcular_anilhas(bp_pausa_peso, st.session_state.barra_kg)}</div>
            <p style="font-size:0.85rem; color:#94a3b8; margin-top:8px; margin-bottom:0;">⏱️ Descanso: 3 min | Conte 1001, 1002, 1003 com a barra imóvel no esterno e exploda!</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="acc-card">
            <span class="badge-acc">3. Força Bruta de Tríceps & Peitoral Inferior</span>
            <h5 style="margin:5px 0;">Paralelas (Weighted Dips)</h5>
            <p style="margin:0;"><b>Prescrição:</b> {cfg['dips']} | ⏱️ Descanso: 2 a 3 min</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">4. Blindagem Posterior de Ombro & Manguito</span>
            <h5 style="margin:5px 0;">Face Pull na Polia Alta (Pausa de 2s atrás)</h5>
            <p style="margin:0;"><b>Prescrição:</b> 3 a 4 séries × 15 reps focando em rotação externa máxima.</p>
        </div>
        <div class="acc-card">
            <span class="badge-acc">5. Tensão Global de Core</span>
            <h5 style="margin:5px 0;">{cfg['core_sex']}</h5>
            <p style="margin:0;">Lombar 100% pressionada contra o solo.</p>
        </div>
        """, unsafe_allow_html=True)

    # Renderização condicional conforme filtro mobile
    if dia_filtro == "Seg (Agacho)":
        renderizar_segunda()
    elif dia_filtro == "Ter (Supino)":
        renderizar_terca()
    elif dia_filtro == "Qui (Terra)":
        renderizar_quinta()
    elif dia_filtro == "Sex (Potência)":
        renderizar_sexta()
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            renderizar_segunda()
            st.divider()
            renderizar_quinta()
        with col_b:
            renderizar_terca()
            st.divider()
            renderizar_sexta()

# =============================================================
# ABA 2: PROTOCOLO DE TENDÕES & SUPLEMENTAÇÃO
# =============================================================
with aba_tendoes:
    st.subheader("🧬 Engenharia de Tendões de Aço (Aos 43+ Anos)")
    st.markdown("""
    Para suportar cargas extremas sem lesões, seus tendões precisam de **subtrato bioquímico** e **deformação mecânica controlada**.
    """)

    c_t1, c_t2 = st.columns(2)
    with c_t1:
        st.markdown("""
        <div class="tendon-card">
            <h4>🥤 1. Janela Bioquímica (45–60 min Pré-Treino)</h4>
            <p>• <b>15g de Colágeno Hidrolisado Tipo 1</b> (ou gelatina sem sabor)</p>
            <p>• <b>100mg de Vitamina C</b> (suco de meio limão ou ácido ascórbico)</p>
            <p>• <b>Redução de Açúcar Refinado:</b> Evita a glicação (AGEs) que resseca e deixa o tendão quebradiço.</p>
        </div>
        """, unsafe_allow_html=True)

    with c_t2:
        st.markdown("""
        <div class="tendon-card">
            <h4>⚙️ 2. As 3 Regras Mecânicas Durante o Treino</h4>
            <p>• <b>Nunca solte o peso (Sem quicar):</b> Desça a barra em 2 a 3s. O controle na frenagem espessa o tendão.</p>
            <p>• <b>Isometrias de 30-45s no Aquecimento:</b> Alinham as fibras de colágeno e geram analgesia articular imediata.</p>
            <p>• <b>Respeite as Semanas 4 e 8 (Deload):</b> O músculo recupera em 48h; o tendão usa a semana leve para cicatrizar microfissuras.</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================
# ABA 3: SIMULADOR DE PROJEÇÃO DE FORÇA (1 ANO)
# =============================================================
with aba_projecao:
    st.subheader("📈 Projeção Matemática de Força (6 Macrociclos de 8 Semanas)")
    st.caption("Considerando a progressão limpa de +5 kg no Agachamento/Terra e +2,5 kg no Supino/Militar a cada bloco de 8 semanas concluído:")

    linhas_proj = []
    for c in range(0, 7):
        ciclo_num = st.session_state.ciclo + c
        meses = c * 2
        sq_proj = st.session_state.sq_1rm + (c * 5.0)
        bp_proj = st.session_state.bp_1rm + (c * 2.5)
        dl_proj = st.session_state.dl_1rm + (c * 5.0)
        ohp_proj = st.session_state.ohp_base + (c * 2.5)
        total_pl = sq_proj + bp_proj + dl_proj
        linhas_proj.append({
            "Macrociclo": f"Ciclo {ciclo_num}" + (" (Atual)" if c == 0 else f" (+{meses} meses)"),
            "Agachamento (1RM)": f"{sq_proj:.1f} kg",
            "Supino Reto (1RM)": f"{bp_proj:.1f} kg",
            "Levantamento Terra (1RM)": f"{dl_proj:.1f} kg",
            "Desenv. Militar (Base)": f"{ohp_proj:.1f} kg",
            "Total Powerlifting": f"{total_pl:.1f} kg"
        })
    st.dataframe(pd.DataFrame(linhas_proj), use_container_width=True, hide_index=True)

# =============================================================
# ABA 4: INTEGRAÇÃO COM CROSSFIT & RECUPERAÇÃO
# =============================================================
with aba_cf:
    st.subheader("🏃 Como Usar o CrossFit a Favor da Força Bruta")
    col_cf1, col_cf2 = st.columns(2)
    with col_cf1:
        st.markdown("""
        <div class="acc-card">
            <h4>🫁 Quarta-Feira: Flushing Aeróbico (Zona 2)</h4>
            <p>• <b>Frequência Cardíaca:</b> Ritmo conversacional (RPE 6).</p>
            <p>• <b>Cargas:</b> Máximo 30% a 40% do 1RM ou kettlebells leves.</p>
            <p>• <b>Função fisiológica:</b> Aumentar capilarização sanguínea para acelerar a ressíntese de ATP-CP entre as séries pesadas de quinta e sexta.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_cf2:
        st.markdown("""
        <div class="acc-card">
            <h4>⚡ Sábado: Condicionamento Geral & Mobilidade</h4>
            <p>• <b>Regra de Ouro:</b> Pare qualquer série antes da falha concêntrica.</p>
            <p>• <b>Evite:</b> Alto volume de LPO pesado ou saltos em profundidade excessivos para poupar o tendão patelar e lombar.</p>
            <p>• <b>Domingo:</b> Descanso absoluto do Sistema Nervoso Central.</p>
        </div>
        """, unsafe_allow_html=True)
