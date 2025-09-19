# News Article Summarizer

This project demonstrates a news article summarizer that can be run either as a local web application with a UI or deployed as a Google Cloud Function.

## Project Overview

### Local UI Version

This version provides a local web application that summarizes news articles from a given URL. It uses Flask for the web interface, `newspaper3k` for article content extraction, and NLTK for a basic extractive text summarization. It also includes in-memory caching for repeated requests.

### Google Cloud Function Version

This version deploys a serverless function on Google Cloud Platform that takes a news article URL as input and returns a summarized version. It leverages Google Cloud's Vertex AI for NLP summarization and can optionally use Google Cloud Memorystore for Redis for caching.

## Features

-   Accepts a news article URL as input.
-   Fetches the article content using `newspaper3k`.
-   Summarizes the article using either a local NLTK-based extractive summarizer (Local UI) or Google Cloud's Vertex AI (Cloud Function).
-   Includes caching for repeated article fetches and summarizations (in-memory for Local UI, optional Redis for Cloud Function).
-   Provides either a minimal web UI (Local) or responds to a POST request (Cloud Function).

## Local UI: Setup and Installation

Follow these steps to set up and run the local web application.

1.  **Navigate to the project directory**

    ```bash
    cd news_summarizer
    ```

2.  **Create a Python Virtual Environment (recommended)**

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**

    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Local UI: How to Run

1.  **Ensure your virtual environment is active and dependencies are installed (as per "Setup and Installation" above).**

2.  **Run the Flask application:**

    ```bash
    python app.py
    ```

    You will see output similar to this, indicating the server is running:
    ```
     * Serving Flask app 'app'
     * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    ```

3.  **Access the application in your web browser:**

    Open `http://127.0.0.1:5000/` in your preferred web browser.

## Local UI: Usage

1.  Paste the URL of a news article into the input field.
2.  Click the "Summarize" button.
3.  The summarized version of the article will appear below.

## Google Cloud Function Deployment

This section outlines the steps to deploy the summarization function as a serverless Google Cloud Function.

### Prerequisites

*   **Google Cloud Account:** Ensure you have an active Google Cloud Platform account.
*   **Google Cloud SDK:** Install and initialize the Google Cloud SDK on your local machine.
    ```bash
    gcloud init
    ```
*   **Enable APIs:** Enable the Cloud Functions API, Vertex AI API, and (optionally for caching) Memorystore for Redis API for your project.
    ```bash
    gcloud services enable cloudfunctions.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable redis.googleapis.com
    ```



### Deploy the Google Cloud Function

Navigate to the `news_summarizer` directory in your terminal (the directory containing `main.py` and `requirements.txt` for the cloud function).

Use the following command to deploy your function:

```bash
gcloud functions deploy summarizeArticle \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point summarize_article \
    --source . \
    --set-env-vars GCP_PROJECT_ID=[YOUR_PROJECT_ID],GCP_REGION=[YOUR_REGION],REDIS_HOST=[YOUR_REDIS_HOST],REDIS_PORT=[YOUR_REDIS_PORT] \
    --timeout 300s \
    --memory 256MB
```

**Replace the following placeholders:**

*   `[YOUR_PROJECT_ID]`: Your Google Cloud Project ID.
*   `[YOUR_REGION]`: The Google Cloud region where you want to deploy your function (e.g., `us-central1`). This should also be the region of your Redis instance if used.
*   `[YOUR_REDIS_HOST]`: The host IP address of your Redis instance from Google Cloud Memorystore (only if Redis is used).
*   `[YOUR_REDIS_PORT]`: The port of your Redis instance (default is `6379`, only if Redis is used).

### Test the Google Cloud Function

After deployment, Google Cloud will provide you with a trigger URL for your function. Use that URL in the following `curl` command to test your function:

```bash
curl -X POST "YOUR_CLOUD_FUNCTION_URL" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.theguardian.com/world/2023/oct/26/israel-hamas-war-live-updates-gaza-latest-news"}'
```

## Result Demo

https://drive.google.com/file/d/19OgNnhQGDtFsm9Ob17QW-pYyXZ59oEmX/view?usp=sharing


## Reflection
This project provided a valuable exercise in adapting a serverless function concept to both a local environment and a cloud platform. A tricky aspect was managing NLTK's data downloads and newspaper3k's lxml dependency in the local setup, requiring specific package installations to resolve import errors.

## AI Usage
ChatGPT was instrumental in generating the initial Flask application structure, integrating newspaper3k, and setting up the NLTK-based summarizer. It also facilitated the creation of comprehensive README.md documentation, detailing both local and Google Cloud deployment steps, which was essential for covering all aspects of the user's evolving requirements.

