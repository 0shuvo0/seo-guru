import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse
import whois
from datetime import datetime
import time

class SEOAnalyzer:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def analyze(self):
        """Perform complete SEO analysis of the website"""
        start_time = time.time()
        
        # Fetch page content
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract main text content
        downloaded = trafilatura.fetch_url(self.url)
        text_content = trafilatura.extract(downloaded)
        
        # Perform various analyses
        meta_analysis = self.analyze_meta_tags(soup)
        content_analysis = self.analyze_content(soup, text_content)
        technical_analysis = self.analyze_technical(response)
        improvements = self.generate_improvements(meta_analysis, content_analysis, technical_analysis)
        
        # Calculate scores
        scores = self.calculate_scores(meta_analysis, content_analysis, technical_analysis)
        
        return {
            'overall_score': scores['overall'],
            'metrics': {
                'Meta Tags': scores['meta'],
                'Content': scores['content'],
                'Technical': scores['technical']
            },
            'load_time': time.time() - start_time,
            'mobile_friendly': self.check_mobile_friendly(),
            'ssl_certified': self.url.startswith('https'),
            'meta_analysis': meta_analysis,
            'content_analysis': content_analysis,
            'technical_analysis': technical_analysis,
            'improvements': improvements
        }

    def analyze_meta_tags(self, soup):
        """Analyze meta tags and their optimization"""
        analysis = []
        
        # Title analysis
        title = soup.title.string if soup.title else None
        if title:
            if len(title) < 30:
                analysis.append("Title tag is too short (recommended: 50-60 characters)")
            elif len(title) > 60:
                analysis.append("Title tag is too long (recommended: 50-60 characters)")
            else:
                analysis.append("Title tag length is optimal")
        else:
            analysis.append("Missing title tag")
        
        # Meta description analysis
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_length = len(meta_desc['content'])
            if desc_length < 120:
                analysis.append("Meta description is too short (recommended: 120-155 characters)")
            elif desc_length > 155:
                analysis.append("Meta description is too long (recommended: 120-155 characters)")
            else:
                analysis.append("Meta description length is optimal")
        else:
            analysis.append("Missing meta description")
        
        return analysis

    def analyze_content(self, soup, text_content):
        """Analyze page content"""
        analysis = []
        
        # Heading structure
        headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        if headings['h1'] == 0:
            analysis.append("Missing H1 heading")
        elif headings['h1'] > 1:
            analysis.append("Multiple H1 headings detected (recommended: only one)")
        
        # Image analysis
        images = soup.find_all('img')
        images_without_alt = len([img for img in images if not img.get('alt')])
        if images_without_alt > 0:
            analysis.append(f"Found {images_without_alt} images without alt text")
        
        # Content length
        if text_content:
            word_count = len(text_content.split())
            if word_count < 300:
                analysis.append("Content length is too short (recommended: minimum 300 words)")
            else:
                analysis.append(f"Good content length: {word_count} words")
        
        return analysis

    def analyze_technical(self, response):
        """Analyze technical aspects"""
        analysis = []
        
        # Response time
        if response.elapsed.total_seconds() > 2:
            analysis.append("Slow page load time (> 2 seconds)")
        
        # URL structure
        parsed_url = urlparse(self.url)
        if len(parsed_url.path.split('/')) > 4:
            analysis.append("URL structure is too deep (recommended: maximum 3 levels)")
        
        # SSL certificate
        if not self.url.startswith('https'):
            analysis.append("Website is not using HTTPS")
        
        return analysis

    def check_mobile_friendly(self):
        """Basic mobile-friendly check"""
        try:
            response = requests.get(self.url, headers={**self.headers, 'User-Agent': 'Mobile'})
            return response.status_code == 200
        except:
            return False

    def calculate_scores(self, meta_analysis, content_analysis, technical_analysis):
        """Calculate scores for different aspects"""
        # Simple scoring system based on number of issues
        meta_score = 100 - (len([x for x in meta_analysis if 'Missing' in x or 'too' in x]) * 20)
        content_score = 100 - (len([x for x in content_analysis if 'Missing' in x or 'too' in x]) * 15)
        technical_score = 100 - (len([x for x in technical_analysis if 'Slow' in x or 'not' in x]) * 25)
        
        # Ensure scores are within 0-100 range
        meta_score = max(0, min(100, meta_score))
        content_score = max(0, min(100, content_score))
        technical_score = max(0, min(100, technical_score))
        
        # Calculate overall score
        overall_score = (meta_score + content_score + technical_score) / 3
        
        return {
            'overall': overall_score,
            'meta': meta_score,
            'content': content_score,
            'technical': technical_score
        }

    def generate_improvements(self, meta_analysis, content_analysis, technical_analysis):
        """Generate improvement suggestions based on analysis"""
        improvements = []
        
        for issue in meta_analysis + content_analysis + technical_analysis:
            if any(keyword in issue.lower() for keyword in ['missing', 'too', 'slow', 'multiple']):
                suggestion = issue.replace('Missing', 'Add')
                suggestion = suggestion.replace('too short', 'increase length of')
                suggestion = suggestion.replace('too long', 'reduce length of')
                improvements.append(suggestion)
        
        return improvements
