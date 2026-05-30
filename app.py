import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go
import json
import base64

# ==========================================
# ASTRAFORGE OMNI-NODE VISUALIZER
# CLASSIFICATION: GOD-TIER MONOLITH
# ==========================================

st.set_page_config(page_title="AstraForge | Omni-Node", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

# --- 1. ELITE CYBER-GRID CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500;700&display=swap');
    :root {
        --bg-void: #02010a;
        --panel-glass: rgba(15, 12, 41, 0.85);
        --neon-cyan: #00f3ff;
        --neon-purple: #bc13fe;
        --neon-red: #ff0055;
        --text-prime: #e2e2e2;
    }
    
    .stApp {
        background-color: var(--bg-void);
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(0, 243, 255, 0.08), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(188, 19, 254, 0.08), transparent 25%);
        color: var(--text-prime);
        font-family: 'Fira Code', monospace;
    }

    /* Core Typography & Headers */
    h1, h2, h3 { color: #ffffff; text-transform: uppercase; letter-spacing: 2px; }
    .omni-title {
        font-size: 3rem; font-weight: 900; text-align: center; margin-bottom: 0px;
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 243, 255, 0.2);
    }
    .omni-sub { text-align: center; color: var(--neon-cyan); letter-spacing: 5px; margin-bottom: 40px; font-size: 1rem;}

    /* Glassmorphism Panels */
    .glass-panel {
        background: var(--panel-glass);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 243, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    /* Metrics Override */
    div[data-testid="metric-container"] {
        background: rgba(0,0,0,0.4); border: 1px solid var(--neon-purple); border-left: 4px solid var(--neon-cyan);
        padding: 15px; border-radius: 4px; box-shadow: 0 0 10px rgba(188, 19, 254, 0.1);
    }
    div[data-testid="metric-container"] label { color: var(--text-prime) !important; font-size: 0.9rem !important;}
    div[data-testid="metric-container"] div { color: var(--neon-cyan) !important; }

    /* Interactive Buttons */
    .stButton>button {
        background: transparent; color: var(--neon-cyan); border: 1px solid var(--neon-cyan);
        padding: 15px; width: 100%; border-radius: 6px; font-weight: bold; letter-spacing: 2px;
        text-transform: uppercase; transition: 0.3s all; box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
    }
    .stButton>button:hover { background: var(--neon-cyan); color: #000; box-shadow: 0 0 30px rgba(0, 243, 255, 0.5); transform: translateY(-2px);}
    
    .btn-danger>button { border-color: var(--neon-red); color: var(--neon-red); }
    .btn-danger>button:hover { background: var(--neon-red); color: #fff; box-shadow: 0 0 30px rgba(255, 0, 85, 0.5);}
    </style>
""", unsafe_allow_html=True)

# --- 2. OMNI-DATA DICTIONARY (THEORY & LOGIC) ---
OMNI_DATA = {
    "Sorting": {
        "Bubble Sort": {"tc": "$O(n^2)$", "sc": "$O(1)$", "desc": "Elementary swap-based sorting. Highly inefficient for large datasets.", "stable": "Yes"},
        "Selection Sort": {"tc": "$O(n^2)$", "sc": "$O(1)$", "desc": "Finds the minimum element and places it at the beginning.", "stable": "No"},
        "Insertion Sort": {"tc": "$O(n^2)$", "sc": "$O(1)$", "desc": "Builds the sorted array one element at a time. Excellent for nearly sorted data.", "stable": "Yes"},
        "Quick Sort": {"tc": "$O(n \\log n)$", "sc": "$O(\\log n)$", "desc": "Divide and conquer pivot-based partitioning. Elite speed.", "stable": "No"},
        "Merge Sort": {"tc": "$O(n \\log n)$", "sc": "$O(n)$", "desc": "Divides array into halves, sorts them, and merges. Consistent speed.", "stable": "Yes"},
        "Heap Sort": {"tc": "$O(n \\log n)$", "sc": "$O(1)$", "desc": "Utilizes a binary heap data structure. Excellent memory management.", "stable": "No"}
    },
    "Searching": {
        "Linear Search": {"tc": "$O(n)$", "sc": "$O(1)$", "desc": "Scans every element sequentially. Brute force approach.", "req": "None"},
        "Binary Search": {"tc": "$O(\\log n)$", "sc": "$O(1)$", "desc": "Divides search interval in half continuously.", "req": "Array MUST be sorted"}
    }
}

# --- 3. GLOBAL MEMORY STATE ---
for key in ['array', 'search_array', 'comparisons', 'swaps', 'exec_time', 'target_val', 'found_idx']:
    if key not in st.session_state:
        st.session_state[key] = None if 'array' in key else 0
if 'size' not in st.session_state: st.session_state.size = 50
if 'speed' not in st.session_state: st.session_state.speed = 0.02
if 'active_mode' not in st.session_state: st.session_state.active_mode = "Sorting"

def gen_array(size, sorted_mode=False):
    arr = [random.randint(10, 1000) for _ in range(size)]
    if sorted_mode: arr.sort()
    st.session_state.array = arr
    st.session_state.comparisons = 0
    st.session_state.swaps = 0
    st.session_state.exec_time = 0.0
    st.session_state.found_idx = -1

if st.session_state.array is None: gen_array(50)

# --- 4. PLOTLY RENDER ENGINES ---
def render_bar(arr, highlight_red=[], highlight_green=[]):
    colors = ['#00f3ff'] * len(arr)
    for i in highlight_red: 
        if i < len(colors): colors[i] = '#ff0055'
    for i in highlight_green: 
        if i < len(colors): colors[i] = '#00ffaa'
        
    fig = go.Figure(data=[go.Bar(
        y=arr, marker=dict(color=colors, line=dict(color='#000', width=1)),
        hovertemplate='Value: %{y}<extra></extra>'
    )])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), height=400
    )
    return fig

def update_ui(ui, arr, c_color=[], s_color=[], status="EXECUTING"):
    ui['chart'].plotly_chart(render_bar(arr, c_color, s_color), use_container_width=True)
    ui['comp'].metric("Comparisons", st.session_state.comparisons)
    ui['swap'].metric("Swaps / Shifts", st.session_state.swaps)
    ui['time'].metric("Delta (s)", f"{st.session_state.exec_time:.3f}")
    ui['stat'].metric("System Status", status)
    time.sleep(st.session_state.speed)

# --- 5. ALGORITHMIC LOGIC CORES (SORTING) ---
def sort_bubble(ui):
    arr = st.session_state.array; n = len(arr); s = time.time()
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            st.session_state.comparisons += 1
            st.session_state.exec_time = time.time() - s
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                st.session_state.swaps += 1
                swapped = True
                update_ui(ui, arr, c_color=[j, j+1])
        if not swapped: break

def sort_insertion(ui):
    arr = st.session_state.array; s = time.time()
    for i in range(1, len(arr)):
        key = arr[i]; j = i - 1
        while j >= 0:
            st.session_state.comparisons += 1
            st.session_state.exec_time = time.time() - s
            update_ui(ui, arr, c_color=[j, j+1])
            if key < arr[j]:
                arr[j+1] = arr[j]
                st.session_state.swaps += 1
                j -= 1
            else: break
        arr[j+1] = key
        update_ui(ui, arr, s_color=[j+1])

def sort_quick(arr, low, high, ui, s_time):
    if low < high:
        pivot = arr[high]; i = low - 1
        for j in range(low, high):
            st.session_state.comparisons += 1
            st.session_state.exec_time = time.time() - s_time
            update_ui(ui, arr, c_color=[j, high])
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                st.session_state.swaps += 1
        arr[i+1], arr[high] = arr[high], arr[i+1]
        st.session_state.swaps += 1
        update_ui(ui, arr, s_color=[i+1])
        pi = i + 1
        sort_quick(arr, low, pi-1, ui, s_time)
        sort_quick(arr, pi+1, high, ui, s_time)

def sort_heap(ui):
    arr = st.session_state.array; n = len(arr); s_time = time.time()
    def heapify(n, i):
        largest = i; l = 2 * i + 1; r = 2 * i + 2
        st.session_state.comparisons += 1
        if l < n and arr[l] > arr[largest]: largest = l
        st.session_state.comparisons += 1
        if r < n and arr[r] > arr[largest]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            st.session_state.swaps += 1
            update_ui(ui, arr, c_color=[i, largest])
            heapify(n, largest)
    for i in range(n // 2 - 1, -1, -1): heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        st.session_state.swaps += 1
        update_ui(ui, arr, s_color=[i, 0])
        heapify(i, 0)

# --- 6. ALGORITHMIC LOGIC CORES (SEARCHING) ---
def search_linear(ui, target):
    arr = st.session_state.array; s = time.time()
    for i in range(len(arr)):
        st.session_state.comparisons += 1
        st.session_state.exec_time = time.time() - s
        update_ui(ui, arr, c_color=[i], status="SCANNING")
        if arr[i] == target:
            st.session_state.found_idx = i
            update_ui(ui, arr, s_color=[i], status="TARGET ACQUIRED")
            return
    update_ui(ui, arr, status="TARGET NOT FOUND")

def search_binary(ui, target):
    arr = st.session_state.array; s = time.time()
    low = 0; high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        st.session_state.comparisons += 1
        st.session_state.exec_time = time.time() - s
        
        # Highlight search space and mid point
        search_space = list(range(low, high+1))
        update_ui(ui, arr, c_color=[mid], s_color=search_space, status=f"DIVIDING: RANGE {low}-{high}")
        
        if arr[mid] == target:
            st.session_state.found_idx = mid
            update_ui(ui, arr, s_color=[mid], status="TARGET ACQUIRED")
            return
        elif arr[mid] < target: low = mid + 1
        else: high = mid - 1
    update_ui(ui, arr, status="TARGET NOT FOUND")

# --- 7. SIDEBAR NAVIGATION & SETTINGS ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f3ff;text-align:center;'>CONTROL NEXUS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    nav_mode = st.radio("System Mode", ["Sorting Engine", "Search Engine", "Complexity Matrix", "Data Export"])
    
    st.markdown("---")
    st.markdown("### Telemetry Settings")
    st.session_state.size = st.slider("Dataset Magnitude", 10, 200, 50, step=10)
    st.session_state.speed = st.slider("Step Delay (s)", 0.0, 0.5, 0.02, step=0.01)
    
    st.markdown("<div class='btn-danger'>", unsafe_allow_html=True)
    if st.button("FORMAT MEMORY (Randomize)"): gen_array(st.session_state.size, False)
    if st.button("FORMAT MEMORY (Sorted)"): gen_array(st.session_state.size, True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. MAIN UI ROUTING ---
st.markdown("<div class='omni-title'>ASTRAFORGE OMNI-NODE</div>", unsafe_allow_html=True)
st.markdown("<div class='omni-sub'>MULTIVARIABLE DATA STRUCTURE ANALYSIS</div>", unsafe_allow_html=True)

# Helper for UI Placeholders
def init_ui():
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    ui = {'comp': c1.empty(), 'swap': c2.empty(), 'time': c3.empty(), 'stat': c4.empty()}
    ui['chart'] = st.empty()
    ui['chart'].plotly_chart(render_bar(st.session_state.array), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    ui['comp'].metric("Comparisons", st.session_state.comparisons)
    ui['swap'].metric("Swaps / Shifts", st.session_state.swaps)
    ui['time'].metric("Delta (s)", f"{st.session_state.exec_time:.3f}")
    ui['stat'].metric("System Status", "IDLE")
    return ui

if nav_mode == "Sorting Engine":
    st.markdown("### 🔀 Sorting Architecture Visualization")
    c1, c2 = st.columns([1, 3])
    with c1:
        algo = st.selectbox("Select Protocol", list(OMNI_DATA["Sorting"].keys()))
        st.info(OMNI_DATA["Sorting"][algo]["desc"])
        if st.button(f"EXECUTE {algo}"):
            ui = init_ui()
            if algo == "Bubble Sort": sort_bubble(ui)
            elif algo == "Insertion Sort": sort_insertion(ui)
            elif algo == "Quick Sort": sort_quick(st.session_state.array, 0, len(st.session_state.array)-1, ui, time.time())
            elif algo == "Heap Sort": sort_heap(ui)
            else: st.error("Algorithm visualization in development for this module.")
            update_ui(ui, st.session_state.array, status="RESOLUTION COMPLETE")
            st.balloons()
    with c2:
        if 'ui' not in locals(): ui = init_ui()

elif nav_mode == "Search Engine":
    st.markdown("### 🔍 Search Architecture Visualization")
    c1, c2 = st.columns([1, 3])
    with c1:
        search_algo = st.selectbox("Select Protocol", list(OMNI_DATA["Searching"].keys()))
        target = st.number_input("Target Value", min_value=0, max_value=1000, value=st.session_state.array[len(st.session_state.array)//2] if len(st.session_state.array)>0 else 500)
        st.warning("Note: Binary Search REQUIRES a sorted array. Use the sidebar to Format Memory to Sorted.")
        if st.button(f"EXECUTE {search_algo}"):
            ui = init_ui()
            if search_algo == "Linear Search": search_linear(ui, target)
            elif search_algo == "Binary Search": search_binary(ui, target)
    with c2:
        if 'ui' not in locals(): ui = init_ui()

elif nav_mode == "Complexity Matrix":
    st.markdown("### 📊 Algorithmic Complexity Database")
    st.markdown("In high-level systems engineering, choosing the right algorithm relies on mathematical Time and Space complexity limits. The matrix below represents the absolute limits calculated in Big-O Notation.")
    
    st.markdown("#### 1. Sorting Protocols")
    sort_df = pd.DataFrame.from_dict(OMNI_DATA["Sorting"], orient='index')
    sort_df.reset_index(inplace=True)
    sort_df.columns = ["Algorithm", "Time Complexity", "Space Complexity", "Description", "Stable"]
    st.dataframe(sort_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 2. Search Protocols")
    search_df = pd.DataFrame.from_dict(OMNI_DATA["Searching"], orient='index')
    search_df.reset_index(inplace=True)
    search_df.columns = ["Algorithm", "Time Complexity", "Space Complexity", "Description", "Requirement"]
    st.dataframe(search_df, use_container_width=True, hide_index=True)

elif nav_mode == "Data Export":
    st.markdown("### 💾 Telemetry & Data Export")
    st.markdown("Export current memory states and telemetry data for external analysis.")
    
    st.write(f"**Current Array Magnitude:** {len(st.session_state.array)} elements")
    st.write(f"**Last Execution Comparisons:** {st.session_state.comparisons}")
    st.write(f"**Last Execution Time:** {st.session_state.exec_time:.4f} seconds")
    
    # Export Engine
    csv = pd.DataFrame({"Array_Data": st.session_state.array}).to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="astraforge_telemetry.csv" style="color: #bc13fe; font-size: 1.2rem; font-weight: bold; text-decoration: none; border: 1px solid #bc13fe; padding: 10px; border-radius: 5px; display: inline-block; margin-top: 20px;">[ DOWNLOAD CSV TELEMETRY ]</a>'
    st.markdown(href, unsafe_allow_html=True)
