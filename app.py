from flask import Flask, request, render_template, jsonify
from newspaper import Article
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
from heapq import nlargest
import functools

app = Flask(__name__)

# Download NLTK resources (only needed once)
nltk.download("stopwords")
nltk.download("punkt")


@functools.lru_cache(maxsize=128)  # Cache up to 128 most recent articles
def fetch_article_content(url):
    """
    Fetches the content of a news article from the given URL using newspaper3k.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error fetching and parsing article content from {url}: {e}")
        return None


@functools.lru_cache(maxsize=128)  # Cache up to 128 most recent summaries
def summarize_text_extractive(text, num_sentences=3):
    """
    Summarizes the given text using a basic extractive summarization technique (NLTK).
    """
    if not text:
        return ""

    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Filter out stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [
        word for word in words if word.isalnum() and word not in stop_words
    ]

    # Calculate word frequency
    word_freq = defaultdict(int)
    for word in filtered_words:
        word_freq[word] += 1

    if not word_freq:
        return ""

    # Calculate sentence scores based on word frequency
    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[i] += word_freq[word]

    # Get the top N sentences for the summary
    summarized_sentences = nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )
    summarized_sentences = sorted(summarized_sentences)

    if not summarized_sentences:
        return ""

    return " ".join([sentences[i] for i in summarized_sentences])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize_article_endpoint():
    data = request.get_json()
    article_url = data.get("url")

    if not article_url:
        return jsonify({"error": "URL is required"}), 400

    article_content = fetch_article_content(article_url)

    if not article_content:
        return jsonify({"error": "Could not fetch article content"}), 500

    summary = summarize_text_extractive(article_content)

    if not summary:
        return jsonify({"error": "Could not summarize article"}), 500

    return jsonify({"summary": summary})


if __name__ == "__main__":
    app.run(debug=True)
