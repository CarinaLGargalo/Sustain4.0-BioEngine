# Streamlit Complete Reference Guide

**Version:** Latest (as of October 2025)  
**Purpose:** Comprehensive reference for Streamlit development  
**Source:** Generated from Context7 MCP documentation  

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Session State Management](#session-state-management)
3. [Layout & Containers](#layout--containers)
4. [Widgets & Input](#widgets--input)
5. [Data Display](#data-display)
6. [Charts & Visualization](#charts--visualization)
7. [File Operations](#file-operations)
8. [Caching & Performance](#caching--performance)
9. [Multipage Apps](#multipage-apps)
10. [Status & Progress](#status--progress)
11. [Forms](#forms)
12. [Chat Interface](#chat-interface)
13. [Configuration](#configuration)
14. [Best Practices](#best-practices)

---

## Core Concepts

### App Structure
```python
import streamlit as st

# Page configuration (MUST be first)
st.set_page_config(
    page_title="My App",
    page_icon="📊",
    layout="wide",  # or "centered"
    initial_sidebar_state="collapsed"  # or "expanded"
)

# Your app code
st.title("My Application")
st.write("Hello, World!")
```

### Basic Display Elements
```python
# Text elements
st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Plain text")
st.markdown("**Bold** and *italic*")
st.caption("Small text")
st.code("print('Hello')", language="python")

# Magic commands (automatic display)
"Just write text"  # Automatically displayed
df  # DataFrames displayed automatically
```

### Rerun Control
```python
# Force app rerun
st.rerun()

# Stop execution
st.stop()
```

---

## Session State Management

### Basic Usage
```python
# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0

# Read and write
st.session_state.count += 1
st.write(f"Count: {st.session_state.count}")

# Widget with key (auto-stores in session state)
st.text_input("Name", key="user_name")
st.write(st.session_state.user_name)
```

### Callbacks
```python
def increment():
    st.session_state.counter += 1

def reset():
    st.session_state.counter = 0

if 'counter' not in st.session_state:
    st.session_state.counter = 0

col1, col2 = st.columns(2)
with col1:
    st.button("Increment", on_click=increment)
with col2:
    st.button("Reset", on_click=reset)

st.write(f"Counter: {st.session_state.counter}")
```

### Preserving Widget State Across Pages
```python
# Method 1: Simple preservation
if "my_key" in st.session_state:
    st.session_state.my_key = st.session_state.my_key

# Method 2: With temporary keys
def store_value(key):
    st.session_state[key] = st.session_state["_"+key]

def load_value(key):
    st.session_state["_"+key] = st.session_state[key]

load_value("my_key")
st.number_input("Value", key="_my_key", on_change=store_value, args=["my_key"])
```

### Widget State Management
```python
# Direct widget state manipulation
if "celsius" not in st.session_state:
    st.session_state.celsius = 50.0

st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    key="celsius"
)

# The value is automatically in session state
st.write(st.session_state.celsius)
```

### Query Parameters
```python
# Set query parameters (URL state)
st.query_params["page"] = "home"
st.query_params["user"] = "john"

# Read query parameters
if "page" in st.query_params:
    current_page = st.query_params["page"]
    st.write(f"Current page: {current_page}")
```

---

## Layout & Containers

### Columns
```python
# Equal width columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column 1")
    st.write("Content 1")

with col2:
    st.header("Column 2")
    st.write("Content 2")

with col3:
    st.header("Column 3")
    st.write("Content 3")

# Custom width columns (proportional)
col1, col2 = st.columns([1, 2])  # col2 is twice as wide
```

### Tabs
```python
tab1, tab2, tab3 = st.tabs(["📋 Tab 1", "📊 Tab 2", "🔄 Tab 3"])

with tab1:
    st.write("Content for tab 1")

with tab2:
    st.write("Content for tab 2")

with tab3:
    st.write("Content for tab 3")
```

### Expander
```python
with st.expander("Click to expand", expanded=False):
    st.write("Hidden content that can be revealed")
    st.image("image.png")
```

### Sidebar
```python
# Add to sidebar
st.sidebar.title("Navigation")
st.sidebar.selectbox("Choose", ["A", "B", "C"])
st.sidebar.button("Click me")

# Using with notation
with st.sidebar:
    st.title("Sidebar Content")
    option = st.selectbox("Select", ["Option 1", "Option 2"])
```

### Popover
```python
with st.popover("⚙️ Settings"):
    st.checkbox("Show advanced options")
    st.slider("Threshold", 0, 100, 50)
```

### Empty Container
```python
# Create placeholder that can be replaced
placeholder = st.empty()

# Later, replace its content
placeholder.write("First content")
time.sleep(1)
placeholder.write("Replaced content")
```

### Container
```python
# Generic container
container = st.container()

# Add content to container
container.write("Content in container")
container.button("Button in container")

# Container with height
container = st.container(height=200)
```

---

## Widgets & Input

### Text Input
```python
# Basic text input
name = st.text_input("Enter your name", value="", max_chars=50)

# With customization
text = st.text_input(
    "Label",
    value="default",
    max_chars=100,
    placeholder="Type here...",
    label_visibility="visible",  # or "hidden", "collapsed"
    disabled=False,
    key="my_input",
    help="Help text",
    on_change=my_callback
)
```

### Text Area
```python
message = st.text_area(
    "Your message",
    value="",
    height=150,
    max_chars=500,
    placeholder="Write your message here..."
)
```

### Number Input
```python
number = st.number_input(
    "Enter a number",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=0.1,
    format="%.2f"
)
```

### Slider
```python
# Single value slider
value = st.slider("Select a value", 0, 100, 50)

# Range slider
min_val, max_val = st.slider(
    "Select range",
    0.0, 100.0, (25.0, 75.0)
)

# Date slider
from datetime import datetime, timedelta
date = st.slider(
    "Select date",
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2025, 12, 31),
    value=datetime(2023, 1, 1),
    format="YYYY-MM-DD"
)
```

### Select Box
```python
option = st.selectbox(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    index=0,  # Default selection
    placeholder="Choose...",
    disabled=False,
    label_visibility="visible"
)
```

### Multiselect
```python
options = st.multiselect(
    "Select multiple",
    ["A", "B", "C", "D"],
    default=["A", "B"],
    max_selections=3
)
```

### Radio Buttons
```python
choice = st.radio(
    "Pick one",
    ["Option 1", "Option 2", "Option 3"],
    index=0,
    horizontal=False  # Set to True for horizontal layout
)
```

### Checkbox
```python
checked = st.checkbox(
    "I agree",
    value=False,
    help="Check if you agree"
)

if checked:
    st.write("Thank you!")
```

### Button
```python
# Basic button
if st.button("Click me"):
    st.write("Button clicked!")

# With callback
def on_click():
    st.session_state.clicked = True

st.button(
    "Submit",
    on_click=on_click,
    type="primary",  # or "secondary"
    disabled=False,
    use_container_width=True,
    help="Click to submit"
)
```

### Link Button
```python
st.link_button(
    "Go to Documentation",
    "https://docs.streamlit.io",
    type="secondary"
)
```

### Date Input
```python
from datetime import date

selected_date = st.date_input(
    "Select date",
    value=date.today(),
    min_value=date(2020, 1, 1),
    max_value=date(2030, 12, 31)
)
```

### Time Input
```python
from datetime import time

selected_time = st.time_input(
    "Select time",
    value=time(12, 0)
)
```

### Color Picker
```python
color = st.color_picker(
    "Pick a color",
    value="#FF0000",
    help="Choose your favorite color"
)
```

---

## Data Display

### DataFrame
```python
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

# Interactive dataframe
event = st.dataframe(
    df,
    use_container_width=True,
    hide_index=False,
    height=400,
    on_select="rerun",
    selection_mode=["multi-row", "multi-column"],
    key="my_dataframe"
)

# Access selected rows
if event.selection.rows:
    selected_data = df.iloc[event.selection.rows]
    st.write(selected_data)
```

### Data Editor
```python
# Editable dataframe
edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # Allow adding/deleting rows
    use_container_width=True,
    column_config={
        "name": st.column_config.TextColumn(
            "Full Name",
            max_chars=50,
            required=True
        ),
        "age": st.column_config.NumberColumn(
            "Age",
            min_value=0,
            max_value=120,
            step=1,
            format="%d years"
        ),
        "active": st.column_config.CheckboxColumn(
            "Active",
            default=False
        )
    }
)
```

### Column Configuration
```python
# Number column
st.column_config.NumberColumn(
    "Price",
    min_value=0,
    format="$%d"
)

# Text column with validation
st.column_config.TextColumn(
    "Email",
    validate="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
)

# Checkbox column
st.column_config.CheckboxColumn(
    "Enabled",
    default=True
)

# Area chart column
st.column_config.AreaChartColumn(
    "Sales (last 6 months)",
    y_min=0,
    y_max=100
)
```

### Table
```python
# Static table
st.table(df)
```

### Metrics
```python
col1, col2, col3 = st.columns(3)

col1.metric(
    "Temperature",
    "70 °F",
    delta="1.2 °F",
    delta_color="normal"  # or "inverse", "off"
)

col2.metric("Wind", "9 mph", delta="-8%")
col3.metric("Humidity", "86%", delta="4%")
```

### JSON
```python
st.json({
    "name": "John",
    "age": 30,
    "skills": ["Python", "Streamlit"]
})
```

---

## Charts & Visualization

### Line Chart
```python
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

st.line_chart(
    chart_data,
    x=None,  # Use index
    y=["A", "B", "C"],
    color=["#FF0000", "#00FF00", "#0000FF"],
    height=400
)
```

### Bar Chart
```python
st.bar_chart(
    chart_data,
    x="Category",
    y="Values",
    color="#FF5733"
)
```

### Area Chart
```python
st.area_chart(chart_data)
```

### Scatter Chart
```python
scatter_data = pd.DataFrame({
    "x": np.random.randn(100),
    "y": np.random.randn(100),
    "size": np.random.randint(10, 100, 100),
    "color": np.random.choice(["red", "blue", "green"], 100)
})

st.scatter_chart(
    scatter_data,
    x="x",
    y="y",
    size="size",
    color="color"
)
```

### Map
```python
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)

st.map(
    map_data,
    latitude='lat',
    longitude='lon',
    size=20,
    color="#0000FF"
)
```

### Plotly Charts
```python
import plotly.express as px
import plotly.graph_objects as go

fig = px.scatter(df, x="x", y="y", color="category")
st.plotly_chart(fig, use_container_width=True)
```

### Altair Charts
```python
import altair as alt

point_selector = alt.selection_point("point_selection")

chart = (
    alt.Chart(chart_data)
    .mark_circle(size=100)
    .encode(
        x="a:Q",
        y="b:Q",
        color=alt.condition(point_selector, "c:Q", alt.value("lightgray")),
        tooltip=["a", "b", "c"]
    )
    .add_params(point_selector)
)

event = st.altair_chart(
    chart,
    use_container_width=True,
    key="altair_chart",
    on_select="rerun"
)

if event.selection:
    st.write("Selection:", event.selection)
```

---

## File Operations

### File Uploader
```python
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["csv", "txt", "json", "xlsx"],
    accept_multiple_files=False,
    help="Upload your data file"
)

if uploaded_file is not None:
    # Read as bytes
    bytes_data = uploaded_file.getvalue()
    
    # Read as string
    string_data = uploaded_file.getvalue().decode("utf-8")
    
    # Read as pandas DataFrame
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

### Multiple File Upload
```python
uploaded_files = st.file_uploader(
    "Upload multiple files",
    type=["csv"],
    accept_multiple_files=True
)

for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file)
    st.write(f"File: {uploaded_file.name}")
    st.dataframe(df)
```

### Download Button
```python
# Download text
st.download_button(
    label="Download as Text",
    data="Hello, World!",
    file_name="hello.txt",
    mime="text/plain"
)

# Download CSV
import pandas as pd

df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
    type="primary"
)

# Download binary (Excel, images, etc.)
import base64

with open("file.xlsx", "rb") as file:
    btn = st.download_button(
        label="Download Excel",
        data=file,
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
```

### Camera Input
```python
from PIL import Image

camera_photo = st.camera_input("Take a picture")

if camera_photo is not None:
    image = Image.open(camera_photo)
    st.image(image, caption="Captured photo")
```

### Image Display
```python
# From file
st.image("path/to/image.png", caption="My Image", width=300)

# From URL
st.image("https://example.com/image.jpg")

# From PIL Image
from PIL import Image
img = Image.open("image.png")
st.image(img, use_column_width=True)

# Multiple images
st.image(["img1.png", "img2.png", "img3.png"], width=200)
```

---

## Caching & Performance

### Cache Data
```python
import time

@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data(filepath):
    """Cache expensive data loading operations."""
    time.sleep(2)  # Simulate slow loading
    df = pd.read_csv(filepath)
    return df

# Only runs once per hour
df = load_data("large_dataset.csv")
```

### Cache Resource
```python
@st.cache_resource
def init_database_connection():
    """Cache database connections and ML models."""
    import sqlite3
    conn = sqlite3.connect("database.db", check_same_thread=False)
    return conn

conn = init_database_connection()  # Only runs once per session
```

### Cache with Parameters
```python
@st.cache_data
def expensive_computation(param1, param2):
    """Cache results based on input parameters."""
    result = param1 * param2 + sum(range(1000000))
    return result

result = expensive_computation(10, 20)
```

### Clear Cache
```python
# Clear all caches
if st.button("Clear cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
```

### Caching with Widgets (Experimental)
```python
@st.cache_data(experimental_allow_widgets=True)
def get_data():
    num_rows = st.slider("Number of rows", 10, 100, 50)
    # Generate data based on slider value
    data = np.random.randn(num_rows, 3)
    return data
```

### Fragments (Partial Reruns)
```python
import time

# Regular widget - causes full rerun
full_rerun_button = st.button("Full Rerun")
st.write(f"Page loaded at: {time.time()}")

# Fragment - only reruns this section
@st.fragment
def expensive_operation():
    """This fragment reruns independently."""
    st.write("Fragment section")
    
    if st.button("Fragment Rerun"):
        st.write("Only fragment reran!")
    
    time.sleep(1)
    st.write(f"Fragment updated at: {time.time()}")

expensive_operation()

# Auto-rerun fragment
@st.fragment(run_every=5)  # Auto-rerun every 5 seconds
def live_data():
    st.write(f"Live data: {time.time()}")

live_data()
```

---

## Multipage Apps

### Directory Structure
```
your_app/
├── streamlit_app.py          # Main entrypoint
├── pages/
│   ├── 01_📊_Page_One.py
│   ├── 02_📈_Page_Two.py
│   └── 03_⚙️_Settings.py
└── .streamlit/
    └── config.toml
```

### Main App (streamlit_app.py)
```python
import streamlit as st

st.set_page_config(
    page_title="My Multipage App",
    page_icon="👋",
    layout="wide"
)

st.title("Welcome! 👋")
st.sidebar.success("Select a page above.")

st.markdown("""
## Main Page
Select a page from the sidebar to navigate.
""")
```

### Page Files (pages/01_Page_One.py)
```python
import streamlit as st

st.set_page_config(page_title="Page One", page_icon="📊")

st.title("📊 Page One")
st.write("Content for page one")
```

### Navigation with st.navigation
```python
# streamlit_app.py
import streamlit as st

# Define pages
home = st.Page("home.py", title="Home", icon="🏠")
settings = st.Page("pages/settings.py", title="Settings", icon="⚙️")
reports = st.Page("pages/reports.py", title="Reports", icon="📊")

# Configure navigation
pg = st.navigation({
    "Main": [home],
    "Tools": [reports, settings]
})

# Add sidebar widgets (preserved across pages)
st.sidebar.selectbox("Group", ["A", "B", "C"], key="group")
st.sidebar.slider("Size", 1, 5, key="size")

pg.run()
```

### Page Links
```python
# Create links to other pages
st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/profile.py", label="My Profile", icon="👤")

# Programmatic navigation
if st.button("Go to Settings"):
    st.switch_page("pages/settings.py")
```

### Preserving Widget State Across Pages
```python
# In entrypoint file (streamlit_app.py)
if "my_key" in st.session_state:
    st.session_state.my_key = st.session_state.my_key

# Or use sidebar widgets (automatically preserved)
with st.sidebar:
    st.selectbox("Filter", ["A", "B", "C"], key="filter")
```

---

## Status & Progress

### Progress Bar
```python
import time

progress_bar = st.progress(0, text="Processing...")

for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1, text=f"Processing... {i+1}%")

progress_bar.empty()  # Remove when done
```

### Spinner
```python
with st.spinner("Loading..."):
    time.sleep(2)
    data = load_data()

st.success("Done!")
```

### Status Messages
```python
# Different message types
st.info("ℹ️ This is informational")
st.success("✅ Operation completed successfully!")
st.warning("⚠️ This is a warning")
st.error("❌ An error occurred!")

# Exception display
try:
    risky_operation()
except Exception as e:
    st.exception(e)
```

### Toast Notifications
```python
if st.button("Show toast"):
    st.toast("✅ Operation successful!", icon="✅")
```

### Status Container
```python
import time

with st.status("Processing data...", expanded=True) as status:
    st.write("Loading dataset...")
    time.sleep(1)
    st.write("Analyzing data...")
    time.sleep(1)
    st.write("Generating report...")
    time.sleep(1)
    status.update(label="✅ Complete!", state="complete", expanded=False)
```

### Animations
```python
# Balloons
if st.button("Celebrate!"):
    st.balloons()

# Snow
if st.button("Let it snow!"):
    st.snow()
```

---

## Forms

### Basic Form
```python
with st.form("my_form"):
    st.write("Form Content")
    
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    
    # Every form must have a submit button
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Hello {name}, you are {age} years old")
```

### Form with Callback
```python
def form_callback():
    st.write("Form submitted!")
    st.write(f"Slider: {st.session_state.my_slider}")
    st.write(f"Checkbox: {st.session_state.my_checkbox}")

with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(
        label='Submit',
        on_click=form_callback
    )
```

### Form with Session State
```python
if 'sum' not in st.session_state:
    st.session_state.sum = ''

def calculate_sum():
    result = st.session_state.a + st.session_state.b
    st.session_state.sum = result

col1, col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    st.number_input('a', key='a')
    st.number_input('b', key='b')
    st.form_submit_button('Calculate', on_click=calculate_sum)
```

---

## Chat Interface

### Basic Chat
```python
import time

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "avatar": "👤"
    })
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate streaming
        assistant_response = f"Response to: {prompt}"
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "avatar": "🤖"
    })
```

---

## Configuration

### config.toml
```toml
# .streamlit/config.toml

[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans-serif"  # or "serif", "monospace"

[theme.sidebar]
font = "sans-serif"

[runner]
enforceSerializableSessionState = false
```

### Theme Customization
```python
# Custom theme via config.toml
[theme]
primaryColor = "#1A6CE7"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#1A1D21"
font = "sans-serif"
baseFontSize = 14
```

---

## Best Practices

### 1. Page Configuration First
```python
# ALWAYS first command
st.set_page_config(
    page_title="App",
    page_icon="📊",
    layout="wide"
)
```

### 2. Use Session State for Statefulness
```python
# Initialize before use
if 'data' not in st.session_state:
    st.session_state.data = load_initial_data()

# Use throughout app
process(st.session_state.data)
```

### 3. Cache Expensive Operations
```python
@st.cache_data(ttl=3600)
def load_data():
    return expensive_operation()

@st.cache_resource
def init_model():
    return load_ml_model()
```

### 4. Use Fragments for Partial Updates
```python
@st.fragment
def live_chart():
    # Only this section reruns
    data = get_latest_data()
    st.line_chart(data)

# Full app doesn't rerun when fragment updates
```

### 5. Organize with Containers
```python
# Better organization
with st.container():
    st.title("Section 1")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Metric 1", 100)
    with col2:
        st.metric("Metric 2", 200)
```

### 6. Handle Widget Keys Properly
```python
# Good - explicit key
st.text_input("Name", key="user_name")
value = st.session_state.user_name

# Avoid - no key, value lost on rerun
value = st.text_input("Name")  # Value doesn't persist
```

### 7. Use Callbacks for Complex Logic
```python
def handle_submit():
    # Process form data
    result = process(st.session_state.form_data)
    st.session_state.result = result

st.button("Submit", on_click=handle_submit)
```

### 8. Error Handling
```python
try:
    result = risky_operation()
    st.success("Success!")
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.exception(e)  # Show full traceback
```

### 9. Loading States
```python
with st.spinner("Loading..."):
    data = load_large_dataset()

st.success("✅ Data loaded successfully!")
```

### 10. Responsive Layouts
```python
# Use container width for responsiveness
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df, use_container_width=True)
st.button("Click", use_container_width=True)
```

---

## Common Patterns

### Data Processing Pipeline
```python
import streamlit as st
import pandas as pd

st.title("Data Processing Pipeline")

# Step 1: Upload
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    # Step 2: Load
    with st.spinner("Loading data..."):
        df = pd.read_csv(uploaded_file)
    
    # Step 3: Preview
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Step 4: Process
    if st.button("Process Data"):
        with st.spinner("Processing..."):
            processed_df = process_data(df)
        
        st.success("✅ Processing complete!")
        
        # Step 5: Download
        csv = processed_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Processed Data",
            csv,
            "processed_data.csv",
            "text/csv"
        )
```

### Dashboard Layout
```python
st.set_page_config(layout="wide")

# Header
st.title("📊 Dashboard")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", "1,234", "+12%")
col2.metric("Revenue", "$45,678", "+8%")
col3.metric("Active Sessions", "567", "-3%")
col4.metric("Conversion Rate", "3.2%", "+0.5%")

# Charts row
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Over Time")
    st.line_chart(sales_data)

with col2:
    st.subheader("Category Distribution")
    st.bar_chart(category_data)

# Details table
st.subheader("Recent Transactions")
st.dataframe(transactions_df, use_container_width=True)
```

### Settings Page
```python
st.title("⚙️ Settings")

with st.form("settings_form"):
    st.subheader("User Preferences")
    
    theme = st.selectbox("Theme", ["Light", "Dark"])
    notifications = st.checkbox("Enable notifications", value=True)
    language = st.selectbox("Language", ["English", "Spanish", "French"])
    
    st.subheader("Display Options")
    
    show_grid = st.checkbox("Show grid lines", value=False)
    max_rows = st.number_input("Max rows to display", 10, 1000, 100)
    
    submitted = st.form_submit_button("Save Settings")
    
    if submitted:
        # Save to session state
        st.session_state.settings = {
            "theme": theme,
            "notifications": notifications,
            "language": language,
            "show_grid": show_grid,
            "max_rows": max_rows
        }
        st.success("✅ Settings saved!")
```

---

## Performance Tips

1. **Use caching** for expensive operations
2. **Use fragments** to avoid full app reruns
3. **Lazy load data** - only load when needed
4. **Limit dataframe size** shown at once
5. **Use `st.empty()` for dynamic updates**
6. **Avoid nested columns** when possible
7. **Use session state** instead of global variables
8. **Clear unused session state** values
9. **Optimize image sizes** before displaying
10. **Use appropriate chart types** for data size

---

## Debugging

### Show Variable Values
```python
st.write("Debug:", variable)
st.json(st.session_state)  # Show all session state
```

### Conditional Display
```python
if st.checkbox("Show debug info"):
    st.write("Session State:", st.session_state)
    st.write("Current values:", locals())
```

### Error Boundaries
```python
try:
    risky_operation()
except Exception as e:
    st.error(f"Error: {str(e)}")
    if st.checkbox("Show traceback"):
        st.exception(e)
```

---

## Running Streamlit

### Basic Run
```bash
streamlit run app.py
```

### With Options
```bash
streamlit run app.py --server.port=8502 --server.address=localhost
```

### From Python
```python
if __name__ == "__main__":
    import subprocess
    subprocess.run(["streamlit", "run", "app.py"])
```

---

## Quick Reference

| Category | Command | Purpose |
|----------|---------|---------|
| **Display** | `st.write()` | Universal display |
| | `st.title()` | Large heading |
| | `st.header()` | Medium heading |
| | `st.markdown()` | Markdown text |
| **Input** | `st.button()` | Button |
| | `st.text_input()` | Single line text |
| | `st.number_input()` | Number input |
| | `st.selectbox()` | Dropdown |
| | `st.slider()` | Slider |
| **Layout** | `st.columns()` | Side-by-side layout |
| | `st.tabs()` | Tabbed interface |
| | `st.expander()` | Collapsible section |
| | `st.sidebar` | Sidebar content |
| **Data** | `st.dataframe()` | Interactive table |
| | `st.data_editor()` | Editable table |
| | `st.table()` | Static table |
| | `st.metric()` | KPI display |
| **Charts** | `st.line_chart()` | Line chart |
| | `st.bar_chart()` | Bar chart |
| | `st.plotly_chart()` | Plotly chart |
| | `st.map()` | Map visualization |
| **Files** | `st.file_uploader()` | File upload |
| | `st.download_button()` | File download |
| | `st.camera_input()` | Camera capture |
| **State** | `st.session_state` | Persistent state |
| | `st.rerun()` | Force rerun |
| | `st.stop()` | Stop execution |
| **Cache** | `@st.cache_data` | Cache data |
| | `@st.cache_resource` | Cache resources |
| | `@st.fragment` | Partial rerun |

---

## Additional Resources

- **Official Docs:** https://docs.streamlit.io
- **API Reference:** https://docs.streamlit.io/develop/api-reference
- **Community:** https://discuss.streamlit.io
- **Gallery:** https://streamlit.io/gallery
- **GitHub:** https://github.com/streamlit/streamlit

---

**Last Updated:** October 31, 2025  
**Generated from:** Context7 MCP Documentation  
**For:** Sustain 4.0 BioEngine Project
