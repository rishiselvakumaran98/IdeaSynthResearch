import requests
from typing import List, Optional, Dict
import dotenv
from time import sleep

class SemanticScholarAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.semanticscholar.org"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

    
    def suggest_paper_completions(self, prefix, limit=5) -> Dict:
        """
        GET /graph/v1/paper/autocomplete
        Suggest paper query completions based on a prefix.
        """
        url = f"{self.base_url}/graph/v1/paper/autocomplete"
        params = {"query": prefix, "limit": limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_papers_bulk(self, paper_ids, fields) -> Dict:
        """
        POST /graph/v1/paper/batch
        Get details for multiple papers at once.
        """
        url = f"{self.base_url}/graph/v1/paper/batch"
        params = {"fields": ",".join(fields)} if fields else {}
        data = {"ids": paper_ids}
        response = requests.post(url, headers=self.headers, params=params, json=data)
        return response.json()

    def paper_relevance_search(self, query, fields=None, limit=10, offset=0) -> Dict:
        """
        GET /graph/v1/paper/search
        Search papers by relevance to a query.
        """
        url = f"{self.base_url}/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "offset": offset
        }
        if fields:
            params["fields"] = ",".join(fields)
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def paper_bulk_search(self, query, fields=None, limit= 100, offset= 0) -> Dict:
        """
        GET /graph/v1/paper/search
        Bulk search papers by relevance to a query.
        """
        return self.paper_relevance_search(query, fields, limit, offset)

    def paper_title_search(self, title, fields = None) -> Dict:
        """
        GET /graph/v1/paper/search/match
        Search for a paper by exact title match.
        """
        url = f"{self.base_url}/graph/v1/paper/search/match"
        params = {"query": title}
        if fields:
            params["fields"] = ",".join(fields)
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_paper_details(self, paper_id, fields = None) -> Dict:
        """
        GET /graph/v1/paper/{paper_id}
        Get details about a paper.
        """
        url = f"{self.base_url}/graph/v1/paper/{paper_id}"
        params = {"fields": ",".join(fields)} if fields else {}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_paper_authors(self, paper_id, fields = None) -> Dict:
        """
        GET /graph/v1/paper/{paper_id}/authors
        Get details about a paper's authors.
        """
        url = f"{self.base_url}/graph/v1/paper/{paper_id}/authors"
        params = {"fields": ",".join(fields)} if fields else {}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_paper_citations(self, paper_id, fields= None, limit= 10, offset= 0) -> Dict:
        """
        GET /graph/v1/paper/{paper_id}/citations
        Get details about a paper's citations.
        """
        url = f"{self.base_url}/graph/v1/paper/{paper_id}/citations"
        params = {
            "limit": limit,
            "offset": offset
        }
        if fields:
            params["fields"] = ",".join(fields) # type: ignore
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_paper_references(self, paper_id, fields= None, limit= 10, offset = 0) -> Dict:
        """
        GET /graph/v1/paper/{paper_id}/references
        Get details about a paper's references.
        """
        url = f"{self.base_url}/graph/v1/paper/{paper_id}/references"
        params = {
            "limit": limit,
            "offset": offset
        }
        if fields:
            params["fields"] = ",".join(fields) # type: ignore
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    # Recommendations API Methods

    def get_recommendations_for_paper(self, paper_id, fields= None, limit= 10) -> Dict:
        """
        GET /recommendations/v1/papers/forpaper/{paper_id}
        Get recommended papers for a single positive example paper.
        """
        url = f"{self.base_url}/recommendations/v1/papers/forpaper/{paper_id}"
        params = {"limit": limit}
        if fields:
            params["fields"] = ",".join(fields) # type: ignore
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_recommendations_for_papers(self, positive_paper_ids, negative_paper_ids= None, fields= None, limit= 10) -> Dict:
        """
        POST /recommendations/v1/papers
        Get recommended papers for lists of positive and negative example papers.
        """
        url = f"{self.base_url}/recommendations/v1/papers"
        params = {"limit": limit}
        if fields:
            params["fields"] = ",".join(fields) # type: ignore
        data = {
            "positivePaperIds": positive_paper_ids,
            "negativePaperIds": negative_paper_ids or []
        }
        response = requests.post(url, headers=self.headers, params=params, json=data)
        return response.json()


if __name__ == "__main__":
    api = SemanticScholarAPI(api_key=dotenv.get_key('.env', 'SEMANTIC_SCHOLAR_API_KEY'))

    suggestions = api.suggest_paper_completions(prefix="machine learning")
    print("Query: 'machine learning'", ', Limit:', 5)
    print("Suggestions:", suggestions)

    # Get details for multiple papers
    paper_ids = ["649def34f8be52c8b66281af98ae884c09aef38b", "ARXIV:2106.15928"] #["10.1145/3368089.3409742", "10.1145/3375637.3392410"]
    papers = api.get_papers_bulk(paper_ids=paper_ids, fields=["title", "authors", "year"])
    print("Paper IDs:", paper_ids)
    print("Papers:", papers)

    # Search papers by relevance
    search_results = api.paper_relevance_search(query="deep learning", fields=["title", "abstract"], limit=1)
    print("Query: 'deep learning'", ', Limit: ', 1)
    print("Search Results:", search_results)

    # Get paper details
    paper_detail = api.get_paper_details(paper_id="649def34f8be52c8b66281af98ae884c09aef38b", fields=["title", "abstract", "authors"])
    print("Paper ID: 649def34f8be52c8b66281af98ae884c09aef38b")
    print("Paper Detail:", paper_detail)

    # Get recommendations for a paper
    recommendations = api.get_recommendations_for_paper(paper_id="360ca02e6f5a5e1af3dce4866a257aafc2d6d6f5", fields=["title", "authors"], limit=5)
    print("Relevant papers for Machine learning - a probabilistic perspective")
    print("Recommendations:", recommendations)

    # Example: Get recommended papers using lists of positive and negative papers
    print("\nGetting recommended papers using positive and negative examples...")

    positive_papers = ["10.1145/3368089.3409742"]  # e.g., Deep Learning paper
    negative_papers = ["10.1145/3459637.3482261"]  # e.g., Unrelated topic paper

    print("Positive Papers:", api.get_papers_bulk(paper_ids=positive_papers, fields=["title"]))
    print("Negative Papers:", api.get_papers_bulk(paper_ids=negative_papers, fields=["title"]))
    sleep(2)  # Sleep to avoid rate limiting from Semantic Scholar API
    recommended = api.get_recommendations_for_papers(
        positive_paper_ids=positive_papers,
        negative_paper_ids=negative_papers,
        fields=["title", "abstract", "authors", "venue", "year"],
        limit=5
    )

    print("Recommended Papers:")
    for rec in recommended.get("recommendedPapers", []):
        print(f"- {rec.get('title')} ({rec.get('year')})")
