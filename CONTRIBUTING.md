# Contributing to NSF I-Corps Automation

Thank you for your interest in improving this tool! This guide will help you understand how to modify the automation logic, especially if the target form structure changes.

## 💻 Development Environment

We use **Streamlit** for the UI and **Selenium** for the browser automation.

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

    For Windows:
    ```bash
    venv\Scripts\activate
    ```
2.  Install dev dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🧩 Project Structure

* `app.py`: The main entry point. Contains the UI logic and the Selenium automation loop.
* `packages.txt`: System-level dependencies for Streamlit Cloud (Chromium).
* `requirements.txt`: Python dependencies.

## 🔧 Updating Form Logic

The core automation logic is located inside the `Start Process` button block in `app.py`.

### Scenario: The Form Changed
If the online form questions change or the bot stops finding elements, you need to update the **Selectors**.

1.  Open the target form in your Chrome browser.
2.  Right-click the element (input box, radio button) and select **Inspect**.
3.  Look for the `id` attribute (e.g., `<input id="SingleLine7-arialabel" ...>`).
4.  Update the corresponding line in `app.py`:

```python
# Example: Updating the Evaluator Name field
# Old ID: SingleLine7-arialabel
# New ID: Text_Input_New_ID

# Find this line in app.py:
wait.until(EC.presence_of_element_located((By.ID, 'SingleLine7-arialabel')))

# Change to:
wait.until(EC.presence_of_element_located((By.ID, 'Text_Input_New_ID')))