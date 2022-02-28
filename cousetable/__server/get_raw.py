import json
import re
import requests
import pandas as pd


class asyncrange:
    class __asyncrange:
        def __init__(self, *args):
            self.__iter_range = iter(range(*args))

        async def __anext__(self):
            try:
                return next(self.__iter_range)
            except StopIteration as e:
                raise StopAsyncIteration(str(e))

    def __init__(self, *args):
        self.__args = args

    def __aiter__(self):
        return self.__asyncrange(*self.__args)


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


def get_table():
    table = session.post(table_url, {
        'xn': info.get('year'),
        'xq': info.get('semester'),
    })

    tab = pd.read_json(table.text)
    clean_table = pd.DataFrame()

    clean_table['name_cn'] = [r.split('\n')[0].strip() for r in tab['SKSJ']]
    clean_table['name_en'] = [r.split('\n')[2]
                              .split('-')[0]
                              .replace('[', '')
                              .strip()
                              for r in tab['SKSJ_EN']]

    clean_table['weekday'] = [r[2] for r in tab['KEY']]
    clean_table['class_of_day'] = [r[6] for r in tab['KEY']]

    def judge_wk(s):
        global max_week
        temp = int(s.split('[')[-3]
                   .split('-')[-1]
                   .replace('周]', '')
                   .replace('单', '')
                   .replace('双', ''))
        if temp > max_week:
            max_week = temp
        return 1 if '单周' in s \
            else (2 if '双周' in s else 0)

    clean_table['norm_odd_even'] = [judge_wk(r) for r in tab['SKSJ']]

    clean_table['location'] = [r.split('[')[-2]
                               .replace(']', '')
                               .strip()
                               for r in tab['SKSJ']]
    with open('proc/'+str()+'.csv', 'w+', encoding='utf-8') as f:
        clean_table.to_csv(f, index=False)


async def get_meta():
    mondays = {}

    async for i in asyncrange(1, max_week + 1):
        try:
            meta_head = session.post(meta_url, {
                'xn': info.get('year'),
                'xq': info.get('semester'),
                'djz': i,
            }).json()
            mondays[i] = meta_head.get('content')[0].get('rq')
        except Exception as e:
            break

    with open('proc/meta.csv', 'w+', encoding='utf-8') as f:
        pd.DataFrame.from_dict(mondays, orient='index').to_csv(
            f, index_label=('week', 'mon_date'))


async def get_raw():
    login()
    get_table()
    await get_meta()
    session.close()
