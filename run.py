import os
import urllib.request
from app.database import init_db

def download_index():
    files = {
        "_data/index/cpp_corpus.faiss": "https://media.githubusercontent.com/media/farmertakeover/Agent-Broncos_ITC-AI-Competition/main/_data/index/cpp_corpus.faiss",
        "_data/index/cpp_corpus.meta.jsonl": "https://media.githubusercontent.com/media/farmertakeover/Agent-Broncos_ITC-AI-Competition/main/_data/index/cpp_corpus.meta.jsonl",
        "_data/index/url_map.json": "https://raw.githubusercontent.com/farmertakeover/Agent-Broncos_ITC-AI-Competition/main/_data/index/url_map.json",
    }
    os.makedirs("_data/index", exist_ok=True)
    for path, url in files.items():
        if not os.path.exists(path):
            print(f"Downloading {path}...")
            urllib.request.urlretrieve(url, path)
            print(f"Done!")

download_index()
init_db()

from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))