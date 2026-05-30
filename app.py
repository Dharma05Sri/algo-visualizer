import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go
import base64
from datetime import datetime

# ==========================================
# ASTRAFORGE APEX VISUALIZER ENGINE
# CLASSIFICATION: ULTIMATE HYBRID BUILD
# ==========================================

st.set_page_config(
    page_title="AstraForge | Apex Engine", 
    page_icon="🌌", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 1. ELITE CYBER-GRID CSS (HYBRID AESTHETIC) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500;700&display=swap');
    
    :root {
        --cyber-bg: #03001C;
        --cyber-panel: rgba(11, 0, 26, 0.85);
        --text-cyan: #00ffff;
        --text-magenta: #ff00ff;
        --text-main: #b6b1df;
        --border-glow: 0 0 15px rgba(0, 255, 255, 0.4);
        --border-glow-magenta: 0 0 15px rgba(255, 0, 255, 0.4);
    }
    
    .stApp {
        background-color: var(--cyber-bg);
        background-image: 
            linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, .05) 25%, rgba(0, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .05) 75%, rgba(0, 255, 255, .05) 76%, transparent 77%, transparent), 
            linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, .05) 25%, rgba(0, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .05) 75%, rgba(0, 255, 255, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
        color: var(--text-main);
        font-family: 'Fira Code', monospace;
    }

    /* Core Typography */
    .apex-title {
        text-align: center; font-size: 2.8rem; font-weight: 900; margin-bottom: 0px; margin-top: -40px;
        text-transform: uppercase; letter-spacing: 4px;
        background: linear-gradient(90deg, var(--text-cyan), var(--text-magenta));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 255, 255, 0.2);
    }
    .apex-sub { text-align: center; color: var(--text-cyan); letter-spacing: 5px; font-size: 0.9rem; margin-bottom: 30px;}

    /* Glassmorphism Dashboard Panels */
    .glass-panel {
        background: var(--cyber-panel);
        backdrop-filter: blur(10px);
        border: 1px solid var(--text-cyan);
        border-radius: 10px;
        padding: 20px;
        box-shadow: var(--border-glow);
        margin-bottom: 20px;
    }

    /* Metric Override */
    div[data-testid="metric-container"] {
        background: rgba(0, 0, 0, 0.5); border: 1px solid var(--text-magenta); border-left: 4px solid var(--text-cyan);
        padding: 15px; border-radius: 5px; box-shadow: var(--border-glow-magenta);
    }
    div[data-testid="metric-container"] label { color: var(--text-main) !important; font-size: 0.8rem !important;}
    div[data-testid="metric-container"] div { color: var(--text-cyan) !important; font-weight: bold;}

    /* Interactive Buttons */
    .stButton>button {
        background: transparent; color: var(--text-cyan); border: 1px solid var(--text-cyan);
        padding: 12px; width: 100%; border-radius: 5px; font-weight: bold; letter-spacing: 2px;
        text-transform: uppercase; transition: 0.3s all; box-shadow: var(--border-glow);
    }
    .stButton>button:hover { background: rgba(0, 255, 255, 0.1); border-color: #fff; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# --- 2. OMNI-DATA THEORETICAL MATRIX ---
OMNI_DATA = {
    "Sorting": {
        "Bubble Sort": {"tc": "$O(n^2)$", "sc": "$O(1)$", "desc": "Elementary swap algorithm. Visualizes basic grid loops."},
        "Selection Sort": {"tc": "$O(n^2)$", "sc": "$O(1)$", "desc": "Finds minimum element and places it at the beginning. Highly visual."},
        "Insertion Sort": {"tc": "$O(n^2)$", "sc": "$O(1)$", "desc": "Builds sorted array one element at a time. Excellent for nearly sorted arrays."},
        "Quick Sort": {"tc": "$O(n \\log n)$", "sc": "$O(\\log n)$", "desc": "Elite pivot-based partitioning. Demonstrates advanced recursive logic."},
        "Heap Sort": {"tc": "$O(n \\log n)$", "sc": "$O(1)$", "desc": "Utilizes a binary heap. Demonstrates maximum memory efficiency."}
    },
    "Searching": {
        "Linear Search": {"tc": "$O(n)$", "sc": "$O(1)$", "desc": "Scans elements sequentially. Brute force execution."},
        "Binary Search": {"tc": "$O(\\log n)$", "sc": "$O(1)$", "desc": "Logarithmic interval halving. REQUIRES SORTED ARRAY."}
    }
}

# --- 3. CORE MEMORY STATE ---
for key in ['array', 'comparisons', 'swaps', 'exec_time', 'found_idx']:
    if key not in st.session_state: st.session_state[key] = None if key == 'array' else 0
if 'size' not in st.session_state: st.session_state.size = 50
if 'speed' not in st.session_state: st.session_state.speed = 0.02

def gen_array(size, sorted_mode=False):
    arr = [random.randint(10, 1000) for _ in range(size)]
    if sorted_mode: arr.sort()
    st.session_state.array = arr
    st.session_state.comparisons = 0
    st.session_state.swaps = 0
    st.session_state.exec_time = 0.0
    st.session_state.found_idx = -1

if st.session_state.array is None: gen_array(50)

# --- 4. ADVANCED PLOTLY NEON RENDERING ---
def render_neon_chart(arr, c_color=[], s_color=[], target_color=[]):
    colors = ['#00FFFF'] * len(arr)
    for i in c_color: 
        if i < len(colors): colors[i] = '#FF00FF' # Magenta for comparison
    for i in s_color: 
        if i < len(colors): colors[i] = '#00FF00' # Green for success/swap
    for i in target_color:
        if i < len(colors): colors[i] = '#FF0000' # Red for targets
        
    fig = go.Figure(data=[go.Bar(
        y=arr, 
        marker=dict(color=colors, line=dict(color='white', width=0.5), opacity=0.9),
        hovertemplate='Index: %{x}<br>Value: %{y}<extra></extra>'
    )])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(visible=False), yaxis=dict(visible=False),
        height=450, bargap=0.05
    )
    return fig

