# News Article Summarizer (Local UI)

This project provides a local web application that summarizes news articles from a given URL. It uses Flask for the web interface, `newspaper3k` for article content extraction, and NLTK for a basic extractive text summarization.

## Features

-   Accepts a news article URL via a web UI.
-   Fetches the article content using `newspaper3k`.
-   Summarizes the article using a simple NLTK-based extractive summarization technique.
-   Provides an in-memory cache for repeated article fetches and summarizations to improve performance.
-   Returns a short summary in the web interface.

## Setup and Installation

Follow these steps to set up and run the application locally.

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

## How to Run

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

## Usage

1.  Paste the URL of a news article into the input field.
2.  Click the "Summarize" button.
3.  The summarized version of the article will appear below.

## Troubleshooting

If you encounter a `ModuleNotFoundError` for `flask` or any other package, ensure your virtual environment is activated and you have run `pip install -r requirements.txt` successfully.
