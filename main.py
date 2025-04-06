import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(page_title="App Library Dashboard", layout="wide")

# Ensure the create_apps directory exists
create_apps_dir = "create_apps"
if not os.path.exists(create_apps_dir):
    os.makedirs(create_apps_dir)

# Define the path to CSV file
csv_file_path = os.path.join(create_apps_dir, "app_library.csv")

# Load existing data if available, otherwise use sample data
if os.path.exists(csv_file_path):
    app_data = pd.read_csv(csv_file_path)
else:
    # Sample data for initial setup
    app_data = pd.DataFrame([
        {
            "App Name": "Invoice Tracker + Reminder Tool",
            "Problem It Solves": "Tracks unpaid invoices and automates follow-up emails",
            "Submitted By": "Cleaning business owner",
            "App Type": "Internal tool",
            "Tech Stack": "Streamlit + Google Sheets + Gmail API (optional)",
            "AI Used?": "Yes – GPT for reminder message generation (toggle option)",
            "User Inputs": "Client name, invoice amount, due date",
            "Core Outputs": "Table of unpaid invoices + reminder log",
            "Automations": "Sends reminder emails after X days past due",
            "Link to Video Tutorial": "",
            "GitHub/Code Link": "",
            "Notes / Future Ideas": "Add client payment status updates, SMS reminders"
        }
    ])
    # Save the initial sample data
    app_data.to_csv(csv_file_path, index=False)

st.title("📚 App Library Dashboard")
st.write("This dashboard tracks all apps you've built based on real-life situations.")

# Add filtering options
with st.sidebar:
    st.header("🔍 Filter Apps")
    app_type = st.selectbox("App Type", ["All"] + sorted(app_data["App Type"].unique().tolist()))
    ai_used = st.selectbox("AI Used?", ["All"] + sorted(app_data["AI Used?"].unique().tolist()))

filtered_data = app_data.copy()
if app_type != "All":
    filtered_data = filtered_data[filtered_data["App Type"] == app_type]
if ai_used != "All":
    filtered_data = filtered_data[filtered_data["AI Used?"] == ai_used]

# Form to add new app entries
with st.expander("➕ Add New App Entry"):
    with st.form("new_app_form"):
        new_entry = {
            "App Name": st.text_input("App Name", placeholder="e.g. Estimate Generator for Plumbers"),
            "Problem It Solves": st.text_area("Problem It Solves", placeholder="Describe the main pain point this app solves"),
            "Submitted By": st.text_input("Submitted By", placeholder="Who requested or inspired this app?"),
            "App Type": st.selectbox("App Type", ["Internal tool", "Client-facing", "Public"]),
            "Tech Stack": st.text_input("Tech Stack", placeholder="e.g. Streamlit + Google Sheets + OpenAI API"),
            "AI Used?": st.text_input("AI Used?", placeholder="Yes or No, with a short explanation if needed"),
            "User Inputs": st.text_area("User Inputs", placeholder="List the inputs a user must fill out"),
            "Core Outputs": st.text_area("Core Outputs", placeholder="What does the app generate or display?"),
            "Automations": st.text_area("Automations", placeholder="Any behind-the-scenes triggers or scheduled actions?"),
            "Link to Video Tutorial": st.text_input("Link to Video Tutorial", placeholder="YouTube or Loom link"),
            "GitHub/Code Link": st.text_input("GitHub/Code Link", placeholder="Optional: link to the source code"),
            "Notes / Future Ideas": st.text_area("Notes / Future Ideas", placeholder="Ideas for improvement or future features")
        }
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Check if at least App Name is provided
            if new_entry["App Name"]:
                # Append the new entry to the dataframe
                app_data = pd.concat([app_data, pd.DataFrame([new_entry])], ignore_index=True)
                # Save the updated dataframe to CSV
                app_data.to_csv(csv_file_path, index=False)
                st.success(f"New entry '{new_entry['App Name']}' saved to {csv_file_path}")
                st.rerun()  # Rerun the app to refresh the data display
            else:
                st.error("App Name is required.")

# Display app table below the form
st.subheader("📋 App Library Table")
st.dataframe(filtered_data, use_container_width=True)

# Add option to download the CSV file
st.download_button(
    label="Download App Library as CSV",
    data=app_data.to_csv(index=False).encode('utf-8'),
    file_name="saved_apps/app_library.csv",
    mime="text/csv"
)
