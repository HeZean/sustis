import json
import re
import requests
import streamlit as st

session = requests.Session()



cas_url = 'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas'
table_url = 'https://tis.sustech.edu.cn/xszykb/queryxszykbzong'
meta_url = 'https://tis.sustech.edu.cn/component/queryRlZcSj'

max_week = 0

session = requests.Session()
tis = session.get(cas_url)
headers = {
    'username': '',
    'password': '',
    'execution': re.findall('on" value="(.+?)"', tis.text)[0],
    '_eventId': 'submit',
    'geolocation': ''
}

with open('user.json') as f:
    info = json.load(f)
    headers.update({'username': info.get('sid'),
                    'password': info.get('pwd')})


def login():
    tis = session.post(cas_url, headers)
    if str(tis.content, 'utf-8').startswith('<!DOCTYPE html><html>'):
        raise Exception('Username or password incorrect')

# https://cas.sustech.edu.cn/cas/login?service=http%3A%2F%2Flocalhost:8501%2Fcas

def check_login():
    # login()
    tis=session.post('https://tis.sustech.edu.cn/UserManager/queryxsxx')
    st.write(tis.text)





st.markdown('## SUSTech 课表-ics 在线生成器')

st.button('获取 CAS 课表', on_click=check_login)


    