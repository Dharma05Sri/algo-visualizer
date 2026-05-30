import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go
import base64
from datetime import datetime

# ==========================================
# ASTRAFORGE ROYAL ELITE APEX ENGINE
# THEME: MAJESTIC OBSIDIAN & GOLD
# BUILD: v8.0 (COMPLETE MONOLITH)
# ==========================================

st.set_page_config(
    page_title="AstraForge | Royal Elite", 
    page_icon="👑", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 1. MAJESTIC OBSIDIAN & GOLD CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Fira+Code:wght@300;500&display=swap');
    
    :root {
        --obsidian: #050505;
        --royal-gold: #D4AF37;
        --bright-gold: #FFD700;
        --panel-dark: #121212;
        --text-cream: #F5F5DC;
        --border-gold: 1px solid #D4AF37;
    }
    
    .stApp {
        background-color: var(--obsidian);
        background-image: radial-gradient(circle at 2px 2px, rgba(212, 175, 55, 0.05) 1px, transparent 0);
        background-size: 40px 40px;
        color: var(--text-cream);
        font-family: 'Fira Code', monospace;
    }

    /* Elite Typography */
    .royal-title {
        text-align: center; font-size: 3.5rem; font-family: 'Playfair Display', serif;
        margin-top: -50px; margin-bottom: 5px; font-weight: 700;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5));
    }
    .royal-sub { 
        text-align: center; color: var(--royal-gold); letter-spacing: 8px; 
        font-size: 0.8rem; margin-bottom: 40px; font-weight: 500;
    }

    /* High-End Panels */
    .glass-panel {
        background: var(--panel-dark);
        border: var(--border-gold);
        border-radius: 4px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), inset 0 0 10px rgba(212, 175, 55, 0.05);
        margin-bottom: 20px;
    }

    /* Metric Cards (Gold Ingot Style) */
    div[data-testid="metric-container"] {
        background: #000000; border: 1px solid #333; border-top: 3px solid var(--royal-gold);
        padding: 15px; transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover { border-top: 3px solid white; transform: translateY(-3px); }
    div[data-testid="metric-container"] label { color: var(--royal-gold) !important; font-size: 0.7rem !important; letter-spacing: 1px;}
    div[data-testid="metric-container"] div { color: white !important; font-family: 'Playfair Display', serif !important; }

    /* Buttons (Premium Feel) */
    .stButton>button {
        background: linear-gradient(145deg, #1a1a1a, #000); color: var(--royal-gold); 
        border: 1px solid var(--royal-gold); border-radius: 0px; padding: 20px;
        text-transform: uppercase; letter-spacing: 3px; font-weight: bold; transition: 0.4s all;
    }
    .stButton>button:hover { background: var(--royal-gold); color: black; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }

    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. OMNI-DATA ARCHITECTURE ---
OMNI_DATA = {
    "Sorting": {
        "Bubble Sort": {"tc": "O(n²)", "sc": "O(1)", "desc": "The foundational swap mechanism. Visualizes the recursive movement of data indices."},
        "Selection Sort": {"tc": "O(n²)", "sc": "O(1)", "desc": "Repeatedly extracts the minimum element. High-precision selection logic."},
        "Insertion Sort": {"tc": "O(n²)", "sc": "O(1)", "desc": "Incremental data structuring. Most efficient for nearly-sorted telemetry sets."},
        "Quick Sort": {"tc": "O(n log n)", "sc": "O(log n)", "desc": "Divide & Conquer partitioning. The gold standard of speed in modern computing."},
        "Heap Sort": {"tc": "O(n log n)", "sc": "O(1)", "desc": "Binary Tree transformation. Perfect balance of speed and memory conservation."}
    },
    "Searching": {
        "Linear Search": {"tc": "O(n)", "sc": "O(1)", "desc": "Exhaustive scan. The brute-force protocol for unsorted memory."},
        "Binary Search": {"tc": "O(log n)", "sc": "O(1)", "desc": "Logarithmic division. Requires a pre-sorted dataset for execution."}
    }
}

# --- 3. MEMORY STATE MANAGEMENT ---
if 'array' not in st.session_state: st.session_state.array = None
for key in ['comparisons', 'swaps', 'exec_time']:
    if key not in st.session_state: st.session_state[key] = 0
if 'size' not in st.session_state: st.session_state.size = 50
if 'speed' not in st.session_state: st.session_state.speed = 0.05

def gen_array(size, sorted_mode=False):
    arr = [random.randint(10, 1000) for _ in range(size)]
    if sorted_mode: arr.sort()
    st.session_state.array = arr
    st.session_state.comparisons = 0
    st.session_state.swaps = 0
    st.session_state.exec_time = 0.0

if st.session_state.array is None: gen_array(50)

# --- 4. ROYAL GOLD PLOTLY ENGINE ---
def render_gold_chart(arr, c_color=[], s_color=[], target_color=[]):
    colors = ['#1A1A1A'] * len(arr) # Charcoal bars
    for i in c_color: 
        if i < len(colors): colors[i] = '#D4AF37' # Metallic Gold for comparisons
    for i in s_color: 
        if i < len(colors): colors[i] = '#FFFFFF' # Pure White for swaps/found
    for i in target_color:
        if i < len(colors): colors[i] = '#8B0000' # Deep Crimson for errors/bounds
        
    fig = go.Figure(data=[go.Bar(
        y=arr, 
        marker=dict(color=colors, line=dict(color='#D4AF37', width=0.8)),
        hovertemplate='Value: %{y}<extra></extra>'
    )])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(visible=False), yaxis=dict(visible=False),
        height=450, bargap=0.1
    )
    return fig

def update_ui(ui, arr, c_color=[], s_color=[], t_color=[], status="SYSTEM ACTIVE"):
    ui['chart'].plotly_chart(render_gold_chart(arr, c_color, s_color, t_color), use_container_width=True)
    ui['comp'].metric("COMPARISONS", f"{st.session_state.comparisons:,}")
    ui['swap'].metric("MEMORY SWAPS", f"{st.session_state.swaps:,}")
    ui['time'].metric("EXEC. DELTA (S)", f"{st.session_state.exec_time:.3f}")
    ui['stat'].metric("CORE STATUS", status)
    time.sleep(st.session_state.speed)

# --- 5. ALGORITHMIC PROTOCOLS (SORTING) ---
def run_bubble(ui):
    arr = st.session_state.array; n = len(arr); s = time.time()
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]; st.session_state.swaps += 1; swapped = True
                update_ui(ui, arr, c_color=[j, j+1])
            else: update_ui(ui, arr, c_color=[j, j+1])
        if not swapped: break

