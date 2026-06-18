import streamlit as st
import datetime
import re 

# Standard page config without forcing wide layouts
st.set_page_config(
    page_title="⏱️ Match Timings Scheduler", 
)


# Main Screen Placeholder
st.title("⏱️ Match Timings Scheduler")


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
    
    # PRE-PROCESS LINES AND CALCULATE REAL DATETIMES FOR VALIDATION
    parsed_events = []
    lines = schedule_template.strip().split('\n')
    
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        if "KO (GAME)" in line:
            parsed_events.append({
                "row_num": idx + 1,
                "datetime": ko_datetime,
                "time_str": formatted_ko_time,
                "is_bold_time": True,
                "event_desc": "**KICK OFF (GAME)**",
                "raw_desc": "KICK OFF (GAME)"
            })
        else:
            match = re.search(r"KO\s*-\s*(\d+)\s*min:\s*(.*)", line)
            if match:
                mins_to_subtract = int(match.group(1))
                event_desc = match.group(2)
                
                calculated_datetime = ko_datetime - datetime.timedelta(minutes=mins_to_subtract)
                
                parsed_events.append({
                    "row_num": idx + 1,
                    "datetime": calculated_datetime,
                    "time_str": calculated_datetime.strftime("%H:%M"),
                    "is_bold_time": True,
                    "event_desc": event_desc,
                    "raw_desc": event_desc
                })
            else:
                # Fallback line for unformatted strings (ignored in chronological calculation check)
                parsed_events.append({
                    "row_num": idx + 1,
                    "datetime": None,
                    "time_str": "--:--",
                    "is_bold_time": False,
                    "event_desc": line,
                    "raw_desc": line
                })

    # CHRONOLOGICAL DATETIME SANITY CHECK
    is_chronological = True
    error_message = ""
    last_valid_datetime = None
    
    for event in parsed_events:
        if event["datetime"] is None:
            continue  # Skip raw descriptive strings
            
        if last_valid_datetime is not None:
            # The next timeline event *must* be strictly later than the previous event
            if event["datetime"] < last_valid_datetime:
                is_chronological = False
                error_message = f"""
                ❌ **Timeline Sequencing Error:** Your timeline goes backwards or stalls!
                \n* **Problem Area (Row {event['row_num']}):** Calculated time evaluates to **{event['time_str']}** (`{event['raw_desc']}`)
                \n* It falls at or before your previous milestone time (**{last_valid_datetime.strftime('%H:%M')}**). 
                \n* Please adjust your countdown order to flow progressively forward toward Kick-Off.
                """
                break
                
        last_valid_datetime = event["datetime"]

    # RENDER UI ONLY IF CHRONOLOGY SANITY CHECK PASSES
    if not is_chronological:
        st.error(error_message)
    else:
        # Main Header (KO vs Opposition @ Time)
        st.markdown(f"## KO vs {opp_name} @ {formatted_ko_time}")
        st.write("---")
        
        # Build layout collections
        table_rows = []
        raw_text_lines = []
        
        for event in parsed_events:
            t_cell = f"**{event['time_str']}**" if event['is_bold_time'] else event['time_str']
            table_rows.append((t_cell, event['event_desc']))
            raw_text_lines.append(f"{event['time_str']} - {event['raw_desc']}")
                    
        # Render the Timings Markdown Table Layout
        markdown_table = "| Time | Action |\n| :--- | :--- |\n"
        for time_cell, event_cell in table_rows:
            markdown_table += f"| {time_cell} | {event_cell} |\n"
        
        st.markdown(markdown_table)
        st.write("---")
        
        # Dedicated Copy/Paste Section for Sharing
        st.markdown("### Copy/Paste Section")
        
        # Constructing a clean text format for Messaging Apps (WhatsApp, Messenger, etc.)
        clipboard_payload = f"*MATCH TIMINGS*\n\n"
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