# 실행코드-------------------------------------------
# streamlit run streamlit_app.py
#----------------------------------------------------

import streamlit as st 

# title 쓰기
st.title(' 맵 ')
# 그냥 text 쓰기 
#st.write('아무거나 쓰세요')
# markdown tag 쓰고 싶으면
#st.markdown('<h1>태그를 쓸 수 있어요</h1>')
# user input 받기 
#st.text_input('사용자 입력을 받아보세요: ')

# 이외에도 다양한 기능 엄청 많다~ 
#st.button 
#st.sidebar 

# 현재위치 좌표 얻기 --------------------------------------------------------------
import requests, json
import pandas as pd
import numpy as np

def current_location():
    here_req = requests.get("http://www.geoplugin.net/json.gp")

    if (here_req.status_code != 200):
        print("현재좌표를 불러올 수 없음")
    else:
        location = json.loads(here_req.text)
        crd = {float(location["geoplugin_latitude"]), float(location["geoplugin_longitude"])}
        crd = list(crd)
        gps = pd.DataFrame( [[crd[1],crd[0]]], columns=['위도','경도'])
    
    return gps

# 맵에 위치 표시 ------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# 위치정보 상세 (단, data에 위도, 경도 컬럼이 있어야 함)

def location_detail(data_c):
    data = data_c.copy()

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

# 실시간 위치 지도 표시 함수 실행 ------------------------------------------------------------------------
gps = current_location()
location_detail(gps)



############################################################################################################
# cctv -----------------------------------------------------------------------------------------------------
import requests
import numpy as np

def get_cctv_url(lat, lng):
    # CCTV 탐색 범위 지정을 위해 임의로 ±1 만큼 가감
    minX = str(lng-1)
    maxX = str(lng+1)
    minY = str(lat-1)
    maxY = str(lat+1)

    # 개인key 입력
    api_call = 'https://openapi.its.go.kr:9443/cctvInfo?' \
                'apiKey=개인key' \
                '&type=ex&cctvType=2' \
                '&minX=' + minX + \
                '&maxX=' + maxX + \
                '&minY=' + minY + \
                '&maxY=' + maxY + \
                '&getType=json'

    w_dataset = requests.get(api_call).json()
    cctv_data = w_dataset['response']['data']

    coordx_list = []
    for index, data in enumerate(cctv_data):
        xy_couple = (float(cctv_data[index]['coordy']),float(cctv_data[index]['coordx']))
        coordx_list.append(xy_couple)

    # 입력한 위경도 좌표에서 가장 가까운 위치에 있는 CCTV를 찾는 과정
    coordx_list = np.array(coordx_list)
    leftbottom = np.array((lat, lng))
    distances = np.linalg.norm(coordx_list - leftbottom, axis=1)
    min_index = np.argmin(distances)

    return cctv_data[min_index]


cctv_data = get_cctv_url(gps['위도'], gps['경도'])
print('CCTV명:', cctv_data['cctvname']) # 가장 가까운 CCTV명
print('CCTV 영상 URL:', cctv_data['cctvurl']) # 가장 가까운 CCTV 영상 URL