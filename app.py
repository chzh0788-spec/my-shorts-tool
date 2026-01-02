import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import zipfile
import io
from urllib.parse import urljoin

st.set_page_config(page_title="Shorts Hub Pro", layout="wide")

# --- 사이드바: API 키 관리 (비밀번호 가리기 해제) ---
with st.sidebar:
    st.header("🔑 API 키 선택")
    
    # Secrets에서 키 불러오기
    saved_keys = []
    if "api_keys" in st.secrets:
        saved_keys = list(st.secrets["api_keys"].values())
    
    # 키 선택 (가려지지 않게 처리)
    selected_key = st.selectbox("사용할 키를 골라주세요", saved_keys + ["직접 입력"])
    
    final_key = ""
    if selected_key == "직접 입력":
        final_key = st.text_input("API 키를 입력하세요", type="default")
    else:
        final_key = selected_key
    
    st.write(f"현재 선택된 키: `{final_key[:15]}...`" if final_key else "키를 선택해주세요.")

# --- 메인 1: 인기글 모으기 (구체화) ---
st.title("🔥 쇼츠 제작 통합 작업실")
st.subheader("🌐 오늘의 인기글 소재 찾기")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.error("디시 실베 (이슈/유머)")
    st.link_button("실베 바로가기", "https://gall.dcinside.com/board/lists?id=dcbest", use_container_width=True)
with col2:
    st.warning("펨코 포텐 (빠른 트렌드)")
    st.link_button("포텐 바로가기", "https://www.fmkorea.com/best", use_container_width=True)
with col3:
    st.info("네이트판 (썰/감동)")
    st.link_button("톡톡 바로가기", "https://pann.nate.com/talk/talker", use_container_width=True)
with col4:
    st.success("Genspark (정밀 분석)")
    st.link_button("젠스파크 검색", "https://www.genspark.ai/", use_container_width=True)

st.divider()

# --- 메인 2: 대본 생성 & 이미지 다운로드 ---
tab_script, tab_img = st.tabs(["📝 대본 제작 & 저장", "🖼️ 이미지 일괄 다운로드"])

with tab_script:
    c1, c2 = st.columns([1, 1])
    with c1:
        content = st.text_area("소재 내용을 붙여넣으세요.", height=300)
        btn = st.button("🚀 군림보 스타일 대본 생성", use_container_width=True)
    with c2:
        if btn:
            if not final_key: st.error("키를 먼저 설정해주세요!")
            else:
                try:
                    genai.configure(api_key=final_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res = model.generate_content(f"군림보 스타일 쇼츠 대본 써줘. [도입-본론-결론-구독유도] \n 내용: {content}")
                    st.success("대본 완성!")
                    st.write(res.text)
                    # 대본 저장 버튼
                    st.download_button("📥 대본(.txt) 저장하기", res.text, file_name="script.txt")
                except Exception as e: st.error(f"오류: {e}")

with tab_img:
    url = st.text_input("이미지를 뽑아낼 게시글 주소(URL)를 입력하세요.")
    if st.button("📸 모든 이미지 긁어오기"):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            imgs = soup.find_all('img')
            
            img_links = []
            for i in imgs:
                src = i.get('src') or i.get('data-src')
                if src:
                    full_url = urljoin(url, src)
                    if any(ext in full_url.lower() for ext in ['.jpg', '.jpeg', '.png']):
                        img_links.append(full_url)
            
            if img_links:
                st.write(f"찾은 이미지: {len(img_links)}개")
                zip_io = io.BytesIO()
                with zipfile.ZipFile(zip_io, 'w') as z:
                    for idx, link in enumerate(img_links):
                        try:
                            img_data = requests.get(link, headers=headers).content
                            z.writestr(f"image_{idx}.jpg", img_data)
                        except: continue
                st.download_button("🎁 이미지 전체 다운로드 (.zip)", zip_io.getvalue(), file_name="images.zip")
            else: st.warning("이미지를 찾을 수 없습니다.")
        except Exception as e: st.error(f"오류: {e}")
