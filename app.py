import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="NSF I-Corps Auto-Filler", layout="wide")
st.title("🤖 NSF I-Corps Form Automation Tool")

# --- MAPPING CONFIGURATION ---
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

FORM_URL = 'https://forms.greatlakesicorps.org/GreatLakesiCorps/form/CourseEvaluation/formperma/hCSRkpmJiZgTyHXyMtXM3kkGPAw5hBCYDhBNDWvtbFQ?zfcrm_entity=121d4c2a61659c80006998e7bf10ed7b57c91e98038d84d45e2d5d31bd6e8dbca3ec6e07706a68e83658b700652e1a58abe64fbc64e7e10fcf15821417eebb25'

# --- HELPER FUNCTION: GET DRIVER ---
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Essential for Docker
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Docker/Linux standard path for chromedriver
    # If running locally on Windows with chromedriver.exe in folder:
    if os.path.exists("chromedriver.exe"):
        service = Service("chromedriver.exe")
        return webdriver.Chrome(service=service, options=chrome_options)
    else:
        # Linux/Docker usually puts it here or in PATH
        return webdriver.Chrome(options=chrome_options)

# --- MAIN UI ---
uploaded_file = st.file_uploader("📂 Upload the Evaluation Spreadsheet (.xlsx)", type=['xlsx'])

if uploaded_file:
    try:
        # 1. Load Excel File Wrapper
        xl = pd.ExcelFile(uploaded_file)
        
        # 2. Select Sheet
        sheet_name = st.selectbox("Select the Sheet:", xl.sheet_names)
        
        if sheet_name:
            df = xl.parse(sheet_name)
            
            # CLEANING: Strip whitespace from headers automatically
            df.columns = df.columns.str.strip()
            
            # CLEANING: Strip whitespace from Team Names
            if 'Team/Project Name' in df.columns:
                df['Team/Project Name'] = df['Team/Project Name'].str.strip()
            
            # 3. Validation: Check Missing Columns
            missing_cols = [v for k, v in COLUMN_MAPPINGS.items() if v not in df.columns]
            
            if missing_cols:
                st.error("❌ Column Mismatch! The following columns are missing or named incorrectly:")
                st.write(missing_cols)
                st.warning("Tip: Check for extra spaces at the end of your column headers in Excel.")
            else:
                st.success("✅ Columns validated successfully.")
                
                # 4. Select Team
                unique_teams = df['Team/Project Name'].unique()
                selected_team = st.selectbox("Select Team to Process:", unique_teams)
                
                # Filter Data
                team_df = df[df['Team/Project Name'] == selected_team]
                st.info(f"Found {len(team_df)} row(s) for team: {selected_team}")

                # 5. Run Button
                if st.button("🚀 Start Automation"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        with st.spinner("Initializing Browser..."):
                            driver = get_driver()
                            wait = WebDriverWait(driver, 10)
                            
                            # Navigate
                            driver.get(FORM_URL)
                            time.sleep(3)
                        
                        total_rows = len(team_df)
                        
                        for i, (index, row) in enumerate(team_df.iterrows()):
                            status_text.write(f"Processing evaluation by: **{row[COLUMN_MAPPINGS['Evaluator Name']]}**")
                            
                            # --- YOUR EXISTING LOGIC (Minimally modified for loop) ---
                            try:
                                # RELOAD PAGE FOR EACH ENTRY (Important for Forms)
                                if i > 0:
                                    driver.get(FORM_URL)
                                    time.sleep(2)

                                # Evaluator Name
                                evaluator_field = wait.until(EC.presence_of_element_located((By.ID, 'SingleLine7-arialabel')))
                                evaluator_field.clear()
                                evaluator_field.send_keys(str(row[COLUMN_MAPPINGS['Evaluator Name']]))

                                # Program Outcome logic
                                outcome = str(row[COLUMN_MAPPINGS['Program Outcome']]).strip().lower()
                                if 'dropped' in outcome: driver.find_element(By.ID, 'Radio8_1').click()
                                elif 'completed' in outcome: driver.find_element(By.ID, 'Radio8_2').click()
                                elif 'not continuing' in outcome: driver.find_element(By.ID, 'Radio8_3').click()

                                # Interviews
                                int_field = driver.find_element(By.ID, 'Number-arialabel')
                                int_field.clear()
                                int_field.send_keys(str(int(float(row[COLUMN_MAPPINGS['Customer Interviews']]))))

                                # Fill Text Areas (Generic Loop for brevity in this example)
                                # You would keep your detailed logic here. 
                                # Example for one text field:
                                try:
                                    cd_comment = str(row[COLUMN_MAPPINGS['Customer Discovery Comments']])
                                    driver.find_element(By.ID, 'MultiLine5-arialabel').send_keys(cd_comment)
                                except: pass

                                # SUBMIT BUTTON (Optional - Uncomment if you want it to actually submit)
                                # driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
                                # time.sleep(2)
                                
                                st.write(f"✅ Finished row {i+1}")
                                progress_bar.progress((i + 1) / total_rows)

                            except Exception as row_error:
                                st.error(f"Error on row {i+1}: {row_error}")

                        st.success("🎉 Automation Complete!")
                        driver.quit()

                    except Exception as e:
                        st.error(f"System Error: {e}")
                        if 'driver' in locals(): driver.quit()

    except Exception as e:
        st.error(f"Error reading file: {e}")