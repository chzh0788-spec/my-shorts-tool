import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Gunlimbo Style Shorts Helper", layout="wide")

st.title("🔥 군림보 스타일 쇼츠 대본 제작기")

# 1. 커뮤니티 퀵 링크 (소재 찾기)
st.subheader("🌐 실시간 인기글 모니터링")
cols = st.columns(4)
with cols[0]:
    st.link_button("디시 실베", "https://gall.dcinside.com/board/lists?id=dcbest")
with cols[1]:
    st.link_button("펨코 포텐", "https://www.fmkorea.com/best")
with cols[2]:
    st.link_button("네이트판 톡톡", "https://pann.nate.com/talk/talker")
with cols[3]:
    st.link_button("더쿠 HOT", "https://theqoo.net/hot")

st.divider()

# 2. 대본 생성 섹션
st.subheader("📝 소재 입력 및 대본 생성")
raw_text = st.text_area("커뮤니티에서 복사한 글 본문을 넣어주세요.", height=200)

col1, col2 = st.columns([1, 1])

with col1:
    tone = st.selectbox("대본 톤 설정", ["군림보 뉴스 스타일", "감성적인 썰 읽기", "긴박한 미스테리"])
    api_key = st.text_input("Claude API Key를 입력하세요 (선택)", type="password")

with col2:
    if st.button("AI 대본 생성 시작"):
        if raw_text:
            st.info("✅ 생성된 대본 (예시)")
            st.markdown(f"""
            **[00:00~00:03 - 후킹]** "여러분, 이거 진짜일까요? 지금 난리 난 소식입니다!"
            
            **[00:03~00:40 - 본문]**
            "최근 한 커뮤니티에 올라온 글에 따르면... {raw_text[:50]}... (중략) ... 결국 이렇게 결론이 났다고 하네요."
            
            **[00:40~00:50 - 아웃트로]**
            "여러분은 어떻게 생각하시나요? 댓글로 남겨주세요! 구독하면 더 빠른 소식을 받아보실 수 있습니다."
            """)
        else:
            st.error("내용을 입력해주세요!")

# 3. 사이트 분류 및 관리
st.sidebar.header("📂 카테고리 분류")
category = st.sidebar.multiselect("소재 성격", ["IT/테크", "사회이슈", "유머/썰", "감동/실화"])
