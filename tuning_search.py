"""
NewsAPI.org client module.
Handles interaction with the NewsAPI.org API.

Available modes:
- everything: Search all news articles from across the web
- top-headlines: Get top headlines for a country, category, or source
- sources: Get list of news sources available on the NewsAPI
"""

import requests
from typing import List, Dict, Optional
from config import Config


class NewsAPIClient:
    """Client for interacting with NewsAPI.org API."""
    
    # Available search modes
    MODE_EVERYTHING = "everything"
    MODE_TOP_HEADLINES = "top-headlines"
    MODE_SOURCES = "sources"
    
    def __init__(self):
        """Initialize the NewsAPI client."""
        Config.validate()
        self.api_key = Config.NEWS_API_KEY
        self.api_base = Config.NEWS_API_BASE
        self.timeout = Config.REQUEST_TIMEOUT
    
    def search(self, query: str, mode: str = MODE_EVERYTHING, **kwargs) -> Dict:
        """
        Search using the specified mode (everything, top-headlines, or sources).
        
        Args:
            query: The search term (for everything/top-headlines) or category (for sources)
            mode: The search mode - 'everything', 'top-headlines', or 'sources'
            **kwargs: Optional parameters:
                - language: Language code (en, pt, es, fr, de, etc.)
                - country: Country code (us, br, ar, au, etc.)
                - category: Category (business, entertainment, general, health, science, sports, technology)
                - page: Result page number (default: 1)
                - pageSize: Number of results per page (default: 10, max: 100)
                - sources: Comma-separated list of source IDs
                - domains: Comma-separated list of domains
                - from: Start date (YYYY-MM-DD)
                - to: End date (YYYY-MM-DD)
                - sortBy: Sort by (relevancy, popularity, publishedAt)
            
        Returns:
            Dictionary containing the search results
        """
        url = f"{self.api_base}/{mode}"
        headers = {
            "X-Api-Key": self.api_key
        }
        
        # Build query parameters
        params = {}
        if mode == self.MODE_SOURCES:
            params["category"] = query
        else:
            params["q"] = query
        
        # Add optional parameters
        if "language" in kwargs:
            params["language"] = kwargs["language"]
        if "country" in kwargs:
            params["country"] = kwargs["country"]
        if "category" in kwargs:
            params["category"] = kwargs["category"]
        if "page" in kwargs:
            params["page"] = kwargs["page"]
        # Default pageSize to 10 to limit articles for classification
        params["pageSize"] = kwargs.get("pageSize", 10)
        if "sources" in kwargs:
            params["sources"] = kwargs["sources"]
        if "domains" in kwargs:
            params["domains"] = kwargs["domains"]
        if "from" in kwargs:
            params["from"] = kwargs["from"]
        if "to" in kwargs:
            params["to"] = kwargs["to"]
        if "sortBy" in kwargs:
            params["sortBy"] = kwargs["sortBy"]
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            # Add query and mode to the response for display purposes
            result["query"] = query
            result["mode"] = mode
            return result
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "query": query,
                "mode": mode,
                "status": "failed"
            }
    
    def search_multiple(self, queries: List[str], mode: str = MODE_EVERYTHING, **kwargs) -> List[Dict]:
        """
        Search for multiple query terms on NewsAPI.
        
        Args:
            queries: List of search terms
            mode: The search mode - 'everything', 'top-headlines', or 'sources'
            **kwargs: Optional parameters passed to search method
            
        Returns:
            List of dictionaries containing search results for each query
        """
        results = []
        for query in queries:
            query = query.strip()
            if query:
                result = self.search(query, mode=mode, **kwargs)
                results.append(result)
        return results
    
    @classmethod
    def get_available_modes(cls) -> List[str]:
        """
        Get list of available search modes.
        
        Returns:
            List of available mode names
        """
        return [cls.MODE_EVERYTHING, cls.MODE_TOP_HEADLINES, cls.MODE_SOURCES]
    
    @classmethod
    def get_mode_description(cls, mode: str) -> str:
        """
        Get description for a search mode.
        
        Args:
            mode: The mode name
            
        Returns:
            Description of the mode
        """
        descriptions = {
            cls.MODE_EVERYTHING: "Search all news",
            cls.MODE_TOP_HEADLINES: "Top headlines",
            cls.MODE_SOURCES: "News sources"
        }
        return descriptions.get(mode, "Unknown mode")
    
    def format_results(self, results: List[Dict]) -> str:
        """
        Format search results for display.
        
        Args:
            results: List of search result dictionaries
            
        Returns:
            Formatted string representation of results
        """
        output = []
        output.append("=" * 80)
        output.append("NEWSAPI.ORG RESULTS")
        output.append("=" * 80)
        output.append("")
        
        for i, result in enumerate(results, 1):
            if "error" in result:
                mode = result.get('mode', 'everything')
                output.append(f"[{i}] Query: {result.get('query', 'Unknown')}")
                output.append(f"    Mode: {self.get_mode_description(mode)} ({mode})")
                output.append(f"    Status: FAILED - {result['error']}")
                output.append("")
            elif result.get("status") == "ok":
                mode = result.get('mode', 'everything')
                query = result.get('query', 'Unknown')
                output.append(f"[{i}] Query: {query}")
                output.append(f"    Mode: {self.get_mode_description(mode)} ({mode})")
                output.append("-" * 40)
                
                # Display total results
                total_results = result.get("totalResults", 0)
                output.append(f"    Total Results: {total_results}")
                output.append("")
                
                # Display articles or sources
                if mode == self.MODE_SOURCES:
                    if "sources" in result:
                        for j, source in enumerate(result["sources"], 1):
                            output.append(f"    Source {j}:")
                            output.append(f"        ID: {source.get('id', 'N/A')}")
                            output.append(f"        Name: {source.get('name', 'N/A')}")
                            output.append(f"        Description: {source.get('description', 'N/A')[:150]}...")
                            output.append(f"        Category: {source.get('category', 'N/A')}")
                            output.append(f"        Language: {source.get('language', 'N/A')}")
                            output.append(f"        Country: {source.get('country', 'N/A')}")
                            output.append("")
                else:
                    if "articles" in result:
                        for j, article in enumerate(result["articles"], 1):
                            output.append(f"    Article {j}:")
                            output.append(f"        Title: {article.get('title', 'N/A')}")
                            output.append(f"        Source: {article.get('source', {}).get('name', 'N/A')}")
                            output.append(f"        Author: {article.get('author', 'N/A')}")
                            output.append(f"        URL: {article.get('url', 'N/A')}")
                            output.append(f"        Published: {article.get('publishedAt', 'N/A')}")
                            description = article.get('description', 'N/A')
                            if len(description) > 200:
                                description = description[:200] + "..."
                            output.append(f"        Description: {description}")
                            output.append("")
            else:
                # Handle unexpected response format
                output.append(f"[{i}] Query: {result.get('query', 'Unknown')}")
                output.append(f"    Status: Unexpected response format")
                output.append(f"    Response: {result}")
                output.append("")
        
        output.append("=" * 80)
        return "\n".join(output)
