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