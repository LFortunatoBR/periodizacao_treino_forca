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
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }
    .workout-card {
        background-color: #1a1c24;
        border: 1px solid #2d313e;
        border-left: 5px solid #ff4b4b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 6px;
        color: #f0f2f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.25);
    }
    .tendon-card {
        background-color: #132226;
        border: 1px solid #1f444c;
        border-left: 5px solid #00d4ff;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 6px;
        color: #e6f9ff;
    }
    .acc-card {
        background-color: #181920;
        border: 1px solid #2b2d38;
        border-left: 5px solid #10b981;
        border-radius: 10px;
        padding: 13px;
        margin-bottom: 6px;
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
        display: inline-block;
    }
    .badge-peak {
        background-color: #f59e0b;
        color: #111827;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    .badge-tendon {
        background-color: #00d4ff;
        color: #001f26;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-acc {
        background-color: #10b981;
        color: #022c22;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .weight-highlight {
        font-size: 1.5rem;
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
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .metric-mini .val {
        font-size: 1.2rem;
        font-weight: 800;
        color: #f8fafc;
    }
    .stButton > button {
        min-height: 42px;
        font-weight: 600;
        border-radius: 9px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# BANCO VISUAL DE EXERCÍCIOS (FOTOS + DIAGRAMA SVG + BIOMECÂNICA)
# -------------------------------------------------------------
BASE_IMG_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises"

def gerar_svg_biomecanico(tipo):
    """Gera uma ilustração vetorial animada (SVG) sem recuo excessivo."""
    svgs = {
        "squat": (
            '<svg viewBox="0 0 260 180" width="100%" height="170" style="background:#11141c; border-radius:10px; border:1px solid #2d3748;">'
            '<style>@keyframes squatMove { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(28px); } } .lifter { animation: squatMove 3.5s infinite ease-in-out; }</style>'
            '<text x="12" y="22" fill="#94a3b8" font-size="11" font-family="sans-serif">VETOR AXIAL &amp; TENDÃO PATELAR (AZUL)</text>'
            '<line x1="30" y1="155" x2="230" y2="155" stroke="#475569" stroke-width="3"/>'
            '<g class="lifter">'
            '<line x1="75" y1="55" x2="185" y2="55" stroke="#ff9f1c" stroke-width="5"/>'
            '<rect x="82" y="42" width="10" height="26" fill="#ff4b4b" rx="2"/>'
            '<rect x="168" y="42" width="10" height="26" fill="#ff4b4b" rx="2"/>'
            '<circle cx="130" cy="40" r="10" fill="#e2e8f0"/>'
            '<line x1="130" y1="52" x2="115" y2="100" stroke="#e2e8f0" stroke-width="6" stroke-linecap="round"/>'
            '<line x1="115" y1="100" x2="148" y2="118" stroke="#cbd5e1" stroke-width="6" stroke-linecap="round"/>'
            '<circle cx="148" cy="118" r="6" fill="#00d4ff"/>'
            '</g>'
            '<line x1="148" y1="132" x2="135" y2="155" stroke="#94a3b8" stroke-width="5" stroke-linecap="round"/>'
            '<text x="158" y="135" fill="#00d4ff" font-size="10" font-weight="bold" font-family="sans-serif">← Tendão Patelar</text>'
            '</svg>'
        ),
        "bench": (
            '<svg viewBox="0 0 260 180" width="100%" height="170" style="background:#11141c; border-radius:10px; border:1px solid #2d3748;">'
            '<style>@keyframes benchMove { 0%, 100% { transform: translateY(0px); } 45%, 65% { transform: translateY(32px); } } .barbell { animation: benchMove 4s infinite ease-in-out; }</style>'
            '<text x="12" y="22" fill="#94a3b8" font-size="11" font-family="sans-serif">PAUSA NO ESTERNO &amp; TENDÃO PEITORAL/TRÍCEPS</text>'
            '<rect x="55" y="115" width="140" height="10" fill="#475569" rx="3"/>'
            '<line x1="75" y1="125" x2="75" y2="160" stroke="#475569" stroke-width="5"/>'
            '<line x1="175" y1="125" x2="175" y2="160" stroke="#475569" stroke-width="5"/>'
            '<path d="M 75 110 Q 120 95 160 112" stroke="#e2e8f0" stroke-width="10" fill="none" stroke-linecap="round"/>'
            '<circle cx="65" cy="108" r="9" fill="#e2e8f0"/>'
            '<circle cx="105" cy="104" r="6" fill="#00d4ff"/>'
            '<g class="barbell">'
            '<line x1="105" y1="60" x2="105" y2="95" stroke="#00d4ff" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="105" cy="55" r="14" fill="#ff4b4b" stroke="#ff9f1c" stroke-width="3"/>'
            '</g>'
            '<text x="128" y="88" fill="#00d4ff" font-size="10" font-weight="bold" font-family="sans-serif">← Pausa no Peito (0 impulso)</text>'
            '</svg>'
        ),
        "deadlift": (
            '<svg viewBox="0 0 260 180" width="100%" height="170" style="background:#11141c; border-radius:10px; border:1px solid #2d3748;">'
            '<style>@keyframes dlMove { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-30px); } } .pull { animation: dlMove 3.5s infinite ease-in-out; }</style>'
            '<text x="12" y="22" fill="#94a3b8" font-size="11" font-family="sans-serif">CUNHA DE QUADRIL &amp; CADEIA POSTERIOR</text>'
            '<line x1="30" y1="155" x2="230" y2="155" stroke="#475569" stroke-width="3"/>'
            '<line x1="125" y1="155" x2="125" y2="118" stroke="#cbd5e1" stroke-width="6"/>'
            '<g class="pull">'
            '<circle cx="100" cy="100" r="6" fill="#00d4ff"/>'
            '<line x1="100" y1="100" x2="142" y2="62" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>'
            '<circle cx="150" cy="52" r="9" fill="#e2e8f0"/>'
            '<line x1="138" y1="68" x2="132" y2="132" stroke="#00d4ff" stroke-width="4"/>'
            '<circle cx="132" cy="132" r="20" fill="#ff4b4b" stroke="#ff9f1c" stroke-width="3"/>'
            '</g>'
            '<text x="158" y="105" fill="#00d4ff" font-size="10" font-weight="bold" font-family="sans-serif">← Barra colada na canela</text>'
            '</svg>'
        ),
        "default": (
            '<svg viewBox="0 0 260 160" width="100%" height="150" style="background:#11141c; border-radius:10px; border:1px solid #2d3748;">'
            '<text x="15" y="28" fill="#00d4ff" font-size="12" font-weight="bold" font-family="sans-serif">CONTROLE EXCÊNTRICO &amp; TENSÃO TENDÍNEA</text>'
            '<rect x="25" y="55" width="210" height="18" rx="9" fill="#1e293b"/>'
            '<rect x="25" y="55" width="165" height="18" rx="9" fill="#00d4ff"/>'
            '<text x="25" y="95" fill="#e2e8f0" font-size="11" font-family="sans-serif">• Descida controlada (2 a 3s): Remodela colágeno Tipo 1</text>'
            '<text x="25" y="118" fill="#ff9f1c" font-size="11" font-family="sans-serif">• Subida explosiva (CAT): Máximo recrutamento motor</text>'
            '<text x="25" y="140" fill="#10b981" font-size="11" font-family="sans-serif">• Estabilidade articular: Sem compensação lombar</text>'
            '</svg>'
        )
    }
    return svgs.get(tipo, svgs["default"])

CATALOGO_EXERCICIOS = {
    "Agachamento Livre": {
        "titulo": "Agachamento Livre com Barra (Back Squat)",
        "imgs": [f"{BASE_IMG_URL}/Barbell_Full_Squat/0.jpg", f"{BASE_IMG_URL}/Barbell_Full_Squat/1.jpg"],
        "svg": "squat",
        "musculos": "Quadríceps, Glúteos, Eretores da Espinha, Adutores",
        "tendoes": "Tendão Patelar, Tendão Quadricipital e Tendão de Aquiles",
        "execucao": [
            "Apoie a barra no trapézio denso (crie uma 'prateleira' puxando os cotovelos para baixo e para trás).",
            "Inspire fundo na barriga (360° Bracing) e trave o abdômen antes de destravar os joelhos.",
            "Desça em 2 a 3 segundos controlados até a linha do quadril romper o paralelo dos joelhos.",
            "Empurre o chão com o pé inteiro (tripé plantar) acelerando o máximo possível na subida."
        ],
        "erro_fatal": "Deixar os joelhos colapsarem para dentro (valgo dinâmico) ou perder a tensão quicando no fundo."
    },
    "Supino Reto": {
        "titulo": "Supino Reto Olímpico (Bench Press)",
        "imgs": [f"{BASE_IMG_URL}/Barbell_Bench_Press_-_Medium_Grip/0.jpg", f"{BASE_IMG_URL}/Barbell_Bench_Press_-_Medium_Grip/1.jpg"],
        "svg": "bench",
        "musculos": "Peitoral Maior, Tríceps Braquial, Deltoide Anterior",
        "tendoes": "Tendão do Peitoral Maior (inserção umeral), Tendão do Tríceps e Manguito Rotador",
        "execucao": [
            "Retraia e deprima as escápulas contra o banco ('guarde as escápulas no bolso de trás da calça').",
            "Crave os pés inteiros no chão gerando tensão contínua das pernas até o tronco (Leg Drive).",
            "Desça a barra controladamente até tocar a linha inferior do esterno (antebraços verticais).",
            "Empurre de forma explosiva em leve diagonal de volta para a linha dos olhos."
        ],
        "erro_fatal": "Abrir os cotovelos a 90° em relação ao tronco (sobrecarrega o tendão do supraespinhal) ou tirar o glúteo do banco."
    },
    "Supino Pausado": {
        "titulo": "Supino Reto com Pausa Estrita de 3s no Peito",
        "imgs": [f"{BASE_IMG_URL}/Barbell_Bench_Press_-_Medium_Grip/0.jpg", f"{BASE_IMG_URL}/Barbell_Bench_Press_-_Medium_Grip/1.jpg"],
        "svg": "bench",
        "musculos": "Peitoral Maior, Tríceps, Estabilizadores Escapulares",
        "tendoes": "Junção Miotendínea Peitoral e Tendão Distal do Tríceps",
        "execucao": [
            "Desça a barra em 2 segundos e encoste-a no esterno sem relaxar os braços.",
            "Conte 3 segundos reais ('1001, 1002, 1003') mantendo o peito alto e o corpo inteiro rígido.",
            "A pausa dissipa 100% do reflexo elástico dos tendões, obrigando o cérebro a disparar força pura da estaca zero.",
            "Ao final do 3º segundo, dispare a barra para cima na velocidade máxima."
        ],
        "erro_fatal": "Afundar a barra na caixa torácica para pegar impulso na subida."
    },
    "Levantamento Terra": {
        "titulo": "Levantamento Terra (Deadlift)",
        "imgs": [f"{BASE_IMG_URL}/Barbell_Deadlift/0.jpg", f"{BASE_IMG_URL}/Barbell_Deadlift/1.jpg"],
        "svg": "deadlift",
        "musculos": "Glúteos, Isquiotibiais, Eretores da Espinha, Grande Dorsal, Trapézio e Antebraços",
        "tendoes": "Tendão Proximal dos Isquiotibiais, Fáscia Toracolombar e Tendões Flexores dos Dedos",
        "execucao": [
            "Aproxime a canela a 2 cm da barra (a barra fica exatamente sobre o meio do pé).",
            "Segure a barra com os braços retos por fora dos joelhos e 'tire a folga da barra' (puxe 1 mm até ouvir o clique do ferro).",
            "Acione as dorsais ('proteja as axilas') e empurre o chão com as pernas enquanto estende o quadril.",
            "Pouse a barra no chão a cada repetição (Dead Stop) para zerar o impulso elástico."
        ],
        "erro_fatal": "Dar um tranco na barra com os cotovelos dobrados (risco direto ao tendão distal do bíceps) ou arredondar a lombar."
    },
    "Barra Fixa Pronada": {
        "titulo": "Barra Fixa Pronada (Pull-ups)",
        "imgs": [f"{BASE_IMG_URL}/Pullups/0.jpg", f"{BASE_IMG_URL}/Pullups/1.jpg"],
        "svg": "default",
        "musculos": "Grande Dorsal, Redondo Maior, Bíceps, Braquiorradial e Core",
        "tendoes": "Tendões Flexores do Cotovelo e Tendão do Grande Dorsal",
        "execucao": [
            "Segure a barra com pegada pronada um pouco mais larga que os ombros.",
            "Inicie o movimento deprimindo as escápulas (afaste os ombros das orelhas).",
            "Puxe o peito em direção à barra até o queixo ultrapassar a linha horizontal.",
            "Desça de forma controlada em 2 a 3 segundos até estender os braços mantendo os ombros ativos."
        ],
        "erro_fatal": "Balançar as pernas (kipping) no treino de força pura ou encurtar a descida."
    },
    "Farmer's Walk": {
        "titulo": "Caminhada do Fazendeiro Pesada (Heavy Farmer's Walk)",
        "imgs": [f"{BASE_IMG_URL}/Farmers_Walk/0.jpg", f"{BASE_IMG_URL}/Farmers_Walk/1.jpg"],
        "svg": "default",
        "musculos": "Flexores do Antebraço, Trapézio Superior/Médio, Oblíquos, Quadrado Lombar e Glúteo Médio",
        "tendoes": "Tendões Flexores Profundos do Punho/Dedos e Ligamentos Glenoumerais",
        "execucao": [
            "Retire os halteres pesados do chão agachando com a coluna neutra.",
            "Estufe o peito, mantenha os ombros levemente para trás e o olhar fixo no horizonte.",
            "Caminhe com passos curtos, rápidos e firmes evitando que o tronco balance para os lados.",
            "Esmague a manopla do halter com força máxima durante todo o percurso."
        ],
        "erro_fatal": "Deixar os ombros despencarem para a frente ou dar passadas muito longas."
    },
    "Desenvolvimento Militar": {
        "titulo": "Desenvolvimento Militar em Pé com Barra (Overhead Press)",
        "imgs": [f"{BASE_IMG_URL}/Barbell_Shoulder_Press/0.jpg", f"{BASE_IMG_URL}/Barbell_Shoulder_Press/1.jpg"],
        "svg": "default",
        "musculos": "Deltoide Anterior e Lateral, Tríceps, Trapézio, Serrátil Anterior e Core",
        "tendoes": "Tendões do Manguito Rotador e Tendão do Tríceps",
        "execucao": [
            "Em pé, contraia fortemente os glúteos e o abdômen para blindar a lombar.",
            "Apoie a barra na parte alta do peitoral/clavículas com os antebraços verticais vistos de frente.",
            "Empurre a barra verticalmente passando rente ao queixo e encaixe a cabeça levemente à frente quando a barra passar da testa.",
            "Desça controlando o peso de volta até tocar a clavícula."
        ],
        "erro_fatal": "Jogar o tronco excessivamente para trás transformando o movimento em um supino inclinado em pé."
    },
    "Pendlay Row": {
        "titulo": "Remada Curvada Explosiva (Pendlay Row)",
        "imgs": [f"{BASE_IMG_URL}/Bent_Over_Barbell_Row/0.jpg", f"{BASE_IMG_URL}/Bent_Over_Barbell_Row/1.jpg"],
        "svg": "default",
        "musculos": "Dorsais, Romboides, Trapézio Médio/Inferior, Eretores da Espinha e Posterior de Ombro",
        "tendoes": "Inserções Escapulares, Fáscia Toracolombar e Tendão Braquiorradial",
        "execucao": [
            "Posicione o tronco praticamente paralelo ao chão com os joelhos semiflexionados e lombar travada.",
            "A barra começa parada no chão a cada repetição.",
            "Puxe a barra de forma explosiva até tocar a região inferior do peito/abdômen superior.",
            "Retorne a barra totalmente ao chão e repita."
        ],
        "erro_fatal": "Levantar o tronco usando impulso da lombar para puxar o peso."
    },
    "Rosca Martelo Excêntrica": {
        "titulo": "Rosca Martelo com Halteres (Foco no Tendão Distal do Bíceps)",
        "imgs": [f"{BASE_IMG_URL}/Hammer_Curls/0.jpg", f"{BASE_IMG_URL}/Hammer_Curls/1.jpg"],
        "svg": "default",
        "musculos": "Braquial, Braquiorradial e Bíceps Braquial",
        "tendoes": "Tendão Distal do Bíceps (inserção no rádio) e Tendão Comum dos Extensores",
        "execucao": [
            "Segure os halteres com pegada neutra (palmas das mãos voltadas uma para a outra).",
            "Suba o peso mantendo os cotovelos fixos ao lado das costelas.",
            "Segure 1 segundo no topo e desça em 3 segundos cravados resistindo à gravidade.",
            "Esse estímulo lento fortalece a inserção do bíceps, prevenindo lesões no Levantamento Terra pesado."
        ],
        "erro_fatal": "Soltar o peso rápido na descida ou jogar o ombro para a frente."
    },
    "Agachamento Búlgaro": {
        "titulo": "Agachamento Búlgaro com Halteres",
        "imgs": [f"{BASE_IMG_URL}/Split_Squat_with_Dumbbells/0.jpg", f"{BASE_IMG_URL}/Split_Squat_with_Dumbbells/1.jpg"],
        "svg": "squat",
        "musculos": "Quadríceps, Glúteo Máximo e Glúteo Médio (estabilizador pélvico)",
        "tendoes": "Tendão Patelar e Tendão Quadricipital (unilateral sem compressão na coluna)",
        "execucao": [
            "Apoie o peito do pé de trás em um banco na altura do joelho.",
            "Incline o tronco levemente à frente (15°) mantendo a coluna reta para recrutar mais o glúteo.",
            "Desça até o joelho de trás chegar próximo ao solo, faça 1 segundo de pausa e suba empurrando pelo pé da frente."
        ],
        "erro_fatal": "Empurrar com a perna de trás ou deixar o joelho da frente balançar para dentro."
    },
    "Elevação Pélvica": {
        "titulo": "Elevação Pélvica com Barra (Barbell Hip Thrust)",
        "imgs": [f"{BASE_IMG_URL}/Barbell_Glute_Bridge/0.jpg", f"{BASE_IMG_URL}/Barbell_Glute_Bridge/1.jpg"],
        "svg": "default",
        "musculos": "Glúteo Máximo e Isquiotibiais",
        "tendoes": "Tendões Proximais dos Isquiotibiais e Inserção Iliotibial",
        "execucao": [
            "Apoie a borda inferior das escápulas em um banco firme e posicione a barra acolchoada sobre o quadril.",
            "Ao subir, mantenha o queixo próximo ao peito (olhando para a frente) e as canelas 100% verticais no topo.",
            "Trave os glúteos por 2 segundos no ponto mais alto garantindo extensão completa de quadril (Lockout do Terra)."
        ],
        "erro_fatal": "Hiperestender a coluna lombar em vez de estender o quadril com os glúteos."
    },
    "Paralelas": {
        "titulo": "Paralelas com Peso (Weighted Dips)",
        "imgs": [f"{BASE_IMG_URL}/Dips_-_Triceps_Version/0.jpg", f"{BASE_IMG_URL}/Dips_-_Triceps_Version/1.jpg"],
        "svg": "default",
        "musculos": "Tríceps Braquial, Peitoral Inferior e Deltoide Anterior",
        "tendoes": "Tendão do Tríceps (olécrano) e Cápsula Anterior do Ombro",
        "execucao": [
            "Sustente o corpo nas barras paralelas com os ombros firmes para baixo (longe das orelhas).",
            "Desça de forma controlada até os braços formarem 90° no cotovelo.",
            "Empurre com potência máxima até estender completamente os cotovelos no topo."
        ],
        "erro_fatal": "Descer além da mobilidade ativa do ombro relaxando as escápulas no fundo."
    },
    "Face Pull": {
        "titulo": "Face Pull na Polia Alta com Rotação Externa",
        "imgs": [f"{BASE_IMG_URL}/Face_Pull/0.jpg", f"{BASE_IMG_URL}/Face_Pull/1.jpg"],
        "svg": "default",
        "musculos": "Deltoide Posterior, Infraespinhal, Redondo Menor e Trapézio Médio",
        "tendoes": "Tendões Posteriores do Manguito Rotador",
        "execucao": [
            "Ajuste a polia na altura da testa usando a corda.",
            "Puxe as pontas da corda em direção às orelhas abrindo os cotovelos e girando os polegares para trás.",
            "Segure 2 segundos na contração máxima sentindo a parte de trás dos ombros e meio das costas."
        ],
        "erro_fatal": "Usar carga excessiva e puxar com a lombar sem girar os punhos para trás."
    },
    "Pallof Press": {
        "titulo": "Pallof Press Isométrico (Core Anti-Rotação)",
        "imgs": [f"{BASE_IMG_URL}/Pallof_Press/0.jpg", f"{BASE_IMG_URL}/Pallof_Press/1.jpg"],
        "svg": "default",
        "musculos": "Oblíquos Internos/Externos, Transverso do Abdômen e Glúteo Médio",
        "tendoes": "Aponeurose Abdominal e Fáscia Toracolombar",
        "execucao": [
            "Fique de lado para a polia ou elástico na altura do esterno.",
            "Empurre o puxador à frente do peito até esticar os braços e segure de 15 a 20 segundos.",
            "Resista totalmente à força lateral que tenta girar seu tronco."
        ],
        "erro_fatal": "Girar os ombros ou compensar inclinando o quadril."
    },
    "Ab Wheel": {
        "titulo": "Ab Wheel (Roda Abdominal) / Prancha RKC",
        "imgs": [f"{BASE_IMG_URL}/Ab_Roller/0.jpg", f"{BASE_IMG_URL}/Ab_Roller/1.jpg"],
        "svg": "default",
        "musculos": "Reto Abdominal, Transverso, Grande Dorsal e Serrátil",
        "tendoes": "Linha Alba e Tendão do Grande Dorsal",
        "execucao": [
            "Ajoelhado, faça uma leve retroversão pélvica ('encaixe o quadril para dentro') e contraia o abdômen.",
            "Deslize a roda à frente apenas até onde consegue manter a lombar 100% blindada, sem arquear.",
            "Puxe de volta pressionando as mãos contra o chão e contraindo o abdômen."
        ],
        "erro_fatal": "Deixar a barriga cair em direção ao chão hiperestendendo a coluna lombar."
    },
    "Ativação Tendões Inferiores": {
        "titulo": "Wall Sit (90°) + Isometria Unipodal de Panturrilha",
        "imgs": [],
        "svg": "squat",
        "musculos": "Quadríceps e Sóleo/Gastrocnêmio (Contração Isométrica)",
        "tendoes": "Tendão Patelar e Tendão de Aquiles",
        "execucao": [
            "Wall Sit: Apoie as costas na parede com joelhos a 90° e sustente 40 segundos imóveis. Isso alinha o colágeno patelar e reduz a dor cortical antes do agachamento.",
            "Panturrilha Isométrica: Na ponta de um degrau em um pé só, sustente no meio da subida por 30 segundos por lado."
        ],
        "erro_fatal": "Fazer rápido ou apoiar as mãos nas coxas para aliviar a tensão do tendão."
    },
    "Ativação Tendões Superiores": {
        "titulo": "Dead Hang (Suspensão na Barra) + Isometria de Manguito",
        "imgs": [f"{BASE_IMG_URL}/Pullups/0.jpg"],
        "svg": "default",
        "musculos": "Flexores de Antebraço, Manguito Rotador e Latíssimo",
        "tendoes": "Tendões do Punho, Cotovelo e Espaço Subacromial do Ombro",
        "execucao": [
            "Dead Hang: Segure na barra fixa com pegada firme e fique pendurado por 35 segundos respirando fundo. Descomprime a coluna e prepara os tendões dos dedos e cotovelos.",
            "Manguito: Segure um elástico leve com cotovelos a 90° colados ao corpo, abra para fora e sustente 20 segundos."
        ],
        "erro_fatal": "Soltar a barra no susto ou prender a respiração."
    }
}

@st.dialog("📸 Guia Visual & Biomecânica do Exercício")
def abrir_modal_exercicio(chave_ex):
    dados = CATALOGO_EXERCICIOS.get(chave_ex, CATALOGO_EXERCICIOS["Agachamento Livre"])
    st.markdown(f"### {dados['titulo']}")
    st.caption(f"🎯 **Músculos:** {dados['musculos']}  \n🧬 **Tendões Blindados:** {dados['tendoes']}")

    if len(dados["imgs"]) >= 2:
        c_img1, c_img2 = st.columns(2)
        with c_img1:
            st.image(dados["imgs"][0], caption="1. Posição Inicial", use_container_width=True)
        with c_img2:
            st.image(dados["imgs"][1], caption="2. Posição Final / Contração", use_container_width=True)
    elif len(dados["imgs"]) == 1:
        st.image(dados["imgs"][0], caption="Posição de Execução", use_container_width=True)

    st.markdown("#### ⚙️ Vetor Biomecânico & Alvo Tendíneo")
    st.markdown(gerar_svg_biomecanico(dados["svg"]), unsafe_allow_html=True)

    st.markdown("#### ✅ Passo a Passo de Execução Perfeita")
    for passo in dados["execucao"]:
        st.markdown(f"- {passo}")

    st.error(f"⚠️ **Erro a Evitar:** {dados['erro_fatal']}")

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
    if st.session_state.get("autenticado", False):
        return True

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("## 🔒 Sistema de Força & Tendões")
        st.caption("Acesso restrito protegido por Streamlit Secrets.")
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
# FUNÇÕES DE CÁLCULO BIOMECÂNICO E CONSTRUÇÃO DE CARTÕES HTML
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

def montar_card_principal(badge_texto, titulo_ex, peso_trab, series_reps, rpe_trab, barra_kg, dica_descanso, info_single=None, um_rm=0.0):
    """Monta o HTML do cartão principal sem indentação para evitar erro de bloco de código no Streamlit."""
    bloco_single = ""
    if info_single:
        peso_s = arredondar_carga(um_rm * info_single[0])
        anilhas_s = calcular_anilhas(peso_s, barra_kg)
        bloco_single = (
            f'<hr style="border-color:#333a4d; margin:12px 0;">'
            f'<span class="badge-peak">⚡ Single de Pico Neural</span>'
            f'<div class="weight-highlight">{peso_s:.1f} kg — {info_single[1]} ({info_single[2]})</div>'
            f'<div class="plate-box">💿 Barra: {anilhas_s}</div>'
        )

    html = (
        f'<div class="workout-card">'
        f'<span class="badge-main">{badge_texto}</span>'
        f'<h4 style="margin:6px 0 2px 0;">{titulo_ex}</h4>'
        f'<div class="weight-highlight">{peso_trab:.1f} kg — {series_reps} ({rpe_trab})</div>'
        f'<div class="plate-box">💿 Barra: {calcular_anilhas(peso_trab, barra_kg)}</div>'
        f'<p style="font-size:0.85rem; color:#94a3b8; margin-top:8px; margin-bottom:0;">{dica_descanso}</p>'
        f'{bloco_single}'
        f'</div>'
    )
    return html

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
# CABEÇALHO E PAINEL COMPACTO DE 1RMs
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
aba_treino, aba_galeria, aba_tendoes, aba_projecao, aba_cf = st.tabs([
    "🏋️ Treino do Dia",
    "📚 Galeria de Execuções",
    "🧬 Protocolo de Tendões",
    "📈 Projeção (1 Ano)",
    "🏃 CrossFit & Recuperação"
])

# =============================================================
# ABA 1: TREINO DO DIA (COM CLIQUE NOS EXERCÍCIOS)
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
            "📱 Selecione o Dia:",
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
    st.info(f"🧬 **Diretriz da Semana:** {cfg['foco_tendao']} *(Toque nos botões 📸 abaixo de cada exercício para abrir a imagem ilustrativa)*")

    def renderizar_segunda(sufixo=""):
        sq_peso = arredondar_carga(st.session_state.sq_1rm * cfg["sq_main"][0])
        st.markdown("### 🦵 Segunda-Feira: Agachamento, Tração & Pegada")
        
        st.markdown(
            '<div class="tendon-card">'
            '<span class="badge-tendon">1. Ativação de Tendões (Pré-Barra)</span>'
            '<p style="margin-top:8px; margin-bottom:4px;"><b>• Nutrição (45m antes):</b> 15g Colágeno Tipo 1 + 100mg Vitamina C</p>'
            '<p style="margin-bottom:4px;"><b>• Tendão Patelar:</b> Wall Sit (Cadeirinha isométrica a 90°) — 2 × 40 segundos</p>'
            '<p style="margin-bottom:0px;"><b>• Tendão de Aquiles:</b> Isometria de Panturrilha Unipodal no degrau — 2 × 30s/pé</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Ilustração: Ativação Patelar & Aquiles", key=f"btn_tend_seg_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Ativação Tendões Inferiores")

        with st.expander("🔥 Ver Rampagem de Aquecimento do Agachamento", expanded=False):
            st.dataframe(gerar_rampagem("Agachamento", sq_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        st.markdown(
            montar_card_principal(
                badge_texto="2. Levantamento Principal",
                titulo_ex="Agachamento Livre (Back Squat)",
                peso_trab=sq_peso,
                series_reps=cfg["sq_main"][1],
                rpe_trab=cfg["sq_main"][2],
                barra_kg=st.session_state.barra_kg,
                dica_descanso="⏱️ Descanso: 3 a 5 min | Descida controlada (2-3s), subida explosiva.",
                info_single=cfg["sq_main"][3],
                um_rm=st.session_state.sq_1rm
            ),
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Agachamento Livre", key=f"btn_sq_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Agachamento Livre")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">3. Dorsais & Cotovelos</span>'
            f'<h5 style="margin:5px 0;">Barra Fixa Pronada (Pull-ups)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["pullup"]} | ⏱️ Descanso: 2 min</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Barra Fixa Pronada", key=f"btn_pull_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Barra Fixa Pronada")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">4. Pegada Brutal, Antebraço & Trapézio</span>'
            f'<h5 style="margin:5px 0;">Caminhada do Fazendeiro (Heavy Farmer\'s Walk)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["farmer"]} | Segure com força máxima sem deixar o ombro cair.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Farmer's Walk", key=f"btn_fw_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Farmer's Walk")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">5. Estabilidade de Core</span>'
            f'<h5 style="margin:5px 0;">{cfg["core_seg"]}</h5>'
            f'<p style="margin:0;">Trave glúteos e abdômen resistindo à rotação da polia/elástico.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Pallof Press", key=f"btn_pal_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Pallof Press")

    def renderizar_terca(sufixo=""):
        bp_peso = arredondar_carga(st.session_state.bp_1rm * cfg["bp_main"][0])
        st.markdown("### 💪 Terça-Feira: Supino Força, Ombros & Blindagem de Bíceps")

        st.markdown(
            '<div class="tendon-card">'
            '<span class="badge-tendon">1. Ativação de Tendões (Pré-Barra)</span>'
            '<p style="margin-top:8px; margin-bottom:4px;"><b>• Descompressão & Pegada:</b> Dead Hang (Suspensão passiva na barra fixa) — 2 × 35 segundos</p>'
            '<p style="margin-bottom:0px;"><b>• Manguito Rotador:</b> Rotação externa isométrica com elástico — 2 × 20s segurando no final</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Ilustração: Dead Hang & Manguito", key=f"btn_tend_ter_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Ativação Tendões Superiores")

        with st.expander("🔥 Ver Rampagem de Aquecimento do Supino Reto", expanded=False):
            st.dataframe(gerar_rampagem("Supino Reto", bp_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        st.markdown(
            montar_card_principal(
                badge_texto="2. Levantamento Principal",
                titulo_ex="Supino Reto com Barra (Bench Press)",
                peso_trab=bp_peso,
                series_reps=cfg["bp_main"][1],
                rpe_trab=cfg["bp_main"][2],
                barra_kg=st.session_state.barra_kg,
                dica_descanso="⏱️ Descanso: 3 a 5 min | Escápulas retraídas e pés cravados no chão.",
                info_single=cfg["bp_main"][3],
                um_rm=st.session_state.bp_1rm
            ),
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Supino Reto", key=f"btn_bp_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Supino Reto")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">3. Força Vertical de Ombros</span>'
            f'<h5 style="margin:5px 0;">Desenvolvimento Militar em Pé (OHP)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["ohp"]} | 💿 {calcular_anilhas(float(cfg["ohp"].split()[0]), st.session_state.barra_kg)}</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Desenvolvimento Militar", key=f"btn_ohp_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Desenvolvimento Militar")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">4. Tração Horizontal Explosiva</span>'
            f'<h5 style="margin:5px 0;">Pendlay Row (Remada Curvada saindo do chão)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["row"]} | 💿 {calcular_anilhas(float(cfg["row"].split()[0]), st.session_state.barra_kg)}</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Pendlay Row", key=f"btn_row_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Pendlay Row")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">5. Blindagem do Tendão Distal do Bíceps</span>'
            f'<h5 style="margin:5px 0;">Rosca Martelo com Halteres (Excêntrica Lenta)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["curl"]}</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Rosca Martelo", key=f"btn_curl_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Rosca Martelo Excêntrica")

    def renderizar_quinta(sufixo=""):
        dl_peso = arredondar_carga(st.session_state.dl_1rm * cfg["dl_main"][0])
        st.markdown("### ⚡ Quinta-Feira: Levantamento Terra & Cadeia Posterior")

        st.markdown(
            '<div class="tendon-card">'
            '<span class="badge-tendon">1. Ativação de Tendões & Core (Pré-Barra)</span>'
            '<p style="margin-top:8px; margin-bottom:4px;"><b>• Isquiotibiais Proximais:</b> Ponte de Glúteo Unilateral Isométrica — 2 × 30s por perna</p>'
            '<p style="margin-bottom:0px;"><b>• Coluna Lombar:</b> Bird-Dog travado (3s no topo) — 2 × 6 reps por lado</p>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.expander("🔥 Ver Rampagem de Aquecimento do Levantamento Terra", expanded=False):
            st.dataframe(gerar_rampagem("Levantamento Terra", dl_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        st.markdown(
            montar_card_principal(
                badge_texto="2. Levantamento Principal",
                titulo_ex="Levantamento Terra (Deadlift)",
                peso_trab=dl_peso,
                series_reps=cfg["dl_main"][1],
                rpe_trab=cfg["dl_main"][2],
                barra_kg=st.session_state.barra_kg,
                dica_descanso="⏱️ Descanso: 4 a 5 min | Pouse a barra no solo a cada repetição (Dead Stop).",
                info_single=cfg["dl_main"][3],
                um_rm=st.session_state.dl_1rm
            ),
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Levantamento Terra", key=f"btn_dl_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Levantamento Terra")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">3. Força Unilateral & Estabilidade Pélvica</span>'
            f'<h5 style="margin:5px 0;">Agachamento Búlgaro com Halteres</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["bulg"]}</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Agachamento Búlgaro", key=f"btn_bulg_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Agachamento Búlgaro")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">4. Bloqueio Final de Quadril (Lockout)</span>'
            f'<h5 style="margin:5px 0;">Elevação Pélvica com Barra (Hip Thrust)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["pelv"]} | 💿 {calcular_anilhas(float(cfg["pelv"].split()[0]), st.session_state.barra_kg)}</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Elevação Pélvica", key=f"btn_pelv_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Elevação Pélvica")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">5. Blindagem Anti-Extensão Lombar</span>'
            f'<h5 style="margin:5px 0;">{cfg["core_qui"]}</h5>'
            f'<p style="margin:0;">Mantenha costelas fechadas e glúteos contraídos o tempo inteiro.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Ab Wheel / Core", key=f"btn_abw_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Ab Wheel")

    def renderizar_sexta(sufixo=""):
        bp_pausa_peso = arredondar_carga(st.session_state.bp_1rm * cfg["bp_pausa"][0])
        st.markdown("### 🎯 Sexta-Feira: Supino Pausado (Força de Arrancada) & Tríceps")

        st.markdown(
            '<div class="tendon-card">'
            '<span class="badge-tendon">1. Preparação de Tendão Peitoral & Tríceps</span>'
            '<p style="margin-top:8px; margin-bottom:4px;"><b>• Escápulas:</b> Band Pull-Apart — 2 × 15 repetições pausando 1s aberto</p>'
            '<p style="margin-bottom:0px;"><b>• Cotovelos:</b> Sustentação isométrica no topo das paralelas — 2 × 25 segundos</p>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.expander("🔥 Ver Rampagem do Supino Pausado", expanded=False):
            st.dataframe(gerar_rampagem("Supino Pausado", bp_pausa_peso, st.session_state.barra_kg), use_container_width=True, hide_index=True)

        st.markdown(
            montar_card_principal(
                badge_texto="2. Levantamento Técnico / Taxa de Disparo",
                titulo_ex="Supino Reto com Pausa de 3 Segundos no Peito",
                peso_trab=bp_pausa_peso,
                series_reps=cfg["bp_pausa"][1],
                rpe_trab=cfg["bp_pausa"][2],
                barra_kg=st.session_state.barra_kg,
                dica_descanso="⏱️ Descanso: 3 min | Conte 1001, 1002, 1003 com a barra imóvel no esterno e exploda!",
                info_single=None
            ),
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Supino Pausado (3s)", key=f"btn_bpp_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Supino Pausado")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">3. Força Bruta de Tríceps & Peitoral Inferior</span>'
            f'<h5 style="margin:5px 0;">Paralelas (Weighted Dips)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> {cfg["dips"]} | ⏱️ Descanso: 2 a 3 min</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Paralelas (Dips)", key=f"btn_dips_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Paralelas")

        st.markdown(
            f'<div class="acc-card"><span class="badge-acc">4. Blindagem Posterior de Ombro & Manguito</span>'
            f'<h5 style="margin:5px 0;">Face Pull na Polia Alta (Pausa de 2s atrás)</h5>'
            f'<p style="margin:0;"><b>Prescrição:</b> 3 a 4 séries × 15 reps focando em rotação externa máxima.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("📸 Ver Execução e Imagem: Face Pull", key=f"btn_fp_{sufixo}", use_container_width=True):
            abrir_modal_exercicio("Face Pull")

    if dia_filtro == "Seg (Agacho)":
        renderizar_segunda("solo")
    elif dia_filtro == "Ter (Supino)":
        renderizar_terca("solo")
    elif dia_filtro == "Qui (Terra)":
        renderizar_quinta("solo")
    elif dia_filtro == "Sex (Potência)":
        renderizar_sexta("solo")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            renderizar_segunda("all")
            st.divider()
            renderizar_quinta("all")
        with col_b:
            renderizar_terca("all")
            st.divider()
            renderizar_sexta("all")

# =============================================================
# ABA 2: GALERIA COMPLETA DE EXECUÇÕES & IMAGENS
# =============================================================
with aba_galeria:
    st.subheader("📚 Biblioteca Visual de Todos os Exercícios do Programa")
    st.caption("Selecione qualquer movimento abaixo para inspecionar as imagens de início/fim, os tendões recrutados e o diagrama vetorial.")

    ex_escolhido = st.selectbox("🔍 Escolha o Exercício:", list(CATALOGO_EXERCICIOS.keys()))
    info_ex = CATALOGO_EXERCICIOS[ex_escolhido]

    col_g1, col_g2 = st.columns([1.3, 1])
    with col_g1:
        st.markdown(f"### {info_ex['titulo']}")
        st.markdown(f"**🎯 Músculos Alvo:** {info_ex['musculos']}")
        st.markdown(f"**🧬 Tendões Blindados:** `{info_ex['tendoes']}`")
        if len(info_ex["imgs"]) >= 2:
            ci1, ci2 = st.columns(2)
            ci1.image(info_ex["imgs"][0], caption="Posição Inicial", use_container_width=True)
            ci2.image(info_ex["imgs"][1], caption="Posição Final", use_container_width=True)
        elif len(info_ex["imgs"]) == 1:
            st.image(info_ex["imgs"][0], caption="Execução", use_container_width=True)

    with col_g2:
        st.markdown("#### ⚙️ Diagrama Biomecânico")
        st.markdown(gerar_svg_biomecanico(info_ex["svg"]), unsafe_allow_html=True)
        st.markdown("#### ✅ Regras de Execução")
        for p in info_ex["execucao"]:
            st.markdown(f"- {p}")
        st.error(f"⚠️ **Evite:** {info_ex['erro_fatal']}")

# =============================================================
# ABA 3: PROTOCOLO DE TENDÕES & SUPLEMENTAÇÃO
# =============================================================
with aba_tendoes:
    st.subheader("🧬 Engenharia de Tendões de Aço (Aos 43+ Anos)")
    c_t1, c_t2 = st.columns(2)
    with c_t1:
        st.markdown(
            '<div class="tendon-card">'
            '<h4>🥤 1. Janela Bioquímica (45–60 min Pré-Treino)</h4>'
            '<p>• <b>15g de Colágeno Hidrolisado Tipo 1</b> (ou gelatina sem sabor)</p>'
            '<p>• <b>100mg de Vitamina C</b> (suco de meio limão ou ácido ascórbico)</p>'
            '<p>• <b>Redução de Açúcar Refinado:</b> Evita a glicação (AGEs) que resseca e deixa o tendão quebradiço.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    with c_t2:
        st.markdown(
            '<div class="tendon-card">'
            '<h4>⚙️ 2. As 3 Regras Mecânicas Durante o Treino</h4>'
            '<p>• <b>Nunca solte o peso (Sem quicar):</b> Desça a barra em 2 a 3s. O controle na frenagem espessa o tendão.</p>'
            '<p>• <b>Isometrias de 30-45s no Aquecimento:</b> Alinham as fibras de colágeno e geram analgesia articular imediata.</p>'
            '<p>• <b>Respeite as Semanas 4 e 8 (Deload):</b> O músculo recupera em 48h; o tendão usa a semana leve para cicatrizar microfissuras.</p>'
            '</div>',
            unsafe_allow_html=True
        )

# =============================================================
# ABA 4: SIMULADOR DE PROJEÇÃO DE FORÇA (1 ANO)
# =============================================================
with aba_projecao:
    st.subheader("📈 Projeção Matemática de Força (6 Macrociclos de 8 Semanas)")
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
# ABA 5: INTEGRAÇÃO COM CROSSFIT & RECUPERAÇÃO
# =============================================================
with aba_cf:
    st.subheader("🏃 Como Usar o CrossFit a Favor da Força Bruta")
    col_cf1, col_cf2 = st.columns(2)
    with col_cf1:
        st.markdown(
            '<div class="acc-card">'
            '<h4>🫁 Quarta-Feira: Flushing Aeróbico (Zona 2)</h4>'
            '<p>• <b>Frequência Cardíaca:</b> Ritmo conversacional (RPE 6).</p>'
            '<p>• <b>Cargas:</b> Máximo 30% a 40% do 1RM ou kettlebells leves.</p>'
            '<p>• <b>Função fisiológica:</b> Aumentar capilarização sanguínea para acelerar a ressíntese de ATP-CP entre as séries pesadas de quinta e sexta.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    with col_cf2:
        st.markdown(
            '<div class="acc-card">'
            '<h4>⚡ Sábado: Condicionamento Geral & Mobilidade</h4>'
            '<p>• <b>Regra de Ouro:</b> Pare qualquer série antes da falha concêntrica.</p>'
            '<p>• <b>Evite:</b> Alto volume de LPO pesado ou saltos em profundidade excessivos para poupar o tendão patelar e lombar.</p>'
            '<p>• <b>Domingo:</b> Descanso absoluto do Sistema Nervoso Central.</p>'
            '</div>',
            unsafe_allow_html=True
        )
