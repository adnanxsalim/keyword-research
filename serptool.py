import requests
from bs4 import BeautifulSoup

class SERPAnalyzer:
    def analyze_serp(self, keyword):
        search_url = f"https://www.google.com/search?q={keyword}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        top_results = soup.select('.tF2Cxc')  # CSS selector for search results
        results = [result.get_text() for result in top_results]
        return results

# Usage
if __name__ == "__main__":
    keyword = input("Enter a Keyword: ")

    serp_analyzer = SERPAnalyzer()
    serp_results = serp_analyzer.analyze_serp(keyword)
    
    print("Top SERP Results:")
    for index, result in enumerate(serp_results, start=1):
        print(f"{index}. {result}")