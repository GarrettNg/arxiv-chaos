import os


API_BASE_URL = os.environ.get(
    "ARXIV_API_BASE_URL", "https://export.arxiv.org/api/query?"
)
