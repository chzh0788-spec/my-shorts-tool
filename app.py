import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import io
import zipfile
from urllib.parse import urljoin

# 페이지 설정
st.set_page_config(page_title="Shorts AI Pro Max", page_icon="🎬", layout="wide")

st.title("🚀 쇼츠 대본 & 이미지 마스터")

# 1. API 키 관리 섹션 (사이드바)
if 'api_keys' not in st.session_state:
    st.session_state['api_keys'] = []

with st.sidebar:
    st.header("🔑 API 키 관리")
    new_key = st.text_input("새 API 키 추가", type="default") # 비밀번호 가리기 해제
    if st.button("키 저장"):
        if new_key and new_key not in st.session_state['api_keys']:
            st.session_state['api_keys'].append(new_key)
            st.success("키가 추가되었습니다!")
    
    selected_key = st.selectbox("사용할 API 키 선택", st.session_state['api_keys'] if st.session_state['api_keys'] else ["등록된 키 없음"])

st.divider()

# 메인 화면 구성
tab1, tab2 = st.tabs(["📝 대본 생성기", "🖼️ 이미지 다운로더"])

# --- 탭 1: 대본 생성기 ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("소재 입력")
        raw_text = st.text_area("커뮤니티 글 본문을 붙여넣으세요.", height=300)
        generate_btn = st.button("🚀 대본 생성 시작", use_container_width=True)

    with col2:
        st.subheader("결과물")
        if generate_btn:
            if selected_key == "등록된 키 없음":
                st.error("API 키를 먼저 등록하고 선택해주세요!")
            elif not raw_text:
                st.warning("내용을 입력해주세요!")
            else:
                try:
                    genai.configure(api_key=selected_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    with st.spinner("AI 집필 중..."):
                        prompt = f"군림보 스타일 쇼츠 대본 써줘. 후킹-본문-구독유도 순서로.\n내용: {raw_text}"
                        response = model.generate_content(prompt)
                        result_text = response.text
                        st.success("대본 완성!")
                        st.markdown(result_text)
                        
                        # 대본 저장(다운로드) 기능
                        st.download_button(
                            label="📥 대본 .txt 파일로 저장",
                            data=result_text,
                            file_name="shorts_script.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"오류: {e}")

# --- 탭 2: 이미지 다운로더 ---
with tab2:
    st.subheader("🔗 커뮤니티 이미지 일괄 추출")
    target_url = st.text_input("이미지를 뽑아낼 사이트 주소(URL)를 입력하세요.")
    
    if st.button("이미지 모두 가져오기"):
        if target_url:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(target_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 이미지 태그 찾기 (사이트마다 구조가 다르므로 일반적인 태그 검색)
                img_tags = soup.find_all('img')
                img_urls = []
                
                for img in img_tags:
                    src = img.get('src') or img.get('data-src')
                    if src:
                        full_url = urljoin(target_url, src)
                        if any(ext in full_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                            img_urls.append(full_url)
                
                if img_urls:
                    st.write(f"총 {len(img_urls)}개의 이미지를 찾았습니다.")
                    
                    # 압축 파일 생성
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                        for i, url in enumerate(img_urls):
                            try:
                                img_data = requests.get(url, headers=headers).content
                                zip_file.writestr(f"image_{i+1}.jpg", img_data)
                            except:
                                continue
                    
                    st.download_button(
                            label="🎁 이미지 전체 다운로드 (.zip)",
                            data=zip_buffer.getvalue(),
                            file_name="images.zip",
                            mime="application/zip"
                    )
                    
                    # 미리보기
                    cols = st.columns(3)
                    for idx, url in enumerate(img_urls[:9]): # 최대 9개 미리보기
                        cols[idx%3].image(url, use_column_width=True)
                else:
                    st.warning("이미지를 찾지 못했습니다. 사이트 보안 정책 때문일 수 있습니다.")
            except Exception as e:
                st.error(f"이미지 추출 중 오류 발생: {e}")

# 하단 퀵 링크 (사용자 편의)
st.divider()
st.subheader("🌐 빠른 이동")
st.link_button("Genspark 바로가기", "https://www.genspark.ai/")
