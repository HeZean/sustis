import json
import re
import time
import requests
import datetime

cas_url = 'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas'
ele_url = 'https://tis.sustech.edu.cn/Xsxk/addGouwuche'

session = requests.Session()
try:
    tis = session.get(cas_url)
except:
    print('Internet connection error, exiting')
    exit(1)

headers = {
    'username': '',
    'password': '',
    'execution': re.findall('on" value="(.+?)"', tis.text)[0],
    '_eventId': 'submit',
    'geolocation': ''
}

ele_head = {
    "p_pylx": "1",
    "mxpylx": "1",
    "p_sfgldjr": "0",
    "p_sfredis": "0",
    "p_sfsyxkgwc": "0",
    "p_xktjz": "rwtjzyx"
}


def login():
    failToLogin = True
    retryTime = 10
    while failToLogin and retryTime >= 0:
        try:
            tis = session.post(cas_url, headers)
            failToLogin = False
        except:
            failToLogin = True
            retryTime -= 1
            print('Failed to login, retrying...')
    if failToLogin:
        print('Failed to login, CAS server is being fucked, exiting')

    if str(tis.content, 'utf-8').startswith('<!DOCTYPE html><html>'):
        raise Exception('Username or password incorrect')

    print('Successfully logged in\n')


def qk(courses,
       # stage 1: 0.1 tps
       since=str(datetime.date.today()) + ' 12:57:00',
       # stage 2: 5 tps
       pat=str(datetime.date.today()) + ' 12:59:00',
       # stage 3: 20 tps
       until=str(datetime.date.today()) + ' 13:05:00'):
    trial_cnt = 0
    start_batch = datetime.datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
    pat_batch = datetime.datetime.strptime(pat, '%Y-%m-%d %H:%M:%S')
    end_batch = datetime.datetime.strptime(until, '%Y-%m-%d %H:%M:%S')

    try:
        while True:
            trial_cnt += 1
            for course in courses:
                ele_head.update(course)
                tis = session.post(ele_url, ele_head)
                print(trial_cnt, tis.json()['message'], sep='\t')
                time.sleep(0.05)

            if datetime.datetime.now() < start_batch:
                print(datetime.datetime.now())
                time.sleep(10)
            elif datetime.datetime.now() < pat_batch:
                print(datetime.datetime.now())
                time.sleep(0.2)
            elif datetime.datetime.now() > end_batch:
                break

            print()

    except KeyboardInterrupt:
        return
    except:
        print(tis.content)


if __name__ == '__main__':
    try:
        with open('user.json') as f:
            info = json.load(f)
            headers.update({'username': info.get('sid'),
                            'password': info.get('pwd')})
            ele_head.update(info.get('ele_head'))
            courses = info.get('courses')

        login()
        qk(courses)

        print('\nAll done, have fun!')
        session.close()

    except Exception as e:
        print(e)
