from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .core import get_key_phrases


app = FastAPI()

form_html = """
    <form action="/search" method="get" class="form-center">
      <label for="search-box">Search arXiv</label>
      <input type="text" name="query" id="search-box">
      <button type="submit">Submit</button>
    </form>
"""


def build_html(body: str) -> str:
    return (
        """
<html>
  <head>
    <title>arXiv chaos</title>
    <style>
      html {
        padding: 40px;
        background-color: SlateGray;
      }

      label {
        color: AliceBlue;
      }

      table, th, td { 
        border: 1px solid;
        border-radius: 5px;
        padding: 5px;
        color: AliceBlue;
      }

      .center-table {
        margin-left: auto;
        margin-right: auto;
      }

      .form-center {
        display: flex;
        justify-content: center;
      }
    </style>
  </head>
"""
        f"  <body>{body}</body>"
        """
</html>
"""
    )


@app.get("/", response_class=HTMLResponse)
def read_item():
    return build_html(form_html)


@app.get("/search", response_class=HTMLResponse)
def read_query(query: str):
    ranked_phrases = get_key_phrases(query)
    html_table_rows = []
    for rp in ranked_phrases:
        html_table_rows.append(f"<tr><td>{rp.phrase}</td><td>{rp.score}</td></tr>")
    body = form_html + (
        """
    <table class="center-table">
      <tr>
        <th>Phrase</th>
        <th>Score</th>
      </tr>
"""
        f"      {''.join(html_table_rows)}"
        """
    </table>
"""
    )
    return build_html(body)
