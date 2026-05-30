import streamlit as st
import random
import time
import pandas as pd

# ==========================================
# ASTRAFORGE ALGORITHMIC VISUALIZER ENGINE
# VERSION: 6.0 (ELITE BUILD)
# ==========================================

# --- 1. CORE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="AstraForge | Algorithmic Visualizer", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. ELITE CSS INJECTION (DARK MODE & NEON UI) ---
st.markdown("""
    <style>
    /* Global Color Palette */
    :root {
        --bg-dark: #0a192f;
        --bg-panel: #112240;
        --text-main: #ccd6f6;
        --text-muted: #8892b0;
        --accent: #64ffda;
        --accent-glow: rgba(100, 255, 218, 0.1);
    }
    
    /* Backgrounds & Text */
    .stApp { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    h1, h2, h3, h4 { color: #e6f1ff; font-family: 'Courier New', Courier, monospace; }
    
    /* Neon Title */
    .title-text {
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--text-main);
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 1px solid var(--accent);
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    .title-text span { color: var(--accent); }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: var(--bg-panel);
        border: 1px solid #233554;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px var(--accent-glow);
    }
    div[data-testid="metric-container"] > div { color: var(--accent); font-family: 'Courier New', monospace; font-size: 1.5rem; }
    div[data-testid="metric-container"] label { color: var(--text-muted); font-weight: bold; font-size: 1rem; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: var(--bg-panel); border-right: 1px solid #233554; }
    .stSlider > div > div > div > div { background-color: var(--accent); }
    
    /* Buttons */
    .stButton>button {
        background-color: transparent;
        color: var(--accent);
        border: 1px solid var(--accent);
        border-radius: 4px;
        padding: 10px 24px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: var(--accent-glow);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px var(--accent-glow);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: var(--text-muted); font-family: 'Courier New', Courier, monospace; }
    .stTabs [aria-selected="true"] { color: var(--accent); border-bottom-color: var(--accent); }
    
    /* Dataframes/Tables */
    .stDataFrame { background-color: var(--bg-panel); border: 1px solid #233554; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ALGORITHMIC THEORY DICTIONARY ---
# This dictionary stores all the educational data for the UI
algo_data = {
    "Bubble Sort": {
        "description": "A foundational, comparison-based algorithm. It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. It is highly inefficient on large lists but serves as a crucial starting point for understanding loops and list traversal.",
        "best_time": "$O(n)$",
        "avg_time": "$O(n^2)$",
        "worst_time": "$O(n^2)$",
        "space": "$O(1)$",
        "code": '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Flag to optimize and stop early if already sorted
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # Swap elements
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr'''
    },
    "Insertion Sort": {
        "description": "Builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms like quicksort or merge sort. However, it performs incredibly well on small datasets or data that is already substantially sorted.",
        "best_time": "$O(n)$",
        "avg_time": "$O(n^2)$",
        "worst_time": "$O(n^2)$",
        "space": "$O(1)$",
        "code": '''def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr'''
    },
    "Selection Sort": {
        "description": "Divides the input list into two parts: a sorted sublist of items which is built up from left to right, and a sublist of the remaining unsorted items. The algorithm proceeds by finding the smallest element in the unsorted sublist, exchanging (swapping) it with the leftmost unsorted element, and moving the sublist boundaries one element to the right.",
        "best_time": "$O(n^2)$",
        "avg_time": "$O(n^2)$",
        "worst_time": "$O(n^2)$",
        "space": "$O(1)$",
        "code": '''def selection_sort(arr):
    for i in range(len(arr)):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr'''
    },
    "Quick Sort": {
        "description": "A highly efficient, divide-and-conquer algorithm. It works by selecting a 'pivot' element from the array and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot. The sub-arrays are then sorted recursively. It represents advanced control over functions and memory.",
        "best_time": "$O(n \\log n)$",
        "avg_time": "$O(n \\log n)$",
        "worst_time": "$O(n^2)$",
        "space": "$O(\\log n)$",
        "code": '''def quick_sort(arr, low, high):
    if low < high:
        # pi is partitioning index
        pi = partition(arr, low, high)
        # Separately sort elements before and after partition
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1'''
    }
}

# --- 4. SESSION STATE INITIALIZATION ---
if 'array' not in st.session_state:
    st.session_state.array = []
if 'array_size' not in st.session_state:
    st.session_state.array_size = 50
if 'comparisons' not in st.session_state:
    st.session_state.comparisons = 0
if 'swaps' not in st.session_state:
    st.session_state.swaps = 0

def generate_array(size):
    st.session_state.array = [random.randint(10, 1000) for _ in range(size)]
    st.session_state.comparisons = 0
    st.session_state.swaps = 0

# --- 5. SIDEBAR & TELEMETRY CONTROLS ---
st.sidebar.markdown("<h2 style='color: #64ffda; text-align: center;'>SYSTEM CONTROLS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

selected_algo = st.sidebar.selectbox("Select Sorting Architecture", list(algo_data.keys()))
array_size = st.sidebar.slider("Dataset Magnitude (Elements)", min_value=10, max_value=150, value=50)
animation_speed = st.sidebar.slider("Execution Delay (Seconds)", min_value=0.0, max_value=0.5, value=0.02, step=0.01)

if st.sidebar.button("Generate New Dataset"):
    generate_array(array_size)

st.sidebar.markdown("---")
st.sidebar.info("AstraForge Engine v6.0\n\nOptimized for Data Structure Analysis.")

# Auto-generate on first load
if len(st.session_state.array) != array_size:
    generate_array(array_size)

# --- 6. CORE ALGORITHMIC LOGIC & ANIMATION CONTROLLERS ---

def update_ui(chart, comp, swap):
    """Updates the bar chart and metric counters in real-time."""
    chart.bar_chart(st.session_state.array)
    comp.metric("Array Comparisons", st.session_state.comparisons)
    swap.metric("Memory Swaps", st.session_state.swaps)
    time.sleep(animation_speed)

def animate_bubble_sort(chart, comp, swap):
    n = len(st.session_state.array)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            st.session_state.comparisons += 1
            if st.session_state.array[j] > st.session_state.array[j+1]:
                st.session_state.array[j], st.session_state.array[j+1] = st.session_state.array[j+1], st.session_state.array[j]
                st.session_state.swaps += 1
                swapped = True
                update_ui(chart, comp, swap)
        if not swapped:
            break

def animate_insertion_sort(chart, comp, swap):
    for i in range(1, len(st.session_state.array)):
        key = st.session_state.array[i]
        j = i - 1
        while j >= 0:
            st.session_state.comparisons += 1
            if key < st.session_state.array[j]:
                st.session_state.array[j + 1] = st.session_state.array[j]
                st.session_state.swaps += 1
                j -= 1
                update_ui(chart, comp, swap)
            else:
                break
        st.session_state.array[j + 1] = key
        update_ui(chart, comp, swap)

def animate_selection_sort(chart, comp, swap):
    n = len(st.session_state.array)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            st.session_state.comparisons += 1
            if st.session_state.array[j] < st.session_state.array[min_idx]:
                min_idx = j
        st.session_state.array[i], st.session_state.array[min_idx] = st.session_state.array[min_idx], st.session_state.array[i]
        st.session_state.swaps += 1
        update_ui(chart, comp, swap)

# Quick Sort requires a wrapper to handle the recursive animation states
def partition(low, high, chart, comp, swap):
    pivot = st.session_state.array[high]
    i = low - 1
    for j in range(low, high):
        st.session_state.comparisons += 1
        if st.session_state.array[j] <= pivot:
            i = i + 1
            st.session_state.array[i], st.session_state.array[j] = st.session_state.array[j], st.session_state.array[i]
            st.session_state.swaps += 1
            update_ui(chart, comp, swap)
    st.session_state.array[i + 1], st.session_state.array[high] = st.session_state.array[high], st.session_state.array[i + 1]
    st.session_state.swaps += 1
    update_ui(chart, comp, swap)
    return i + 1

def animate_quick_sort(low, high, chart, comp, swap):
    if low < high:
        pi = partition(low, high, chart, comp, swap)
        animate_quick_sort(low, pi - 1, chart, comp, swap)
        animate_quick_sort(pi + 1, high, chart, comp, swap)

# --- 7. MAIN UI RENDER & TAB ARCHITECTURE ---
st.markdown("<div class='title-text'>Astra<span>Forge</span> // Algo-Visualizer</div>", unsafe_allow_html=True)

# Create the Tabbed Interface
tab1, tab2, tab3, tab4 = st.tabs(["[ ⚡ Visualizer Engine ]", "[ 📖 Algorithmic Theory ]", "[ 💻 Python Implementation ]", "[ 📊 Complexity Matrix ]"])

with tab1:
    st.markdown("### Real-Time Execution Environment")
    st.write(f"Currently monitoring: **{selected_algo}** architecture.")
    
    # Telemetry Dashboard
    col1, col2, col3 = st.columns(3)
    comp_metric = col1.empty()
    swap_metric = col2.empty()
    status_metric = col3.empty()
    
    comp_metric.metric("Array Comparisons", st.session_state.comparisons)
    swap_metric.metric("Memory Swaps", st.session_state.swaps)
    status_metric.metric("Engine Status", "IDLE")
    
    st.markdown("---")
    
    # Main Visualization Canvas
    chart_canvas = st.empty()
    chart_canvas.bar_chart(st.session_state.array)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button(f"INITIALIZE {selected_algo.upper()} SEQUENCE", use_container_width=True):
            status_metric.metric("Engine Status", "EXECUTING...")
            st.session_state.comparisons = 0
            st.session_state.swaps = 0
            
            # Execute Selected Routing
            if selected_algo == "Bubble Sort":
                animate_bubble_sort(chart_canvas, comp_metric, swap_metric)
            elif selected_algo == "Insertion Sort":
                animate_insertion_sort(chart_canvas, comp_metric, swap_metric)
            elif selected_algo == "Selection Sort":
                animate_selection_sort(chart_canvas, comp_metric, swap_metric)
            elif selected_algo == "Quick Sort":
                animate_quick_sort(0, len(st.session_state.array)-1, chart_canvas, comp_metric, swap_metric)
                
            status_metric.metric("Engine Status", "COMPLETE")
            st.success("Execution sequence successfully resolved.")

with tab2:
    st.markdown(f"### {selected_algo} Deep Dive")
    st.write(algo_data[selected_algo]["description"])
    
    st.markdown("#### Mathematical Complexity Analysis")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best Case Time", algo_data[selected_algo]["best_time"])
    col2.metric("Average Case", algo_data[selected_algo]["avg_time"])
    col3.metric("Worst Case", algo_data[selected_algo]["worst_time"])
    col4.metric("Memory Space", algo_data[selected_algo]["space"])
    
    st.info("Note: Complexity analysis utilizes Big-O notation to mathematically describe the limiting behavior of a function when the argument tends towards a particular value or infinity.")

with tab3:
    st.markdown(f"### Core Python Mechanics: {selected_algo}")
    st.write("Review the underlying structural loops, list indices, and functional definitions driving this algorithm.")
    st.code(algo_data[selected_algo]["code"], language="python")

with tab4:
    st.markdown("### Global Algorithmic Complexity Matrix")
    st.write("A macro-level comparison of computational efficiency across multiple structures.")
    
    # Generate DataFrame dynamically from dictionary
    matrix_data = {
        "Algorithm": [],
        "Best-Case Time": [],
        "Average-Case Time": [],
        "Worst-Case Time": [],
        "Space Complexity": []
    }
    
    for algo, data in algo_data.items():
        matrix_data["Algorithm"].append(algo)
        matrix_data["Best-Case Time"].append(data["best_time"])
        matrix_data["Average-Case Time"].append(data["avg_time"])
        matrix_data["Worst-Case Time"].append(data["worst_time"])
        matrix_data["Space Complexity"].append(data["space"])
        
    df = pd.DataFrame(matrix_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8892b0; font-size: 0.8rem;'>&copy; 2026 AstraForge Engineering | Advanced Computational Visualization</p>", unsafe_allow_html=True)
