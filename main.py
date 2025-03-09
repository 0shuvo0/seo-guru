import streamlit as st
import time
from seo_analyzer import SEOAnalyzer
from visualizer import create_score_gauge, create_metrics_chart
from utils import is_valid_url

# Page configuration
st.set_page_config(
    page_title="SEO GURU - Website Analysis Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #FF4B4B;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .category-title {
        color: #FF4B4B;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔍 SEO GURU")
st.markdown("### Comprehensive SEO Analysis Tool")

# URL Input
url = st.text_input("Enter website URL", placeholder="https://example.com")

if url:
    if not is_valid_url(url):
        st.error("Please enter a valid URL including http:// or https://")
    else:
        with st.spinner("Analyzing website... This may take a minute"):
            try:
                # Initialize analyzer
                analyzer = SEOAnalyzer(url)

                # Perform analysis
                results = analyzer.analyze()

                # Layout
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("### Overall SEO Score")
                    create_score_gauge(results['overall_score'])

                    st.markdown("### Performance Metrics")
                    create_metrics_chart(results['metrics'])

                with col2:
                    st.markdown("### Quick Stats")
                    st.metric("Page Load Time", f"{results['load_time']:.2f}s")
                    st.metric("Mobile Friendly", "✅ Yes" if results['mobile_friendly'] else "❌ No")
                    st.metric("SSL Certified", "✅ Yes" if results['ssl_certified'] else "❌ No")

                # Detailed Analysis Sections
                st.markdown("### Detailed Analysis")

                tabs = st.tabs([
                    "Meta Tags", "Content", "Technical", 
                    "Speed", "Security", "Links", "Improvements"
                ])

                # Meta Tags Analysis
                with tabs[0]:
                    st.markdown("#### 🏷️ Meta Tags Analysis")
                    for item in results['meta_analysis']:
                        if "optimal" in item.lower() or "found" in item.lower():
                            st.success(item)
                        elif "missing" in item.lower() or "too" in item.lower():
                            st.error(item)
                        else:
                            st.info(item)

                # Content Analysis
                with tabs[1]:
                    st.markdown("#### 📝 Content Analysis")

                    # Group content metrics
                    metrics = {}
                    keywords = []

                    for item in results['content_analysis']:
                        if "keywords" in item.lower():
                            keywords.append(item)
                        else:
                            category = item.split(':')[0] if ':' in item else 'General'
                            if category not in metrics:
                                metrics[category] = []
                            metrics[category].append(item)

                    # Display grouped metrics
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("##### Content Metrics")
                        for category, items in metrics.items():
                            with st.expander(category, expanded=True):
                                for item in items:
                                    st.write(item)

                    with col2:
                        st.markdown("##### Keyword Analysis")
                        for item in keywords:
                            st.write(item)

                # Technical Analysis
                with tabs[2]:
                    st.markdown("#### ⚙️ Technical Analysis")
                    col1, col2 = st.columns(2)

                    technical_items = results['technical_analysis']
                    mid = len(technical_items) // 2

                    with col1:
                        for item in technical_items[:mid]:
                            if "not" in item.lower() or "needs" in item.lower():
                                st.error(item)
                            else:
                                st.success(item)

                    with col2:
                        for item in technical_items[mid:]:
                            if "not" in item.lower() or "needs" in item.lower():
                                st.error(item)
                            else:
                                st.success(item)

                # Speed Analysis
                with tabs[3]:
                    st.markdown("#### ⚡ Speed Analysis")
                    for item in results['speed_analysis']:
                        if "slow" in item.lower() or "large" in item.lower():
                            st.error(item)
                        else:
                            st.success(item)

                # Security Analysis
                with tabs[4]:
                    st.markdown("#### 🔒 Security Analysis")
                    for item in results['security_analysis']:
                        if "not" in item.lower() or "risk" in item.lower():
                            st.error(item)
                        else:
                            st.success(item)

                # Link Analysis
                with tabs[5]:
                    st.markdown("#### 🔗 Link Analysis")
                    for item in results['link_analysis']:
                        if "broken" in item.lower():
                            st.error(item)
                        else:
                            st.info(item)

                # Improvements
                with tabs[6]:
                    st.markdown("#### 📈 Improvement Suggestions")

                    # Group improvements by category
                    grouped_improvements = {}
                    for item in results['improvements']:
                        category = item[1:item.find(']')]  # Extract category from [Category]
                        if category not in grouped_improvements:
                            grouped_improvements[category] = []
                        grouped_improvements[category].append(item[item.find(']')+1:].strip())

                    # Display grouped improvements
                    for category, improvements in grouped_improvements.items():
                        with st.expander(f"{category} Improvements", expanded=True):
                            for improvement in improvements:
                                st.markdown(f"🔸 {improvement}")

            except Exception as e:
                st.error(f"An error occurred while analyzing the website: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by SEO GURU")