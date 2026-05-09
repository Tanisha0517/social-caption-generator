import streamlit as st
from groq import Groq

st.set_page_config(page_title="Social Media Caption Generator", page_icon="✨", layout="centered")

st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; border: none; border-radius: 10px;
        padding: 12px 30px; font-size: 16px; font-weight: 600; width: 100%;
    }
    .caption-box {
        background: white; border: 2px solid #667eea;
        border-radius: 12px; padding: 16px 20px; margin: 10px 0;
        font-size: 15px; line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# ✨ Caption Generator")
st.markdown("##### AI-powered captions for your social media posts")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_xxxxxxxxxxxx")
    st.markdown("[Get free API key →](https://console.groq.com)")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("📱 Platform", ["Instagram", "Twitter / X", "LinkedIn", "Facebook"])
with col2:
    tone = st.selectbox("🎭 Tone", ["Funny", "Inspirational", "Professional", "Casual", "Romantic"])

topic = st.text_area("📝 Topic / Description", placeholder="e.g. My trip to Goa, Morning workout...", height=100)
count = st.slider("Number of captions", 1, 5, 3)

if st.button("✨ Generate Captions"):
    if not api_key:
        st.error("⚠️ Sidebar mein API key daalo!")
    elif not topic.strip():
        st.warning("⚠️ Topic likho pehle!")
    else:
        with st.spinner("🤖 Generating..."):
            try:
                client = Groq(api_key=api_key)
                prompt = f"""Generate exactly {count} captions for {platform}.
Topic: {topic}, Tone: {tone}
- Add emojis and 3-5 hashtags
- Separate each caption with ---
- Return ONLY captions, nothing else"""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                output = response.choices[0].message.content.strip()
                captions = [c.strip() for c in output.split("---") if c.strip()]

                st.success(f"✅ {len(captions)} captions ready!")
                for i, cap in enumerate(captions, 1):
                    st.markdown(f"**Caption {i}:**")
                    st.code(cap, language=None)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.divider()
st.markdown('<p style="text-align:center;color:#aaa;">Built with Streamlit + Groq AI ✨</p>', unsafe_allow_html=True)




# api key : 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