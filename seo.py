import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# Function to fetch SEO data
def get_seo_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error if request fails
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract meta data
        title = soup.title.string if soup.title else "No Title Found"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else "No Description Found"
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = meta_keywords["content"] if meta_keywords else "No Keywords Found"

        # Extract text and analyze top keywords
        text = soup.get_text()
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())  # Words with 4+ letters
        common_words = Counter(words).most_common(10)  # Get top 10 keywords

        return {
            "Title": title,
            "Meta Description": description,
            "Meta Keywords": keywords,
            "Top Keywords": common_words
        }

    except requests.exceptions.RequestException as e:
        return {"Error": f"Failed to fetch data: {e}"}

# Function to generate HTML report
def generate_html(seo_data):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analysis Report</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>SEO Analysis Report</h1>
        <p class="text-gray-600">Generated using Python & BeautifulSoup</p>

        <h2>Title:</h2>
        <p>{seo_data.get("Title", "N/A")}</p>

        <h2>Meta Description:</h2>
        <p>{seo_data.get("Meta Description", "N/A")}</p>

        <h2>Meta Keywords:</h2>
        <p>{seo_data.get("Meta Keywords", "N/A")}</p>

        <h2>Top Keywords:</h2>
        <ul>
            {''.join(f'<li>{word} ({count} times)</li>' for word, count in seo_data.get("Top Keywords", []))}
        </ul>
    </div>
</body>
</html>
"""
    
    with open("seo_report.html", "w", encoding="utf-8") as file:
        file.write(html_content)

# Run the script
if __name__ == "__main__":
    url = input("Enter website URL: ")  # Take input from the user
    seo_data = get_seo_data(url)
    generate_html(seo_data)

    print("\n✅ SEO Report generated successfully! Open 'seo_report.html' in your browser.")
