from pydantic import BaseModel


class ArticleMetadata(BaseModel):
    """arXiv article metadata
    Currently only using the `summary` field.
    """

    # published: str = ""
    # updated: str = ""
    # title: str = ""
    summary: str = ""
    # authors: list[str] = []
    # journal_ref: str = ""
    # arxiv_link: str = ""


class RankedPhrase(BaseModel):
    """Phrases scored and ranked by the RAKE algorithm."""

    phrase: str
    score: str
