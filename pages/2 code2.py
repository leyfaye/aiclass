import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image, UnidentifiedImageError
import io


hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""


st.markdown(hide_github_icon, unsafe_allow_html=True)


def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)


# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"


# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)


# secrets.toml 파일에서 gemini_api_key1 값 가져오기
api_key = secrets["api_key"]


# Gemini API 키 설정
genai.configure(api_key=api_key)


# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("핸드폰 사진 업로드")


# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
    with st.spinner("이미지를 분석중입니다. 잠시만 기다려주세요..."):
        try:
            # 이미지 바이트 문자열로 변환
            img_bytes = uploaded_file.read()


            # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
            img = Image.open(io.BytesIO(img_bytes))


            model = genai.GenerativeModel('gemini-1.5-flash')


            # Generate content
            response = model.generate_content([
                "이 사진은 동물의 사진입니다. 동물의 이름을 최대한 추측해서 판별해주세요. "
                "동물의 모습과 습성, 서식지 등을 학생에게 설명하듯이 자세히 한글로 설명해 주세요. "
                "더불어 동물을 사랑하고 생명을 존중할 수 있도록 마지막에 이야기를 해주세요.", img
            ])


            # Resolve the response
            response.resolve()


            # 결과 표시
            st.image(img)  # 업로드된 사진 출력
            st.markdown(response.text)
        except UnidentifiedImageError:
            st.error("업로드된 파일이 유효한 이미지 파일이 아닙니다. 다른 파일을 업로드해 주세요.")
else:
    st.markdown("핸드폰 사진을 업로드하세요.")
