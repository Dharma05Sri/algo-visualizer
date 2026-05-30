import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# ASTRAFORGE CYBER-GRID VISUALIZER ENGINE
# PROJECT CODE: AEGIS-VIS-UL7
# ==========================================

# --- 1. CORE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="AstraForge // Aegis Vis UL7", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. ELITE CSS INJECTION: CYBER-GRID AESTHETIC ---
# Radical distinction from previous build: Neon Cyan/Magenta glow, Grid backgrounds, Floating panels
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500;700&display=swap');

    /* Global CSS Overrides */
    :root {
        --cyber-bg: #03001C;
        --cyber-panel: rgba(11, 0, 26, 0.9);
        --text-cyan: #00ffff;
        --text-magenta: #ff00ff;
        --text-main: #b6b1df;
        --border-glow: 0 0 15px rgba(0, 255, 255, 0.4);
        --border-glow-magenta: 0 0 15px rgba(255, 0, 255, 0.4);
    }
    
    .stApp { 
        background-color: var(--cyber-bg); 
        background-image: linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, .05) 25%, rgba(0, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .05) 75%, rgba(0, 255, 255, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, .05) 25%, rgba(0, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .05) 75%, rgba(0, 255, 255, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
        color: var(--text-main); 
        font-family: 'Fira Code', monospace; 
    }

    /* Top Floating Title */
    .title-container {
        text-align: center;
        margin-top: -60px;
        margin-bottom: 30px;
        padding: 20px;
        background: var(--cyber-panel);
        border: 1px solid var(--text-cyan);
        box-shadow: var(--border-glow);
        border-radius: 0 0 15px 15px;
    }
    .main-title {
        color: white;
        text-transform: uppercase;
        letter-spacing: 5px;
        font-size: 2.2rem;
        font-weight: 700;
        text-shadow: 0 0 10px var(--text-cyan);
    }
    .sub-title {
        color: var(--text-cyan);
        font-size: 0.9rem;
        letter-spacing: 2px;
    }

    /* Dashboard styling (Moving controls to top instead of sidebar) */
    [data-testid="stVerticalBlock"] > div:has(div.dashboard-box) {
        background: var(--cyber-panel);
        border: 1px solid var(--text-magenta);
        box-shadow: var(--border-glow-magenta);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 5px;
        padding: 10px;
    }
    div[data-testid="metric-container"] > label { color: var(--text-main) !important; font-size: 0.8rem !important;}
    div[data-testid="metric-container"] > div { color: white !important; font-size: 1.8rem !important; font-weight: bold;}

    /* Advanced Plotly Chart Integration */
    .js-plotly-plot {
        border: 1px solid var(--text-cyan);
        box-shadow: var(--border-glow);
        border-radius: 10px;
        background: var(--cyber-panel) !important;
    }

    /* Control Buttons */
    .stButton>button {
        background-color: transparent;
        color: white;
        border: 1px solid var(--text-cyan);
        border-radius: 4px;
        padding: 12px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: var(--border-glow);
    }
    .stButton>button:hover {
        background-color: rgba(0, 255, 255, 0.1);
        border: 1px solid white;
        transform: scale(1.02);
    }

    /* Theory/Info Section (Bottom) */
    [data-testid="stExpander"] {
        background: var(--cyber-panel);
        border: 1px solid var(--text-magenta);
        box-shadow: var(--border-glow-magenta);
        border-radius: 10px;
    }
    [data-testid="stExpander"] > div[role="button"] > p {
        color: var(--text-magenta) !important;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* Hide standard Streamlit header/footer */
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. THEORETICAL DATA MATRIX ---
algo_matrix = {
    "Bubble Sort": {
        "desc": "An elementary O(n²) sorting algorithm. It repeatedly 'bubbles' the largest unsorted element to its correct position by comparing adjacent pairs.",
        "tc": "O(n²)", "sc": "O(1)", "type": "Comparison/Exchange"
    },
    "Selection Sort": {
        "desc": "An O(n²) comparison sort. It divides the input list into a sorted and an unsorted region, repeatedly selecting the smallest element from the unsorted region and moving it to the sorted region.",
        "tc": "O(n²)", "sc": "O(1)", "type": "Comparison/Selection"
    },
    "Insertion Sort": {
        "desc": "An efficient O(n²) algorithm for small or nearly sorted data. It builds the final sorted array one item at a time by 'inserting' unsorted elements into their correct position within the already sorted partition.",
        "tc": "O(n²)", "sc": "O(1)", "type": "Comparison/Insertion"
    },
    "Quick Sort": {
        "desc": "An O(n log n) divide-and-conquer algorithm. It picks a 'pivot' and partitions the array around it. This is widely considered the fastest comparison sort in practice.",
        "tc": "O(n log n)", "sc": "O(log n)", "type": "Comparison/Partitioning"
    }
}

# --- 4. SESSION STATE / MEMORY MANAGEMENT ---
# Hardcore modular state handling for complex animations
if 'array' not in st.session_state:
    st.session_state.array = []
if 'comparisons' not in st.session_state:
    st.session_state.comparisons = 0
if 'swaps' not in st.session_state:
    st.session_state.swaps = 0
if 'exec_time' not in st.session_state:
    st.session_state.exec_time = 0.0
if 'anim_speed' not in st.session_state:
    st.session_state.anim_speed = 0.05
if 'size' not in st.session_state:
    st.session_state.size = 50

# --- 5. VISUALIZATION FUNCTIONS (PLOTLY NEON ENGINE) ---

def render_plotly_chart(arr, highlighting=None):
    """Generates the advanced, neon-themed Plotly bar chart with gradient glows."""
    colors = ['#00FFFF'] * len(arr) # Standard Cyber-Cyan
    if highlighting:
        for idx in highlighting:
            colors[idx] = '#FF00FF' # Highlight in Cyber-Magenta for comparisons

    fig = go.Figure(data=[go.Bar(
        x=list(range(len(arr))),
        y=arr,
        marker=dict(
            color=colors,
            line=dict(color='white', width=0.5),
            # Complex styling for neon glow effect
            opacity=0.9
        ),
        hovertemplate='Index: %{x}<br>Value: %{y}<extra></extra>'
    )])

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        height=450,
        bargap=0.05
    )
    return fig

