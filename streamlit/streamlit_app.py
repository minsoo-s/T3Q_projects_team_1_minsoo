# �����ڵ�-------------------------------------------
# streamlit run streamlit_app.py
#----------------------------------------------------

import streamlit as st 
st.set_page_config(layout="wide")

# title ����
st.title(' �뱸������ �������� �ʿ��� ��ƮȦ ��ġ���� ')
# ������ ���� select box
option = st.sidebar.selectbox(
    '� ������ ���ðڽ��ϱ�?',
    ('�뱸 ��ü','�ϱ�', '�߱�', '����', '����',"����", "������", "�޼���", "�޼���"))

# if st.sidebar.selectbox('����'):


# [ ������ġ ��ǥ ���� �Լ� ] --------------------------------------------------------------
# �ǽð� ��ġ���� ����
import requests, json
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

def current_location():
    here_req = requests.get("http://www.geoplugin.net/json.gp")

    if (here_req.status_code != 200):
        print("������ǥ�� �ҷ��� �� ����")
    else:
        location = json.loads(here_req.text)
        crd = {float(location["geoplugin_latitude"]), float(location["geoplugin_longitude"])}
        crd = list(crd)
        gps = pd.DataFrame( [[crd[1],crd[0]]], columns=['����','�浵'])
    
    return gps
    
# �ǽð� ��ġ���� ����(�ÿ���) - ��ϴ��б�
def geocoding():
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode("�뱸 �ϱ� ��ϴ��б� �۷ι��ö���")
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
    gps = pd.DataFrame( [[crd['lat'],crd['lng']]], columns=['����','�浵'])
    return gps

# [ �ʿ� ��ġ ǥ�� �Լ�] ------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# ��ġ���� �� (��, data�� ����, �浵 �÷��� �־�� ��)
def location_detail(data_c):
    data = data_c.copy()

    # ������ �̹��� �ҷ�����
    ICON_URL = "https://cdn-icons-png.flaticon.com/512/2711/2711648.png"
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
    la, lo = np.mean(data["����"]), np.mean(data["�浵"])

    layers = [
        pdk.Layer(
            type="IconLayer",
            data=data,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position="[�浵, ����]",
            pickable=True,
        )
    ]
    
    if len(data_c) == 0:
        pass
    else:
        # Deck Ŭ���� �ν��Ͻ� ����
        deck = pdk.Deck(height=100,
                        #width=1000,
                        map_style='mapbox://styles/mapbox/streets-v11', 
                        initial_view_state=pdk.ViewState(longitude=lo, 
                                                        latitude=la, 
                                                        zoom=12, 
                                                        pitch=50), 
                        layers=layers,
                        tooltip={"text":"{�ּ�}\n{����}/{�浵}"})

        st.pydeck_chart(deck, use_container_width=True)

# r = pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state,
#     tooltip={"text": "{name}\n{address}"},
#     map_style=pdk.map_styles.ROAD,
# )

# [ gps �����ͼ� ���� �� ���� �Լ� ]--------------------------------------------------
def add_gps_all(gps):
    # gps_all(����) �ҷ�����
    gps_all = pd.read_csv('gps_all.csv')

    # gps_all(����), gps(�߰� ����) ������������ ���� 
    gps_all = pd.concat([gps_all,gps]).reset_index()
    gps_all = gps_all.drop('index',axis=1)

    # �ߺ� ��ġ���� ����
    gps_all = gps_all.drop_duplicates()

    # �߰� ��ġ���� ����� ������������ ����
    gps_all.to_csv('gps_all.csv',index = False)



# [����,�浵 -> �ּ� ��ȯ �Լ�]-----------------------------------------------------
from geopy.geocoders import Nominatim

def geocoding_reverse(lat_lng_str): 
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)

    return address

# [ ���� ���� �ּ� ������������ �Լ� ]----------------------------------------------------
def createDF(gps_all):
# ����,�浵 -> �ּ� ��ȯ
    address_list = []
    for i in range(len(gps_all)):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        lat = gps_all['����'][i]
        lng = gps_all['�浵'][i]
        address = geocoding_reverse(f'{lat}, {lng}')
        
        # ī�װ� ���� 
        if option =='�뱸 ��ü':
            address_list.append(address)
        elif option in address[0]:
            address_list.append(address)

    df = pd.DataFrame(address_list, columns=['�ּ�','��ġ����(����,�浵)'])
    
    df_map = pd.DataFrame(columns=['�ּ�','����','�浵'])
    for i in range(len(df)):
        df_map.loc[i] = [df.loc[i]['�ּ�'],df.loc[i][1][0],df.loc[i][1][1]]

    # ����,�浵 �ּҺ�ȯ ������������ �ð�ȭ
    st.dataframe(df_map)

    # �ش� ���� ��ġ���� ���� ǥ��
    st.write(option,'����, ������ �ʿ��� ����: ',len(df_map),'��')
    
    return df_map
#---------------------------------------------------------------

# [ ���� �Լ� ���� �ڵ� ]------------------------------------------------------------------------

# �ǽð� ��ġ���� ����
gps = geocoding()   # �ÿ���
#gps = current_location()   # �ǽð���ǥ

# ���� ��ġ���� �����Ϳ� �ǽð� ��ġ���� �߰� ����
add_gps_all(gps)

# ���� ������ ��ü ��ġ���� ���� �ҷ�����
gps_all = pd.read_csv('gps_all.csv')

# �ּ� ������������ ǥ��
df_map = createDF(gps_all) 

# ��ü ��ġ���� �� ������ ǥ��
location_detail(df_map)
