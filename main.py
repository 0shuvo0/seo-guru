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
        with st.spinner("Analyzing website... Please wait"):
            try:
                # Initialize analyzer
                analyzer = SEOAnalyzer(url)
                
                # Perform analysis
                analysis_results = analyzer.analyze()
                
                # Display results
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Overall SEO Score")
                    create_score_gauge(analysis_results['overall_score'])
                    
                    st.markdown("### Key Metrics")
                    create_metrics_chart(analysis_results['metrics'])
                
                with col2:
                    st.markdown("### Quick Stats")
                    st.metric("Page Load Time", f"{analysis_results['load_time']:.2f}s")
                    st.metric("Mobile Friendly", "Yes" if analysis_results['mobile_friendly'] else "No")
                    st.metric("SSL Certified", "Yes" if analysis_results['ssl_certified'] else "No")
                
                # Detailed Analysis Sections
                st.markdown("### Detailed Analysis")
                tabs = st.tabs(["Meta Tags", "Content", "Technical", "Improvements"])
                
                with tabs[0]:
                    st.markdown("#### Meta Tags Analysis")
                    for item in analysis_results['meta_analysis']:
                        st.markdown(f"- {item}")
                
                with tabs[1]:
                    st.markdown("#### Content Analysis")
                    for item in analysis_results['content_analysis']:
                        st.markdown(f"- {item}")
                
                with tabs[2]:
                    st.markdown("#### Technical Analysis")
                    for item in analysis_results['technical_analysis']:
                        st.markdown(f"- {item}")
                
                with tabs[3]:
                    st.markdown("#### Improvement Suggestions")
                    for item in analysis_results['improvements']:
                        st.markdown(f"- 🔸 {item}")
                
            except Exception as e:
                st.error(f"An error occurred while analyzing the website: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by SEO GURU")
