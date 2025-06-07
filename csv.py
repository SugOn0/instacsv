import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="설문 결과 뷰어", layout="wide")
st.title("📋 설문 결과 뷰어")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

def render_image(base64_str):
    if pd.isna(base64_str) or not isinstance(base64_str, str):
        return "❌"
    return f'<img src="{base64_str}" width="100" height="100"/>'

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        st.success("✅ 파일 업로드 성공!")

        # 사진 처리
        if "사진" in df.columns:
            df_display = df.copy()
            df_display["사진"] = df_display["사진"].apply(render_image)
            st.markdown("### 전체 응답 결과")
            st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.dataframe(df)

        # 150개 랜덤 추출
        st.markdown("---")
        st.markdown("### 🎯 무작위 150명 추출")
        if st.button("150명 랜덤 추출하기"):
            sample_count = min(150, len(df))
            sample_df = df.sample(n=sample_count, random_state=random.randint(0, 9999))

            if "사진" in sample_df.columns:
                sample_df["사진"] = sample_df["사진"].apply(render_image)
                st.markdown(sample_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.dataframe(sample_df)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("CSV 파일을 업로드하면 결과가 여기에 표시됩니다.")
