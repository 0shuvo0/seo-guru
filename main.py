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

# Custom CSS with animations
st.markdown("""
    <style>
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

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
        animation: slideIn 0.5s ease-out;
    }

    .category-title {
        color: #FF4B4B;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        animation: fadeIn 0.5s ease-out;
    }

    .analysis-section {
        animation: slideIn 0.5s ease-out;
    }

    .stMarkdown {
        animation: fadeIn 0.5s ease-out;
    }

    .metric-value {
        animation: fadeIn 1s ease-out;
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
                # Show progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Initialize analyzer
                analyzer = SEOAnalyzer(url)
                status_text.text("Initializing analysis...")
                progress_bar.progress(20)
                time.sleep(0.3)  # Small delay for visual effect

                # Perform analysis
                status_text.text("Analyzing website content...")
                progress_bar.progress(40)
                time.sleep(0.3)

                results = analyzer.analyze()

                status_text.text("Processing results...")
                progress_bar.progress(80)
                time.sleep(0.3)

                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                time.sleep(0.3)

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                # Layout with staggered animations
                col1, col2 = st.columns([2, 1])

                with col1:
                    with st.container():
                        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                        st.markdown("### Overall SEO Score")
                        create_score_gauge(results['overall_score'])
                        st.markdown("</div>", unsafe_allow_html=True)
                        time.sleep(0.2)

                    with st.container():
                        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                        st.markdown("### Performance Metrics")
                        create_metrics_chart(results['metrics'])
                        st.markdown("</div>", unsafe_allow_html=True)
                        time.sleep(0.2)

                with col2:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("### Quick Stats")
                    st.metric("Page Load Time", f"{results['load_time']:.2f}s")
                    time.sleep(0.1)
                    st.metric("Mobile Friendly", "✅ Yes" if results['mobile_friendly'] else "❌ No")
                    time.sleep(0.1)
                    st.metric("SSL Certified", "✅ Yes" if results['ssl_certified'] else "❌ No")
                    st.markdown("</div>", unsafe_allow_html=True)

                # Detailed Analysis Sections
                st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                st.markdown("### Detailed Analysis")
                st.markdown("</div>", unsafe_allow_html=True)

                tabs = st.tabs([
                    "Meta Tags", "Content", "Technical", 
                    "Speed", "Security", "Links", "Improvements"
                ])

                # Meta Tags Analysis
                with tabs[0]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 🏷️ Meta Tags Analysis")
                    for item in results['meta_analysis']:
                        time.sleep(0.1)  # Slight delay for staggered appearance
                        if "optimal" in item.lower() or "found" in item.lower():
                            st.success(item)
                        elif "missing" in item.lower() or "too" in item.lower():
                            st.error(item)
                        else:
                            st.info(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Content Analysis
                with tabs[1]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 📝 Content Analysis")

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

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("##### Content Metrics")
                        for category, items in metrics.items():
                            time.sleep(0.1)
                            with st.expander(category, expanded=True):
                                for item in items:
                                    st.write(item)

                    with col2:
                        st.markdown("##### Keyword Analysis")
                        for item in keywords:
                            time.sleep(0.1)
                            st.write(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Technical Analysis
                with tabs[2]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### ⚙️ Technical Analysis")
                    col1, col2 = st.columns(2)

                    technical_items = results['technical_analysis']
                    mid = len(technical_items) // 2

                    with col1:
                        for item in technical_items[:mid]:
                            time.sleep(0.1)
                            if "not" in item.lower() or "needs" in item.lower():
                                st.error(item)
                            else:
                                st.success(item)

                    with col2:
                        for item in technical_items[mid:]:
                            time.sleep(0.1)
                            if "not" in item.lower() or "needs" in item.lower():
                                st.error(item)
                            else:
                                st.success(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Speed Analysis
                with tabs[3]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### ⚡ Speed Analysis")
                    for item in results['speed_analysis']:
                        time.sleep(0.1)
                        if "slow" in item.lower() or "large" in item.lower():
                            st.error(item)
                        else:
                            st.success(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Security Analysis
                with tabs[4]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 🔒 Security Analysis")
                    for item in results['security_analysis']:
                        time.sleep(0.1)
                        if "not" in item.lower() or "risk" in item.lower():
                            st.error(item)
                        else:
                            st.success(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Link Analysis
                with tabs[5]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 🔗 Link Analysis")
                    for item in results['link_analysis']:
                        time.sleep(0.1)
                        if "broken" in item.lower():
                            st.error(item)
                        else:
                            st.info(item)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Improvements
                with tabs[6]:
                    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                    st.markdown("#### 📈 Improvement Suggestions")

                    grouped_improvements = {}
                    for item in results['improvements']:
                        category = item[1:item.find(']')]
                        if category not in grouped_improvements:
                            grouped_improvements[category] = []
                        grouped_improvements[category].append(item[item.find(']')+1:].strip())

                    for category, improvements in grouped_improvements.items():
                        time.sleep(0.1)
                        with st.expander(f"{category} Improvements", expanded=True):
                            for improvement in improvements:
                                st.markdown(f"🔸 {improvement}")
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while analyzing the website: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by SEO GURU")