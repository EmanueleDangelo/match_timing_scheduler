import streamlit as st
import datetime
import re 

# Standard page config without forcing wide layouts
st.set_page_config(
    page_title="Match Day Scheduler", 
)

st.markdown("""
    <style>
    [data-testid="stSidebar"] textarea {
        font-size: 12pt !important; /* Bumps up font 1-2 points */
        font-family: monospace;     /* Keeps characters aligned */
    }
    </style>
    """, unsafe_allow_html=True)

# Main Screen Placeholder
st.title("⏱️ Match Day Timeline")
st.info("Use the 'Scheduler' sidebar to input your match details (tap the '>' arrow on mobile).")


# =========================================================
# SIDEBAR SETUP (STANDARD SETTINGS)
# =========================================================

# Title of the sidebar
st.sidebar.title("Scheduler")
st.sidebar.markdown("---")

# Time selection tool (Kick Off Time)
default_ko_time = datetime.time(15, 00)
ko_time = st.sidebar.time_input(
    "Kick Off Time:", 
    value=default_ko_time,
    step=60
)

# Opposition input field
opposition = st.sidebar.text_input(
    "Opposition Team Name:", 
    placeholder="e.g., Australia"
)

# 4. Scheduler text box
default_template = """KO - 120 min: Strapping and meeting in room
KO - 60 min: Send in team sheet?
KO - 45 min: Boots on
KO - 40 min: Activation (10 min)
KO - 30 min: Warm up starts (20 min)
KO - 10 min: Bathroom and shirt on
KO - 4 min: Huddle and breathe
KO - 2 min: Have to be ready in the tunnel
KO (GAME)"""

schedule_template = st.sidebar.text_area(
    "Schedule Template Layout:", 
    value=default_template, 
    height=350
)

st.sidebar.markdown("---")

# Generate schedule
generate_button = st.sidebar.button("GENERATE SCHEDULE", use_container_width=True)

# =========================================================
# MAIN SCREEN LOGIC
# =========================================================

if generate_button:

    # Base Setup for DateTime Calculations
    today = datetime.date.today()
    ko_datetime = datetime.datetime.combine(today, ko_time)
    formatted_ko_time = ko_time.strftime("%H:%M")
    opp_name = opposition.strip() if opposition.strip() else "Opposition"
    
    # Main Header (KO vs Opposition @ Time)
    st.markdown(f"## KO vs {opp_name} @ {formatted_ko_time}")
    st.write("---")
    
    # Processing the Text Template Line by Line
    table_rows = []
    raw_text_lines = []
    lines = schedule_template.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Scenario A: The Kick-Off Line itself
        if "KO (GAME)" in line:
            formatted_time = f"**{formatted_ko_time}**"
            event_desc = "**KICK OFF (GAME)**"
            table_rows.append((formatted_time, event_desc))
            raw_text_lines.append(f"{formatted_ko_time} - KICK OFF (GAME)")
            
        # Scenario B: Countdowns (KO - X min)
        else:
            match = re.search(r"KO\s*-\s*(\d+)\s*min:\s*(.*)", line)
            if match:
                mins_to_subtract = int(match.group(1))
                event_desc = match.group(2)
                
                # Time Delta calculation
                calculated_time = ko_datetime - datetime.timedelta(minutes=mins_to_subtract)
                time_str = calculated_time.strftime("%H:%M")
                
                table_rows.append((f"**{time_str}**", event_desc))
                raw_text_lines.append(f"{time_str} - {event_desc}")
            else:
                # Text fallback line if pattern does not match
                table_rows.append(("--:--", line))
                raw_text_lines.append(f"--:-- - {line}")
                
    # Render the Timings Markdown Table Layout
    markdown_table = "| Time | Action |\n| :--- | :--- |\n"
    for time_cell, event_cell in table_rows:
        markdown_table += f"| {time_cell} | {event_cell} |\n"
    
    st.markdown(markdown_table)
    st.write("---")
    
    # Dedicated Copy/Paste Section for Sharing
    st.markdown("###Copy/Paste Section")
    
    # Constructing a clean text format for Messaging Apps (WhatsApp, Messenger, etc.)
    clipboard_payload = f"**MATCH TIMINGS**\n"
    clipboard_payload += f"vs {opp_name.upper()}\n"
    clipboard_payload += f"Kick-off: {formatted_ko_time}\n"
    clipboard_payload += "--------------------------------------\n"
    clipboard_payload += "\n".join(raw_text_lines)
    
    st.text_area(
        label="Tap inside the box below to select all and copy straight to WhatsApp:", 
        value=clipboard_payload, 
        height=250
    )

else:
    # Initial landing screen view before clicking the button
    st.info("👈 Use the 'Scheduler' sidebar inputs on the left to get started, then click **Generate Schedule**.")