def run_selection(ui):
    arr = st.session_state.array; n = len(arr); s = time.time()
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
            update_ui(ui, arr, c_color=[j, min_idx])
            if arr[j] < arr[min_idx]: min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if i != min_idx: st.session_state.swaps += 1
        update_ui(ui, arr, s_color=[i, min_idx])

def run_insertion(ui):
    arr = st.session_state.array; s = time.time()
    for i in range(1, len(arr)):
        key = arr[i]; j = i - 1
        while j >= 0:
            st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
            update_ui(ui, arr, c_color=[j, j+1])
            if key < arr[j]:
                arr[j+1] = arr[j]; st.session_state.swaps += 1; j -= 1
            else: break
        arr[j+1] = key; update_ui(ui, arr, s_color=[j+1])

def partition(arr, low, high, ui, s_time):
    pivot = arr[high]; i = low - 1
    for j in range(low, high):
        st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s_time
        update_ui(ui, arr, c_color=[j, high])
        if arr[j] <= pivot:
            i += 1; arr[i], arr[j] = arr[j], arr[i]; st.session_state.swaps += 1
            update_ui(ui, arr, c_color=[i, j])
    arr[i+1], arr[high] = arr[high], arr[i+1]; st.session_state.swaps += 1
    update_ui(ui, arr, s_color=[i+1])
    return i + 1

def run_quick(arr, low, high, ui, s_time):
    if low < high:
        pi = partition(arr, low, high, ui, s_time)
        run_quick(arr, low, pi-1, ui, s_time)
        run_quick(arr, pi+1, high, ui, s_time)