def initialize_ui_placeholders():
    """Initializes dynamic screen placeholders for real-time updates."""
    # This architecture ensures fast, efficient redraws
    metric_cols = st.columns(4)
    chart_p = st.empty()
    status_p = st.empty()
    
    return {
        'comp': metric_cols[0].empty(),
        'swap': metric_cols[1].empty(),
        'time': metric_cols[2].empty(),
        'status': metric_cols[3].empty(),
        'chart': chart_p
    }

def update_visuals(placeholders, arr, highlights=None, status="EXECUTING"):
    """Modular function to refresh telemetry and graphics."""
    placeholders['chart'].plotly_chart(render_plotly_chart(arr, highlights), use_container_width=True)
    placeholders['comp'].metric("Comparisons", f"{st.session_state.comparisons:,}")
    placeholders['swap'].metric("Array Swaps", f"{st.session_state.swaps:,}")
    placeholders['time'].metric("Exec. Delta (s)", f"{st.session_state.exec_time:.3f}")
    placeholders['status'].metric("Core Status", status)
    time.sleep(st.session_state.anim_speed)

def generate_new_dataset():
    """Generates a complex random data set."""
    st.session_state.array = [random.randint(20, 1000) for _ in range(st.session_state.size)]
    st.session_state.comparisons = 0
    st.session_state.swaps = 0
    st.session_state.exec_time = 0.0

# --- 6. CORE ALGORITHM ANIMATION ENGINES ---
# Implementing direct session state array manipulation with telemetry tracking

def run_bubble_sort(placeholders):
    arr = st.session_state.array
    n = len(arr)
    start = time.time()
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            st.session_state.comparisons += 1
            st.session_state.exec_time = time.time() - start
            
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                st.session_state.swaps += 1
                swapped = True
                update_visuals(placeholders, arr, highlights=[j, j+1])
            else:
                # Still update visuals for the comparison check
                update_visuals(placeholders, arr, highlights=[j, j+1])
                
        if not swapped: break

def run_selection_sort(placeholders):
    arr = st.session_state.array
    n = len(arr)
    start = time.time()
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            st.session_state.comparisons += 1
            st.session_state.exec_time = time.time() - start
            update_visuals(placeholders, arr, highlights=[j, min_idx])
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if i != min_idx: st.session_state.swaps += 1
        update_visuals(placeholders, arr)

def run_insertion_sort(placeholders):
    arr = st.session_state.array
    start = time.time()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            st.session_state.comparisons += 1
            st.session_state.exec_time = time.time() - start
            update_visuals(placeholders, arr, highlights=[j, j+1])
            if key < arr[j]:
                arr[j+1] = arr[j]
                st.session_state.swaps += 1
                j -= 1
            else: break
        arr[j+1] = key
        update_visuals(placeholders, arr)

