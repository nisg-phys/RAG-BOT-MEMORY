
import re

def preprocess_query(query: str) -> str:
    """
    Preprocess user query before retrieval.

    Current steps:
    - strip whitespace
    - normalize spaces
    - remove accidental newlines

    Future extensions:
    - query rewriting
    - keyword expansion
    - spell correction
    """

    if not query:
        return ""

    # Remove extra whitespace
    query = query.strip()

    # Normalize spaces
    query = re.sub(r"\s+", " ", query)

    return query
