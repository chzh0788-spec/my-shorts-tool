import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="Shorts AI Master", page_icon="🎬", layout="wide")

st.title("🚀 쇼츠 대본 제작기 (Gemini 무료 버전)")
st.info("구글 API를 사용하여 무료로 대본을 생성합니다.")

# 1. 커뮤니티 링크
with st.expander("🌐 소재 찾으러 가기 (커뮤니티 인기글)", expanded=True):
    cols = st.columns(4)
    links = [("디시 실베", "https://gall.dcinside.com/board/lists?id=dcbest"), 
             ("펨코 포텐", "https://www.fmkorea.com/best"), 
             ("네이트판", "https://pann.nate.com/talk/talker"), 
             ("더쿠 HOT", "https://theqoo.net/hot")]
    for i, (name, url) in enumerate(links):
        cols[i].link_button(name, url, use_container_width=True)

st.divider()

# 2. 입력창 및 설정
col_in, col_set = st.columns([2, 1])

with col_in:
    raw_text = st.text_area("✍️ 커뮤니티 글 본문을 복사해서 넣어주세요.", height=300)

with col_set:
    st.subheader("⚙️ 설정")
    api_key = st.text_input("🔑 Gemini API Key를 입력하세요", type="password")
    tone = st.selectbox("📣 대본 스타일", ["군림보 (빠른 전개/이슈)", "미스테리 (공포/기괴)", "감성 썰 (공감)"])

# 3. 실행 및 결과
if st.button("🚀 AI 대본 생성 시작", use_container_width=True):
    if not api_key:
        st.warning("Google AI Studio에서 받은 API 키를 입력해주세요!")
    elif not raw_text:
        st.error("분석할 내용을 넣어주세요!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            with st.spinner("AI가 고퀄리티 대본을 뽑아내고 있습니다..."):
                prompt = f"""
                너는 유튜버 '군림보' 스타일의 쇼츠 대본 작가야. 
                제공된 커뮤니티 글을 바탕으로 시청자가 끝까지 보게 만드는 쇼츠 대본을 작성해줘.

                [제약 조건]
                1. 0~3초: 사람들의 호기심을 자극하는 강렬한 후킹 멘트로 시작할 것.
                2. 본론: 핵심 내용을 3가지 포인트로 요약해서 빠르게 전개할 것.
                3. 말투: "~라고 하네요", "~라는 소식입니다" 처럼 빠르고 명확한 군림보 특유의 뉴스톤 사용.
                4. 마지막: "구독하고 더 많은 이슈를 확인하세요!"라는 문구 포함.

                내용: {raw_text}
                """
                response = model.generate_content(prompt)
                
                st.success("✅ 대본 생성이 완료되었습니다!")
                st.markdown("---")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"오류 발생: {e}")
