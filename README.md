# 🤖 NSF I-Corps Form Automation Tool

A Python-based web application designed to automate the data entry process for NSF I-Corps course evaluations. This tool reads data from an Excel spreadsheet, allows for user verification, and then uses a headless browser to automatically fill and submit the online evaluation forms.

## 🚀 Features

* **Excel Integration:** Upload standard NSF I-Corps evaluation spreadsheets (`.xlsx`).
* **Data Verification:** Review and edit data in an interactive table before submission.
* **Headless Automation:** Runs silently in the background (server-side) using Selenium and Chromium.
* **Cloud Ready:** Optimized for deployment on Streamlit Community Cloud.
* **Safe Mode:** Includes a "Test Mode" to verify form filling without actually submitting data.

## 🛠️ Setup & Installation

### Option 1: Cloud Deployment (Recommended)
This app is designed to run on **Streamlit Community Cloud**.
1.  [NSF I-Corps Form Automation Tool](https://nsf-teameval.streamlit.app/)

### Option 2: Local Development
If you want to run this on your own machine:

1.  **Prerequisites:**
    * Python 3.13+
    * Google Chrome installed
    * Git

2.  **Clone the Repo:**
    ```bash
    git clone https://github.com/bandlayash/jpec-team-eval-app.git
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## 📖 How to Use

1.  **Prepare your Excel File:** Ensure your spreadsheet has the standard columns (Evaluator Name, Team Name, Customer Interviews, etc.).
2.  **Upload:** Drag and drop your `.xlsx` file into the app.
3.  **Configure:**
    * **Sheet Name:** Select the tab containing the data.
    * **Header Row:** Adjust if your headers aren't on Row 1 (default is set to Row 3 / Index 2).
    * **Team Selection:** Choose the specific team you want to process.
4.  **Verify:** Check the data in the "Review Data" table. You can edit cells directly here if needed.
5.  **Run:**
    * Leave "Enable REAL Submission" **unchecked** to test.
    * Check "Enable REAL Submission" when you are ready to submit to the portal.
6.  **Monitor:** Watch the status bar as the bot processes each row.

## ⚠️ Troubleshooting

* **"Unable to obtain driver":** If running locally, ensure you have `webdriver-manager` installed. If on Cloud, check that `packages.txt` exists.
* **"Bad argument type":** This usually means the Excel header row selection is wrong. Try adjusting the "Header Row" input in the sidebar.
* **Form Not Filling:** If the target form URL changes, the specific HTML IDs (e.g., `Radio8_1`) might have changed. See the `CONTRIBUTING.md` for how to update selectors.

