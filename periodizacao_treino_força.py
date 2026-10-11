import streamlit as st
import pandas as pd
import math

# Configuração da página para visualização otimizada em smartphones
st.set_page_config(
    page_title="Força & Adaptação Neural",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funções utilitárias
def arredondar_carga(peso, passo=2.5):
    """Arredonda para o passo mínimo de anilhas (2.5 kg)."""
    return round(peso / passo) * passo

def calcular_anilhas(peso_total, barra=20.0):
    """Retorna a combinação de anilhas por lado."""
    if peso_total <= barra:
        return "Barra vazia"
    
    peso_lado = (peso_total - barra) / 2.0
    anilhas = [25.0, 20.0, 15.0, 10.0, 5.0, 2.5, 1.25]
    resultado = []
    restante = peso_lado
    
    for anilha in anilhas:
        qtd = int(restante // anilha)
        if qtd > 0:
            resultado.append(f"{qtd}x {anilha:g}kg")
            restante = round(restante - (qtd * anilha), 2)
            
    return " + ".join(resultado) + " / lado"

def gerar_rampagem(nome, carga_alvo, barra=20.0):
    """Gera tabela com séries de aquecimento e ativação neural (PAP)."""
    if "terra" in nome.lower() or "deadlift" in nome.lower():
        p1 = max(60.0, arredondar_carga(carga_alvo * 0.50))
        p2 = arredondar_carga(carga_alvo * 0.70)
        p3 = arredondar_carga(carga_alvo * 0.85)
        p4 = arredondar_carga(carga_alvo * 0.92)
        etapas = [
            {"Série": "Aquecimento 1", "Carga": f"{p1:.1f} kg", "Reps": "5 reps", "Anilhas": calcular_anilhas(p1, barra), "Foco": "Altura oficial / ritmo fluido"},
            {"Série": "Aquecimento 2", "Carga": f"{p2:.1f} kg", "Reps": "3 reps", "Anilhas": calcular_anilhas(p2, barra), "Foco": "Aceleração concêntrica"},
            {"Série": "Aproximação", "Carga": f"{p3:.1f} kg", "Reps": "2 reps", "Anilhas": calcular_anilhas(p3, barra), "Foco": "Pressão intra-abdominal (Bracing)"},
            {"Série": "Single Neural (PAP)", "Carga": f"{p4:.1f} kg", "Reps": "1 rep", "Anilhas": calcular_anilhas(p4, barra), "Foco": "Sentir a densidade da carga"}
        ]
    else:
        p1 = arredondar_carga(carga_alvo * 0.50)
        p2 = arredondar_carga(carga_alvo * 0.70)
        p3 = arredondar_carga(carga_alvo * 0.88)
        etapas = [
            {"Série": "Barra Vazia", "Carga": f"{barra:.1f} kg", "Reps": "2x 5-8 reps", "Anilhas": "Barra vazia", "Foco": "Amplitude articular profunda"},
            {"Série": "Aquecimento", "Carga": f"{p1:.1f} kg", "Reps": "5 reps", "Anilhas": calcular_anilhas(p1, barra), "Foco": "Ritmo e posicionamento"},
            {"Série": "Aproximação", "Carga": f"{p2:.1f} kg", "Reps": "3 reps", "Anilhas": calcular_anilhas(p2, barra), "Foco": "Velocidade concêntrica máxima (CAT)"},
            {"Série": "Single Neural (PAP)", "Carga": f"{p3:.1f} kg", "Reps": "1 rep", "Anilhas": calcular_anilhas(p3, barra), "Foco": "Ativação de alto limiar"}
        ]
    return pd.DataFrame(etapas)

# Estado inicial da sessão
if "ciclo" not in st.session_state:
    st.session_state.ciclo = 1
if "sq_1rm" not in st.session_state:
    st.session_state.sq_1rm = 90.0
if "bp_1rm" not in st.session_state:
    st.session_state.bp_1rm = 80.0
if "dl_1rm" not in st.session_state:
    st.session_state.dl_1rm = 140.0
if "ohp_base" not in st.session_state:
    st.session_state.ohp_base = 45.0
if "barra_kg" not in st.session_state:
    st.session_state.barra_kg = 20.0

# Barra Lateral: Configurações de Carga
with st.sidebar:
    st.header(f"⚙️ Configurações (Ciclo {st.session_state.ciclo})")
    
    st.session_state.barra_kg = st.number_input("Peso da Barra (kg)", value=float(st.session_state.barra_kg), step=2.5)
    st.session_state.sq_1rm = st.number_input("1RM Agachamento (Back Squat)", value=float(st.session_state.sq_1rm), step=2.5)
    st.session_state.bp_1rm = st.number_input("1RM Supino Reto (Bench Press)", value=float(st.session_state.bp_1rm), step=2.5)
    st.session_state.dl_1rm = st.number_input("1RM Levantamento Terra (Deadlift)", value=float(st.session_state.dl_1rm), step=2.5)
    st.session_state.ohp_base = st.number_input("Base Desenv. Militar (OHP)", value=float(st.session_state.ohp_base), step=2.5)
    
    st.divider()
    
    if st.button("🚀 Avançar Ciclo (+5kg Terra/Agacho, +2.5kg Supino/OHP)", use_container_width=True):
        st.session_state.ciclo += 1
        st.session_state.sq_1rm += 5.0
        st.session_state.dl_1rm += 5.0
        st.session_state.bp_1rm += 2.5
        st.session_state.ohp_base += 2.5
        st.success(f"Ciclo {st.session_state.ciclo} iniciado com novas cargas de referência!")
        st.rerun()

# Interface Principal
st.title("🏋️ Treinamento de Força Pura & Adaptação Neural")
st.caption(f"Ciclo Ativo: {st.session_state.ciclo} | Barra: {st.session_state.barra_kg:.1f} kg | Sistema de Arredondamento Automático para Anilhas")

# Métricas no topo
col1, col2, col3, col4 = st.columns(4)
col1.metric("1RM Agachamento", f"{st.session_state.sq_1rm:.1f} kg")
col2.metric("1RM Supino", f"{st.session_state.bp_1rm:.1f} kg")
col3.metric("1RM Terra", f"{st.session_state.dl_1rm:.1f} kg")
col4.metric("Base OHP", f"{st.session_state.ohp_base:.1f} kg")

st.divider()

# Abas de Navegação
aba_semanas, aba_rampagem, aba_crossfit = st.tabs(["📅 Semanas do Bloco", "🔥 Calculadora de Rampagem", "🏃 CrossFit & Recuperação"])

with aba_semanas:
    semana_sel = st.radio("Selecione a Semana:", ["Semana 1 (80% - Acumulação)", "Semana 2 (85% - Intensificação)", "Semana 3 (88%/92% - Pico)", "Semana 4 (70% - Deload)"], horizontal=True)
    num_semana = int(semana_sel.split()[1])

    # Parâmetros de cada semana
    configs = {
        1: {
            "sq": (0.80, "4 × 3", "7 – 7.5"), "bp": (0.80, "5 × 3", "7.5"), "dl": (0.80, "3 × 3", "7 – 7.5"),
            "bp_p": (0.65, "4 × 3 (3s pausa)", "6.5"),
            "pullup": "3 × 4 (Peso corporal)", "ohp": f"{arredondar_carga(st.session_state.ohp_base):.1f} kg (3 × 5)",
            "row": f"{arredondar_carga(st.session_state.bp_1rm * 0.75):.1f} kg (3 × 5)", "bulg": "Halteres 16 kg (3 × 5/perna)",
            "pelv": f"{arredondar_carga(st.session_state.sq_1rm * 0.90):.1f} kg (3 × 6)", "dips": "3 × 5 (Peso corporal)",
            "core_seg": "Pallof Press: 3 × 12s/lado", "core_sex": "Hollow Rock Estático: 3 × 30s"
        },
        2: {
            "sq": (0.85, "4 × 2", "8.0"), "bp": (0.85, "4 × 2", "8.0"), "dl": (0.85, "3 × 2", "8.0"),
            "bp_p": (0.65, "4 × 3 (3s pausa)", "7.0"),
            "pullup": "3 × 5 (Peso corporal, +1 rep)", "ohp": f"{arredondar_carga(st.session_state.ohp_base + 2.5):.1f} kg (3 × 5)",
            "row": f"{arredondar_carga((st.session_state.bp_1rm * 0.75) + 2.5):.1f} kg (3 × 5)", "bulg": "Halteres 18 kg (3 × 5/perna)",
            "pelv": f"{arredondar_carga((st.session_state.sq_1rm * 0.90) + 5.0):.1f} kg (3 × 6)", "dips": "+2.5 a 5 kg cinto (3 × 5)",
            "core_seg": "Pallof Press: 3 × 15s/lado", "core_sex": "Hollow Rock Estático: 3 × 35s"
        },
        3: {
            "sq": (0.88, "3 × 2", "8.5", 0.92, "1 × 1 (Single)", "9.0"),
            "bp": (0.88, "3 × 2", "8.5", 0.92, "1 × 1 (Single)", "9.0"),
            "dl": (0.88, "2 × 2", "8.5", 0.93, "1 × 1 (Single)", "9.0"),
            "bp_p": (0.70, "5 × 2 (3s pausa)", "7.0"),
            "pullup": "+2.5 a 5 kg cinto (4 × 4)", "ohp": f"{arredondar_carga(st.session_state.ohp_base + 5.0):.1f} kg (3 × 4)",
            "row": f"{arredondar_carga((st.session_state.bp_1rm * 0.75) + 5.0):.1f} kg (3 × 4)", "bulg": "Halteres 20 kg (3 × 5/perna)",
            "pelv": f"{arredondar_carga((st.session_state.sq_1rm * 0.90) + 10.0):.1f} kg (3 × 5)", "dips": "+7.5 kg cinto (3 × 4-5)",
            "core_seg": "Pallof Press: 3 × 15s/lado (carga max)", "core_sex": "Hollow Rock Estático: 3 × 40s"
        },
        4: {
            "sq": (0.70, "3 × 2", "5.0"), "bp": (0.70, "3 × 2", "5.0"), "dl": (0.70, "2 × 1", "5.0"),
            "bp_p": (0.50, "3 × 2 (3s pausa)", "4.5"),
            "pullup": "2 × 4 (Peso corporal)", "ohp": f"{arredondar_carga(st.session_state.ohp_base * 0.75):.1f} kg (2 × 5)",
            "row": f"{arredondar_carga((st.session_state.bp_1rm * 0.75) * 0.75):.1f} kg (2 × 5)", "bulg": "Halteres 12 kg (2 × 5/perna)",
            "pelv": f"{arredondar_carga(st.session_state.sq_1rm * 0.65):.1f} kg (2 × 5)", "dips": "2 × 5 (Peso corporal)",
            "core_seg": "Pallof Press: 2 × 12s/lado", "core_sex": "Hollow Rock Estático: 2 × 20s"
        }
    }
    
    cfg = configs[num_semana]
    
    # Grid de 4 dias de treino
    d_seg, d_ter = st.columns(2)
    d_qui, d_sex = st.columns(2)
    
    with d_seg:
        st.subheader("🏋️ Segunda: Força de Agachamento")
        sq_p = arredondar_carga(st.session_state.sq_1rm * cfg["sq"][0])
        st.markdown(f"**Principal:** Agachamento Livre — **{sq_p:.1f} kg** ({cfg['sq'][1]} @ RPE {cfg['sq'][2]})")
        st.caption(f"👉 Anilhas: {calcular_anilhas(sq_p, st.session_state.barra_kg)}")
        if num_semana == 3:
            sq_s = arredondar_carga(st.session_state.sq_1rm * cfg["sq"][3])
            st.markdown(f"**Single de Pico:** **{sq_s:.1f} kg** (1 × 1 @ RPE 9.0)")
            st.caption(f"👉 Anilhas: {calcular_anilhas(sq_s, st.session_state.barra_kg)}")
        st.markdown(f"• **Acessório:** Barra Fixa Pronada: {cfg['pullup']}")
        st.markdown(f"• **Core:** {cfg['core_seg']}")
        st.info("Descanso nos principais: 3 a 5 minutos completos.")

    with d_ter:
        st.subheader("💪 Terça: Força de Supino")
        bp_p = arredondar_carga(st.session_state.bp_1rm * cfg["bp"][0])
        st.markdown(f"**Principal:** Supino Reto — **{bp_p:.1f} kg** ({cfg['bp'][1]} @ RPE {cfg['bp'][2]})")
        st.caption(f"👉 Anilhas: {calcular_anilhas(bp_p, st.session_state.barra_kg)}")
        if num_semana == 3:
            bp_s = arredondar_carga(st.session_state.bp_1rm * cfg["bp"][3])
            st.markdown(f"**Single de Pico:** **{bp_s:.1f} kg** (1 × 1 @ RPE 9.0)")
            st.caption(f"👉 Anilhas: {calcular_anilhas(bp_s, st.session_state.barra_kg)}")
        st.markdown(f"• **Acessório 1:** Desenv. Militar: {cfg['ohp']}")
        st.markdown(f"• **Acessório 2:** Pendlay Row: {cfg['row']}")
        st.info("Foco concêntrico: velocidade máxima na subida.")

    with d_qui:
        st.subheader("⚡ Quinta: Força de Levantamento Terra")
        dl_p = arredondar_carga(st.session_state.dl_1rm * cfg["dl"][0])
        st.markdown(f"**Principal:** Levantamento Terra — **{dl_p:.1f} kg** ({cfg['dl'][1]} @ RPE {cfg['dl'][2]})")
        st.caption(f"👉 Anilhas: {calcular_anilhas(dl_p, st.session_state.barra_kg)}")
        if num_semana == 3:
            dl_s = arredondar_carga(st.session_state.dl_1rm * cfg["dl"][3])
            st.markdown(f"**Single de Pico:** **{dl_s:.1f} kg** (1 × 1 @ RPE 9.0)")
            st.caption(f"👉 Anilhas: {calcular_anilhas(dl_s, st.session_state.barra_kg)}")
        st.markdown(f"• **Acessório 1:** Agachamento Búlgaro: {cfg['bulg']}")
        st.markdown(f"• **Acessório 2:** Elevação Pélvica: {cfg['pelv']}")
        st.info("Zere a energia elástica a cada repetição no chão.")

    with d_sex:
        st.subheader("🎯 Sexta: Supino Técnica & Potência")
        bp_tec = arredondar_carga(st.session_state.bp_1rm * cfg["bp_p"][0])
        st.markdown(f"**Principal:** Supino Pausado (3s no peito) — **{bp_tec:.1f} kg** ({cfg['bp_p'][1]} @ RPE {cfg['bp_p'][2]})")
        st.caption(f"👉 Anilhas: {calcular_anilhas(bp_tec, st.session_state.barra_kg)}")
        st.markdown(f"• **Acessório 1:** Paralelas (Dips): {cfg['dips']}")
        st.markdown(f"• **Acessório 2:** Face Pull Polia Alta: 3 × 15 reps")
        st.markdown(f"• **Core:** {cfg['core_sex']}")
        st.info("Pausa estrita tocando a camiseta sem afundar a caixa torácica.")

with aba_rampagem:
    st.subheader("🔥 Protocolo de Rampagem (Aquecimento e Potenciação)")
    st.markdown("Execute antes da 1ª série de trabalho oficial. Acelera o disparo do SNC sem gerar fadiga lática.")
    
    col_ex, col_sem = st.columns(2)
    with col_ex:
        ex_sel = st.selectbox("Exercício Principal:", ["Agachamento Livre", "Supino Reto", "Levantamento Terra"])
    with col_sem:
        sem_ramp = st.selectbox("Semana do Treino:", [1, 2, 3, 4], format_func=lambda x: f"Semana {x}")
        
    pct_map = {1: 0.80, 2: 0.85, 3: 0.88, 4: 0.70}
    if ex_sel == "Agachamento Livre":
        carga_trabalho = arredondar_carga(st.session_state.sq_1rm * pct_map[sem_ramp])
    elif ex_sel == "Supino Reto":
        carga_trabalho = arredondar_carga(st.session_state.bp_1rm * pct_map[sem_ramp])
    else:
        carga_trabalho = arredondar_carga(st.session_state.dl_1rm * pct_map[sem_ramp])
        
    st.markdown(f"**Carga Alvo de Trabalho do Dia:** `{carga_trabalho:.1f} kg`")
    df_rampagem = gerar_rampagem(ex_sel, carga_trabalho, st.session_state.barra_kg)
    st.dataframe(df_rampagem, use_container_width=True, hide_index=True)
    st.caption("⏱️ Ao finalizar a Single Neural, descanse de 2 a 3 minutos antes da 1ª série de trabalho.")

with aba_crossfit:
    st.subheader("🏃 Integração com CrossFit & Recuperação")
    
    col_cf1, col_cf2 = st.columns(2)
    with col_cf1:
        st.markdown("### Quarta-feira: Aeróbico / Flushing")
        st.write("• **Intensidade:** Zona 2 estrita (FC ~65-75% da máx / RPE 6).")
        st.write("• **Cargas na barra:** Máximo 30% a 40% do 1RM ou apenas halteres/kettlebells leves.")
        st.write("• **Movimentos ideais:** Remo, Bike ergométrica, SkiErg, corrida leve e sustentação corporal.")
        st.write("• **Proibido:** Thrusters pesados, Deadlifts pesados ou repetições até a falha.")
        
    with col_cf2:
        st.markdown("### Sábado: MetCon Leve / Dinâmico")
        st.write("• **Objetivo:** Trabalho de mobilidade dinâmica e condicionamento geral.")
        st.write("• **Regra:** Pare a cada série antes de perder a velocidade mecânica dos movimentos.")
        st.write("• **Domingo:** Descanso absoluto para recuperação total dos estoques neurais e tecidos conectivos.")