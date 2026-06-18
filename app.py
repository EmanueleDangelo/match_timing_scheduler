import streamlit as st
import datetime

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

# If the user clicks the button, process the logic
if generate_button:
    # This is a temporary success message for testing Step 1
    # We will replace this with the real mathematical calculations in Step 2!
    st.success(f"Generating schedule for the match against **{opposition if opposition else 'Unknown Opposition'}** at **{ko_time.strftime('%H:%M')}**...")
else:
    # Default instruction message before the button is clicked
    st.info("Use the 'Scheduler' sidebar to input your match details, then click **Generate Schedule** (tap the '>' arrow on mobile).")