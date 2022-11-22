import streamlit as st 

# title 쓰기
st.title('제목 쓰세요')
# 그냥 text 쓰기 
st.write('아무거나 쓰세요')
# markdown tag 쓰고 싶으면
st.markdown('<h1>태그를 쓸 수 있어요</h1>')
# user input 받기 
st.text_input('사용자 입력을 받아보세요: ')

# 이외에도 다양한 기능 엄청 많다~ 
st.button 
st.sidebar 

# 맵
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st


# 위치정보 상세 (단, data에 위도 경도 컬럼이 있어야 함)
def location_detail(data):
    # 아이콘 이미지 불러오기
    ICON_URL = "https://cdn-icons-png.flaticon.com/512/1141/1141117.png"
    icon_data = {
        # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
        # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
        "url": ICON_URL,
        "width": 242,
        "height": 242,
        "anchorY": 242,
    }
    data["icon_data"] = None
    for i in data.index:
        data["icon_data"][i] = icon_data
    la, lo = np.mean(data["위도"]), np.mean(data["경도"])

    layers = [
        pdk.Layer(
            type="IconLayer",
            data=data,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position="[경도, 위도]",
            pickable=True,
        )
    ]

    # Deck 클래스 인스턴스 생성
    deck = pdk.Deck(
        map_style=None, initial_view_state=pdk.ViewState(longitude=lo, latitude=la, zoom=11, pitch=50), layers=layers
    )

    st.pydeck_chart(deck, use_container_width=True)