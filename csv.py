import streamlit as st
import pandas as pd
import random
from io import BytesIO

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

        st.markdown("---")
        st.markdown("### 🎯 무작위 추출")

        # 뽑을 인원 수 입력 받기 (최대: 데이터 길이)
        sample_max = len(df)
        sample_num = st.number_input(
            "추출할 인원 수를 입력하세요",
            min_value=1,
            max_value=sample_max,
            value=min(150, sample_max),
            step=1
        )

        if st.button(f"{sample_num}명 랜덤 추출하기"):
            sample_df = df.sample(n=sample_num, random_state=random.randint(0, 9999))

            # 학년, 반, 번호 컬럼이 있으면 정렬
            sort_cols = [col for col in ["학년", "반", "번호"] if col in sample_df.columns]
            if sort_cols:
                sample_df = sample_df.sort_values(by=sort_cols)

            csv_for_download = sample_df.to_csv(index=False).encode("utf-8")

            st.success(f"✅ {sample_num}명 랜덤 추출 성공!")

            if "사진" in sample_df.columns:
                display_df = sample_df.copy()
                display_df["사진"] = display_df["사진"].apply(render_image)
                st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.dataframe(sample_df)

            st.download_button(
                label="💾 CSV로 저장하기",
                data=csv_for_download,
                file_name="랜덤_추출_결과.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("CSV 파일을 업로드하면 결과가 여기에 표시됩니다.")

