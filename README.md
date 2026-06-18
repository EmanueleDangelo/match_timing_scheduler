# Match Day Scheduler

A lightweight, mobile-optimized web application built with Python and Streamlit to automate back-calculations for sports tournament timelines. 

Instead of manually calculating multi-step schedules based on varying kick-off (KO) times while exhausted at a sports complex, this tool allows coaches to manage an editable template and generate precise execution timelines in one click.

---

## Features

* **Dynamic Back-Calculations:** Input your Kick-off time and automatically convert `KO - X min` milestones into exact clock times.
* **Mobile Responsive Design:** Tailored layout that collapses beautifully into a native-feeling sidebar menu on a phone.
* **Chronological Sanity Check:** Automatically scans calculated times down the list to ensure your schedule flows forward logically, flagging an error if milestones break chronological order.
* **One-Tap WhatsApp Sharing:** Generates a dedicated plain-text payload at the bottom formatted with messaging syntax (`*BOLD*`), making team updates a simple double-tap and copy/paste away.

## Dependencies

This project requires **Python 3.8+** and a single core package: **Streamlit**.

### Install via pip
Open your terminal or command prompt and run the following command to install Streamlit:
```bash
pip install streamlit
```

### Run locally
```
streamlit run app.py
```
A local development server will start, and the app will automatically open in a new tab inside your default web browser (usually at http://localhost:8501).