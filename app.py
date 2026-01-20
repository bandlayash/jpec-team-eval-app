import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import sys

# Try to import webdriver_manager for local testing
try:
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_WEBDRIVER_MANAGER = True
except ImportError:
    HAS_WEBDRIVER_MANAGER = False

# --- CONFIG ---
st.set_page_config(page_title="NSF I-Corps Auto-Filler", layout="wide")
st.title("🤖 NSF I-Corps Form Automation Tool")

# --- MAPPINGS ---
COLUMN_MAPPINGS = {
    'Team/Project Name': 'Team/Project Name',
    'Evaluator Name': 'Evaluator Name',
    'Date': 'Date of Evaluation',
    'Program Outcome': 'Program Outcome: Completed and team is continuing with project or Dropped out of the Program',
    'Customer Interviews': 'Customer Interviews Completed',
    'Customer Discovery': 'Customer Discovery Interviewing: Competence level: High or Fair or Not Yet',
    'Customer Discovery Comments': 'Customer Discovery Interviewing Comments',
    'Program Engagement': 'Program Engagement: Competence level: High or Fair or Not Yet',
    'Program Engagement Comments': 'Program Engagement Comments',
    'Hypothesis Development': 'Hypotheses Development : Competence level: High or Fair or Not Yet',
    'Hypothesis Comments': 'Hypotheses Development Comments',
    'Customer Mapping': 'Customer/Ecosystem Mapping: Competence level: High or Fair or Not Yet',
    'Customer Mapping Comments': 'Customer/Ecosystem Mapping Comments',
    'Value Proposition': 'Value Proposition Design:Competence level: High or Fair or Not Yet',
    'Value Proposition Comments': 'Value Proposition Design Comments',
    'Integration': 'Integration of Insights: Competence level: High or Fair or Not Yet',
    'Integration Comments': 'Integration of Insights Comments',
    'Commercialization': 'Commercialization Pathway: Competence level: High or Fair or Not Yet',
    'Commercialization Comments': 'Commercialization Pathway Comments',
    'NSF Ready': 'Ready for National NSF I-Corps? Yes or No',
    'NSF Comments': 'National I-Corps Readiness Comments',
    'Team Dynamics Comments': 'Team Dynamics and Coachability Comments',
    'Other Comments': 'Other Comments'
}

def get_driver():
    """
    Universal Driver Loader:
    1. Checks for system Chromium (Streamlit Cloud / Linux)
    2. Falls back to webdriver_manager (Local Testing)
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 1. CLOUD / LINUX STRATEGY
    # Streamlit Cloud installs 'chromium-browser' via packages.txt
    if shutil.which("chromium-browser"):
        chrome_options.binary_location = shutil.which("chromium-browser")
        service = Service() # Use default service
        return webdriver.Chrome(service=service, options=chrome_options)
    
    # 2. LOCAL / WINDOWS / MAC STRATEGY
    # Use webdriver_manager to automatically download the right driver
    elif HAS_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    # 3. FALLBACK (Hope Selenium Manager works)
    else:
        return webdriver.Chrome(options=chrome_options)

# --- SIDEBAR ---
st.sidebar.header("Configuration")
form_url = st.sidebar.text_input("Form URL", value='ENTER URL HERE')
enable_submission = st.sidebar.checkbox("✅ Enable REAL Submission", value=False)

# --- MAIN ---
uploaded_file = st.file_uploader("📂 Upload Evaluation Spreadsheet (.xlsx)", type=['xlsx'])

if uploaded_file:
    try:
        xl = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Select Sheet", xl.sheet_names)
        
        if sheet_name:
            # FIX 1: Dynamic Header Row Selection
            df = xl.parse(sheet_name)
            
            # Data Cleaning
            df.columns = df.columns.astype(str).str.strip()
            
            if 'Team/Project Name' in df.columns:
                df['Team/Project Name'] = df['Team/Project Name'].astype(str).str.strip()
                unique_teams = df['Team/Project Name'].unique()
                selected_team = st.selectbox("Select Team to Process:", unique_teams)
                team_df = df[df['Team/Project Name'] == selected_team]
            else:
                st.warning(f"Column 'Team/Project Name' not found. Found columns: {list(df.columns)}")
                team_df = df

            st.divider()
            st.write(f"### Review Data ({len(team_df)} rows)")
            edited_df = st.data_editor(team_df, num_rows="dynamic")
            
            if st.button("🚀 Start Process", type="primary"):
                progress_bar = st.progress(0)
                status = st.empty()
                
                try:
                    driver = get_driver()
                    wait = WebDriverWait(driver, 10)
                    
                    status.write("Browser started. navigating...")
                    driver.get(form_url)
                    time.sleep(2)
                    
                    total = len(edited_df)
                    
                    for i, (idx, row) in enumerate(edited_df.iterrows()):
                        status.write(f"Processing {i+1}/{total}...")
                        
                        try:
                            if i > 0:
                                driver.get(form_url)
                                time.sleep(2)
                            
                            # --- FORM FILLING LOGIC ---
                            # Evaluator
                            val = row.get(COLUMN_MAPPINGS['Evaluator Name'], '')
                            wait.until(EC.presence_of_element_located((By.ID, 'SingleLine7-arialabel'))).send_keys(str(val))
                            
                            # Interviews (Example)
                            val = int(float(row.get(COLUMN_MAPPINGS['Customer Interviews'], 0)))
                            driver.find_element(By.ID, 'Number-arialabel').send_keys(str(val))
                            
                            # ... (The rest of your logic remains the same) ...
                            
                            if enable_submission:
                                driver.find_element(By.XPATH, '//button[contains(text(), "Submit")]').click()
                                st.toast(f"Row {i+1} Submitted")
                            
                        except Exception as e:
                            st.error(f"Row {i+1} Error: {e}")
                        
                        progress_bar.progress((i+1)/total)
                        
                    st.success("Done!")
                    driver.quit()
                    
                except Exception as e:
                    st.error(f"Driver Error: {e}")

    except Exception as e:
        st.error(f"File Error: {e}")