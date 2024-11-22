import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

# Streamlit 페이지 설정
st.set_page_config(
    page_title="JCH OJT 챗봇 🌟",
    page_icon="🏢",
    layout="wide"
)

# CSS 스타일 적용
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        background-color: #0083B8;
    }
    .css-1d391kg {
        padding: 2rem;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("# 🏢 제이씨현시스템㈜ 신입사원 OJT 도우미 ")
st.markdown("### 🤖 무엇이든 물어보세요!")

# 회사 소개 섹션 추가
st.markdown("""
### 💪 제이씨현시스템㈜의 강점
- 🖥️ **PC 부품 시장 선도**
  - 메인보드 시장 점유율 20%
  - 그래픽카드 시장 점유율 20%
  
- 🌐 **다양한 사업 영역**
  - IT기기 리스/렌탈 비즈니스
  - 자체 브랜드 모니터 'UDEA', 'BattleG'
  - 콤스코프 광섬유케이블 솔루션
  
- 📈 **안정적인 기업 구조**
  - 코스닥 상장 기업
  - 다수의 계열사 보유
  - 장학재단 운영
""")

# 사이드바 수정
with st.sidebar:
    st.markdown("## 🏢 회사 소개")
    st.markdown("""
    제이씨현시스템㈜은 컴퓨터 관련 제품 및 드론, VR기기 등을 
    공급하는 코스닥 상장 기업입니다.
    
    ### 📌 주요 계열사
    - ㈜엘림넷
    - 디앤디컴㈜
    - 대아리드선㈜
    - 제이씨현온비즈㈜
    - ㈜솔레오
    - ㈜제이씨에이치인베스트먼트
    - (재)제이씨현장학재단
    """)
    
    st.markdown("## ℹ️ 안내사항")
    st.markdown("""
    - 👋 환영합니다!
    - 📚 OJT 관련 질문을 해주세요
    - 🔑 API 키는 안전하게 보관됩니다
    - 💡 명확한 질문을 해주세요
    """)
    
    st.markdown("## 🎯 주요 기능")
    st.markdown("""
    - OJT 문서 기반 답변
    - 실시간 채팅
    - 대화 기록 저장
    """)

# API 키 입력 섹션
if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = ""

col1, col2 = st.columns([3, 1])
with col1:
    api_key = st.text_input("🔑 Google API 키를 입력하세요:", 
                           value=st.session_state.GOOGLE_API_KEY,
                           type="password",
                           placeholder="API 키를 입력해주세요")

if api_key:
    st.session_state.GOOGLE_API_KEY = api_key
    genai.configure(api_key=api_key)

    # PDF 파일 읽기
    def read_pdf(file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    # PDF 파일 경로 설정
    pdf_path = "ojt.pdf"
    if os.path.exists(pdf_path):
        ojt_content = read_pdf(pdf_path)
    else:
        st.error("⚠️ PDF 파일을 찾을 수 없습니다.")
        st.stop()

    # 채팅 모델 설정
    model = genai.GenerativeModel('gemini-pro')

    # 채팅 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 구분선 추가
    st.markdown("---")
    
    # 채팅 컨테이너
    chat_container = st.container()
    
    with chat_container:
        # 채팅 기록 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("💭 질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 로딩 표시
        with st.spinner('🤔 답변을 생성하고 있습니다...'):
            # 컨텍스트와 함께 응답 생성
            context = f"""
            다음 JCH OJT 문서를 참고하여 질문에 답변해주세요:
            {ojt_content}
            
            질문: {prompt}
            """

            with st.chat_message("assistant", avatar="🤖"):
                response = model.generate_content(context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

else:
    st.warning("👉 계속하려면 API 키를 입력하세요.")

# 푸터 추가
st.markdown("---")
st.markdown("### 🌟 제이씨현시스템㈜ OJT 챗봇")
st.markdown("#### 신입사원분들의 성공적인 적응을 응원합니다! 💪")
