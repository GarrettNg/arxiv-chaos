import urllib.request

import feedparser
from rake_nltk import Rake

from .config import API_BASE_URL
from .models import ArticleMetadata, RankedPhrase


def fetch(
    search_query: str,
    start_index: int = 0,
    max_results: int = 10,
    sort_by: str = "submittedDate",
    api_base_url=API_BASE_URL,
) -> bytes:
    """Retrieve query data from arXiv REST API.

    :param search_query: arXiv search query
    :param start_index: initial index for search results
    :param max_results: max number of search results to request
    :param sort_by: search result sorting method
    :param api_base_url: arXiv API URL
    :returns: HTTP response (XML) from arXiv
    """
    response_data = None
    search_url = f"{api_base_url}search_query={search_query}&start={start_index}&sortBy={sort_by}&max_results={max_results}"
    with urllib.request.urlopen(search_url) as res:
        response_data = res.read()
        if res.status != 200:
            print("error:", response.status)
    if response_data == None:
        print("error: no response")
    return response_data


def clean(input_str: str) -> str:
    """Remove and/or replace unwanted characters (such as newlines) in an input string.

    :param input_str: the string to be cleaned
    :returns: cleaned input string
    """
    cleaned_str = ""
    cleaned_str = input_str.replace("\n", " ")  # replace newlines with spaces
    # latex can bork the keyword extraction so that should probably be stripped, possibly via regex
    return cleaned_str


def parse(xml_response: bytes) -> list[ArticleMetadata]:
    """Extract abstracts from XML response data.

    :param xml_response: XML response data to be parsed
    :returns: list of article metadata
    """
    articles = []
    d = feedparser.parse(xml_response)
    for entry in d.entries:
        metadata = {}
        if entry.summary is not None:
            metadata["summary"] = clean(entry.summary)
            articles.append(ArticleMetadata(**metadata))
    return articles


def process(
    articles: list[ArticleMetadata], num_phrases: int = 10
) -> list[RankedPhrase]:
    """Extract keywords from article abstracts.

    :param articles: list of article metadata
    :param num_phrases: number of phrases to show in descending score order
    :returns: list of RankedPhrase objects
    """
    num_results = min(num_phrases, len(articles))
    joined_abstracts = ""
    for a in articles:
        joined_abstracts += a.summary
    rake = Rake()
    rake.extract_keywords_from_text(joined_abstracts)
    ranked_phrases = rake.get_ranked_phrases_with_scores()[:num_results]
    return [RankedPhrase(phrase=rp[1], score=rp[0]) for rp in ranked_phrases]


def get_key_phrases(query: str) -> list[RankedPhrase]:
    """Run pipeline to query arXiv for abstracts and extract keywords.

    :param query: arXiv search query
    :returns: list of RankedPhrase objects
    """
    cleaned_query = query.replace(" ", "+")  # url cannot contain space
    res = fetch(f"all:{cleaned_query}")
    articles = parse(res)
    return process(articles)