# Advanced Recursive QuickSort Wrapper
def partition(arr, low, high, placeholders, start_time):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        st.session_state.comparisons += 1
        st.session_state.exec_time = time.time() - start_time
        update_visuals(placeholders, arr, highlights=[j, high])
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            st.session_state.swaps += 1
            update_visuals(placeholders, arr, highlights=[i, j])
    
    arr[i+1], arr[high] = arr[high], arr[i+1]
    st.session_state.swaps += 1
    update_visuals(placeholders, arr)
    return i + 1

def run_quick_sort(arr, low, high, placeholders, start_time):
    if low < high:
        pi = partition(arr, low, high, placeholders, start_time)
        run_quick_sort(arr, low, pi-1, placeholders, start_time)
        run_quick_sort(arr, pi+1, high, placeholders, start_time)

# --- 7. MAIN UI LAYOUT RENDER ---

# A. Floating Title Panel
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>ASTRAFORGE // AEGIS-VIS-UL7</div>
        <div class='sub-title'>High-Level Algorithmic Analysis Engine</div>
    </div>
""", unsafe_allow_html=True)

# B. Control Dashboard (Elevated at Top)
with st.container():
    st.markdown('<div class="dashboard-box">', unsafe_allow_html=True)
    cols = st.columns([1.5, 1.5, 1, 1])
    
    with cols[0]:
        sel_algo = st.selectbox("Algorithmic Core", list(algo_matrix.keys()))
    with cols[1]:
        # Using Session State links for sliders for advanced reactivity
        st.session_state.size = st.slider("Dataset Elements", 10, 150, 50, step=5)
    with cols[2]:
        st.session_state.anim_speed = st.slider("Step Delay (s)", 0.0, 0.3, 0.05, step=0.01)
    with cols[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        init_btn = st.button("Initialize Logic Stream")
    
    # Auto-regen array if size changed
    if len(st.session_state.array) != st.session_state.size:
        generate_new_dataset()
    st.markdown('</div>', unsafe_allow_html=True)

# C. Telemetry Dashboard & Main Visualization Canvas
ui = initialize_ui_placeholders()

# Render initial state
ui['chart'].plotly_chart(render_plotly_chart(st.session_state.array), use_container_width=True)
ui['status'].metric("Core Status", "IDLE")

# D. Logical Execution Sequence
if init_btn:
    generate_new_dataset() # Fresh start for clean telemetry
    
    # Clear visual state
    update_visuals(ui, st.session_state.array, status="PREPARING")
    
    # Execution Routing
    if sel_algo == "Bubble Sort": run_bubble_sort(ui)
    elif sel_algo == "Selection Sort": run_selection_sort(ui)
    elif sel_algo == "Insertion Sort": run_insertion_sort(ui)
    elif sel_algo == "Quick Sort": run_quick_sort(st.session_state.array, 0, len(st.session_state.array)-1, ui, time.time())
    
    # Final state
    update_visuals(ui, st.session_state.array, status="RESOLVED")
    st.balloons()

# E. Educational & Advanced Analytics Section (Separated visually)
st.markdown("---")
st.markdown("### Advanced Core Analytics // AEGIS INTEL")

with st.expander(f"📖 {sel_algo}: Architecture & Operational Theory", expanded=False):
    cols = st.columns([2, 1])
    with cols[0]:
        st.markdown(f"#### Definition")
        st.write(algo_matrix[sel_algo]["desc"])
        st.markdown(f"**Structural Type:** {algo_matrix[sel_algo]['type']}")
    with cols[1]:
        st.markdown("#### Complexity Profile")
        st.info(f"""
        - Time Complexity: {algo_matrix[sel_algo]['tc']}
        - Space Complexity: {algo_matrix[sel_algo]['sc']}
        """)

with st.expander("📊 Global Complexity Matrix (Computational Comparison)", expanded=False):
    # Convert matrix dict to dataframe and apply Cyber-Grid styling
    data = []
    for algo, intel in algo_matrix.items():
        data.append({
            "Core Algorithm": algo,
            "Class": intel["type"],
            "Time (Avg)": intel["tc"],
            "Space (Worst)": intel["sc"]
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Advanced Metadata Footer
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
st.markdown(f"""
    <p style='text-align: center; color: #8892b0; font-size: 0.7rem; font-family: Courier New, monospace;'>
        [ SYSTEM TIME: {current_time} ] [ BUILD: AEGIS-VIS-UL7.6.1 ] <br>
        &copy; 2026 ASTRAFORGE ENGINEERING SYNDICATE. All rights reserved.
    </p>
""", unsafe_allow_html=True)