def run_heap(ui):
    arr = st.session_state.array; n = len(arr); s_time = time.time()
    def heapify(n, i):
        largest = i; l = 2 * i + 1; r = 2 * i + 2
        st.session_state.comparisons += 1
        if l < n and arr[l] > arr[largest]: largest = l
        if r < n and arr[r] > arr[largest]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]; st.session_state.swaps += 1
            update_ui(ui, arr, c_color=[i, largest]); heapify(n, largest)
    for i in range(n // 2 - 1, -1, -1): heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]; st.session_state.swaps += 1
        update_ui(ui, arr, s_color=[i, 0]); heapify(i, 0)

# --- 6. ALGORITHMIC PROTOCOLS (SEARCHING) ---
def search_linear(ui, target):
    arr = st.session_state.array; s = time.time()
    for i in range(len(arr)):
        st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
        update_ui(ui, arr, c_color=[i], status="SCANNING...")
        if arr[i] == target:
            update_ui(ui, arr, s_color=[i], status="TARGET ACQUIRED")
            return
    update_ui(ui, arr, t_color=list(range(len(arr))), status="404: NOT FOUND")

def search_binary(ui, target):
    arr = st.session_state.array; s = time.time()
    low = 0; high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
        search_space = list(range(low, high+1))
        update_ui(ui, arr, c_color=[mid], s_color=search_space, status=f"DIVIDING: {low}-{high}")
        if arr[mid] == target:
            update_ui(ui, arr, s_color=[mid], status="TARGET ACQUIRED")
            return
        elif arr[mid] < target: low = mid + 1
        else: high = mid - 1
    update_ui(ui, arr, t_color=list(range(len(arr))), status="404: NOT FOUND")

# --- 7. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37;text-align:center;'>ENGINE CORE</h2>", unsafe_allow_html=True)
    nav_mode = st.radio("ARCHIVE MODULE", ["Sort Module", "Search Module", "Complexity Matrix", "Data Archive"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### CONFIGURATION")
    st.session_state.size = st.slider("Dataset Magnitude", 10, 150, 50, step=10)
    st.session_state.speed = st.slider("Execution Delay", 0.0, 0.3, 0.05, step=0.01)
    
    if st.button("RESET: RANDOM DATA"): gen_array(st.session_state.size, False)
    if st.button("RESET: SORTED DATA"): gen_array(st.session_state.size, True)

# --- 8. MAIN UI RENDER ---
st.markdown("<div class='royal-title'>ASTRAFORGE APEX</div>", unsafe_allow_html=True)
st.markdown("<div class='royal-sub'>THE SUPREME COMPUTATIONAL ENGINE</div>", unsafe_allow_html=True)

def initialize_ui():
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    ui = {'comp': c1.empty(), 'swap': c2.empty(), 'time': c3.empty(), 'stat': c4.empty()}
    ui['chart'] = st.empty()
    ui['chart'].plotly_chart(render_gold_chart(st.session_state.array), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return ui

ui = initialize_ui()

if nav_mode == "Sort Module":
    c1, c2 = st.columns([1, 2])
    with c1:
        algo = st.selectbox("PROTOCOL", list(OMNI_DATA["Sorting"].keys()))
        st.write(OMNI_DATA["Sorting"][algo]["desc"])
        if st.button(f"INITIALIZE {algo.upper()}"):
            if algo == "Bubble Sort": run_bubble(ui)
            elif algo == "Selection Sort": run_selection(ui)
            elif algo == "Insertion Sort": run_insertion(ui)
            elif algo == "Quick Sort": run_quick(st.session_state.array, 0, len(st.session_state.array)-1, ui, time.time())
            elif algo == "Heap Sort": run_heap(ui)
            st.success("Execution Resolved.")
            st.balloons()

elif nav_mode == "Search Module":
    c1, c2 = st.columns([1, 2])
    with c1:
        search_algo = st.selectbox("PROTOCOL", list(OMNI_DATA["Searching"].keys()))
        target_val = st.number_input("TARGET VALUE", value=st.session_state.array[len(st.session_state.array)//2] if st.session_state.array is not None else 500)
        st.info("Reminder: Binary Search requires sorted data.")
        if st.button(f"INITIALIZE {search_algo.upper()}"):
            if search_algo == "Linear Search": search_linear(ui, target_val)
            elif search_algo == "Binary Search": search_binary(ui, target_val)

elif nav_mode == "Complexity Matrix":
    st.markdown("### 📊 GLOBAL COMPLEXITY DATABASE")
    sort_df = pd.DataFrame.from_dict(OMNI_DATA["Sorting"], orient='index').reset_index()
    sort_df.columns = ["ALGORITHM", "TIME", "SPACE", "DESCRIPTION"]
    st.dataframe(sort_df, use_container_width=True, hide_index=True)

elif nav_mode == "Data Archive":
    st.markdown("### 💾 TELEMETRY ARCHIVE")
    st.write(f"**Magnitude:** {len(st.session_state.array)} | **Comparisons:** {st.session_state.comparisons}")
    csv = pd.DataFrame({"Memory_Map": st.session_state.array}).to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="telemetry.csv" style="color:#D4AF37;text-decoration:none;border:1px solid #D4AF37;padding:10px;">[ EXTRACT CSV ]</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #444; font-size: 0.6rem;'>ASTRAFORGE APEX // ROYAL EDITION v8.0</p>", unsafe_allow_html=True)
