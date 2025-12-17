# Base Python Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# --- 1. INSTALL CHROME & DEPENDENCIES ---
# We need wget, gnupg, and unzip to install Chrome/Chromedriver
RUN apt-get update && apt-get install -y wget gnupg2 unzip curl

# Install Google Chrome Stable
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# --- 2. INSTALL CHROMEDRIVER ---
# Detect Chrome version and install matching driver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    rm ~/chromedriver_linux64.zip && \
    mv -f ~/chromedriver /usr/bin/chromedriver && \
    chown root:root /usr/bin/chromedriver && \
    chmod 0755 /usr/bin/chromedriver

# --- 3. PYTHON SETUP ---
# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]