def update_ui(ui, arr, c_color=[], s_color=[], t_color=[], status="EXECUTING..."):
    ui['chart'].plotly_chart(render_neon_chart(arr, c_color, s_color, t_color), use_container_width=True)
    ui['comp'].metric("Comparisons", f"{st.session_state.comparisons:,}")
    ui['swap'].metric("Memory Swaps", f"{st.session_state.swaps:,}")
    ui['time'].metric("Exec. Delta (s)", f"{st.session_state.exec_time:.3f}")
    ui['stat'].metric("System Status", status)
    time.sleep(st.session_state.speed)

# --- 5. EXECUTION PROTOCOLS (SORTING) ---
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
        st.session_state.comparisons += 1
        if r < n and arr[r] > arr[largest]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]; st.session_state.swaps += 1
            update_ui(ui, arr, c_color=[i, largest])
            heapify(n, largest)
    for i in range(n // 2 - 1, -1, -1): heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]; st.session_state.swaps += 1
        update_ui(ui, arr, s_color=[i, 0])
        heapify(i, 0)

# --- 6. EXECUTION PROTOCOLS (SEARCHING) ---
def search_linear(ui, target):
    arr = st.session_state.array; s = time.time()
    for i in range(len(arr)):
        st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
        update_ui(ui, arr, c_color=[i], status="SCANNING MEMORY...")
        if arr[i] == target:
            update_ui(ui, arr, s_color=[i], status="TARGET ACQUIRED")
            return
    update_ui(ui, arr, t_color=list(range(len(arr))), status="404: TARGET NOT FOUND")

def search_binary(ui, target):
    arr = st.session_state.array; s = time.time()
    low = 0; high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        st.session_state.comparisons += 1; st.session_state.exec_time = time.time() - s
        search_space = list(range(low, high+1))
        update_ui(ui, arr, c_color=[mid], s_color=search_space, status=f"HALVING: RANGE {low}-{high}")
        
        if arr[mid] == target:
            update_ui(ui, arr, s_color=[mid], target_color=search_space, status="TARGET ACQUIRED")
            return
        elif arr[mid] < target: low = mid + 1
        else: high = mid - 1
    update_ui(ui, arr, t_color=list(range(len(arr))), status="404: TARGET NOT FOUND")

# --- 7. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffff;text-align:center;'>AEGIS NEXUS</h2>", unsafe_allow_html=True)
    nav_mode = st.radio("System Mode", ["Sorting Engine", "Search Engine", "Complexity Matrix", "Data Export"])
    st.markdown("---")
    st.markdown("### Telemetry Configuration")
    st.session_state.size = st.slider("Dataset Magnitude", 10, 150, 50, step=10)
    st.session_state.speed = st.slider("Execution Delay (s)", 0.0, 0.3, 0.02, step=0.01)
    
    if st.button("FORMAT RANDOM"): gen_array(st.session_state.size, False)
    if st.button("FORMAT SORTED"): gen_array(st.session_state.size, True)

# --- 8. MAIN UI RENDERING ---
st.markdown("<div class='apex-title'>ASTRAFORGE // APEX</div>", unsafe_allow_html=True)
st.markdown("<div class='apex-sub'>MULTIVARIABLE ALGORITHMIC VISUALIZATION</div>", unsafe_allow_html=True)

def initialize_ui():
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    ui = {'comp': c1.empty(), 'swap': c2.empty(), 'time': c3.empty(), 'stat': c4.empty()}
    ui['chart'] = st.empty()
    ui['chart'].plotly_chart(render_neon_chart(st.session_state.array), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    ui['comp'].metric("Comparisons", st.session_state.comparisons)
    ui['swap'].metric("Swaps / Shifts", st.session_state.swaps)
    ui['time'].metric("Delta (s)", f"{st.session_state.exec_time:.3f}")
    ui['stat'].metric("System Status", "IDLE")
    return ui

if nav_mode == "Sorting Engine":
    c1, c2 = st.columns([1, 3])
    with c1:
        algo = st.selectbox("Select Sort Protocol", list(OMNI_DATA["Sorting"].keys()))
        st.info(OMNI_DATA["Sorting"][algo]["desc"])
        if st.button(f"EXECUTE {algo}"):
            ui = initialize_ui()
            if algo == "Bubble Sort": run_bubble(ui)
            elif algo == "Selection Sort": run_selection(ui)
            elif algo == "Insertion Sort": run_insertion(ui)
            elif algo == "Quick Sort": run_quick(st.session_state.array, 0, len(st.session_state.array)-1, ui, time.time())
            elif algo == "Heap Sort": run_heap(ui)
            update_ui(ui, st.session_state.array, status="RESOLUTION COMPLETE")
            st.balloons()
    with c2:
        if 'ui' not in locals(): ui = initialize_ui()

elif nav_mode == "Search Engine":
    c1, c2 = st.columns([1, 3])
    with c1:
        search_algo = st.selectbox("Select Search Protocol", list(OMNI_DATA["Searching"].keys()))
        target_val = st.number_input("Target Memory Value", min_value=0, max_value=1000, value=st.session_state.array[len(st.session_state.array)//2] if len(st.session_state.array)>0 else 500)
        st.warning("Binary Search REQUIRES a sorted array. Use 'FORMAT SORTED' in the sidebar.")
        if st.button(f"EXECUTE {search_algo}"):
            ui = initialize_ui()
            if search_algo == "Linear Search": search_linear(ui, target_val)
            elif search_algo == "Binary Search": search_binary(ui, target_val)
    with c2:
        if 'ui' not in locals(): ui = initialize_ui()

elif nav_mode == "Complexity Matrix":
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("### 📊 Algorithmic Complexity Database")
    st.markdown("Advanced computational limits calculated using Big-O Notation.")
    
    st.markdown("#### Sorting Protocols")
    sort_df = pd.DataFrame.from_dict(OMNI_DATA["Sorting"], orient='index').reset_index()
    sort_df.columns = ["Algorithm", "Time Complexity", "Space Complexity", "Description"]
    st.dataframe(sort_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### Searching Protocols")
    search_df = pd.DataFrame.from_dict(OMNI_DATA["Searching"], orient='index').reset_index()
    search_df.columns = ["Algorithm", "Time Complexity", "Space Complexity", "Description"]
    st.dataframe(search_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif nav_mode == "Data Export":
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("### 💾 Telemetry & Data Export")
    st.markdown("Export the exact memory array currently loaded in the visualizer for offline analysis.")
    
    st.write(f"**Current Array Magnitude:** {len(st.session_state.array)} elements")
    st.write(f"**Last Execution Comparisons:** {st.session_state.comparisons}")
    
    csv = pd.DataFrame({"Memory_Array": st.session_state.array}).to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="astraforge_telemetry.csv" style="color: #00ffff; font-size: 1rem; font-weight: bold; text-decoration: none; border: 1px solid #00ffff; padding: 10px; border-radius: 5px; display: inline-block; margin-top: 10px; box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);">[ DOWNLOAD CSV ]</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><p style='text-align: center; color: #8892b0; font-size: 0.7rem;'>[ ASTRAFORGE APEX ] &copy; 2026. Data visualization engineering.</p>", unsafe_allow_html=True)
