import requests

TIEBA_NAME = ''
TIEBA_FID = ''
BDUSS = ''

with open('./threads.txt', 'r', encoding='UTF-8') as f:
    thread_list = f.readlines()


def rewind(tid, pid=0):
    cookies = {
        'BDUSS': BDUSS,
    }

    headers = {
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'fn': TIEBA_NAME,
        'fid': TIEBA_FID,
        'tid_list[]': tid,
        'pid_list[]': pid,
        'type_list[]': 1 if pid else 0,
        'is_frs_mask_list[]': 0
    }

    response = requests.post('https://tieba.baidu.com/mo/q/bawurecoverthread',
                             headers=headers, data=data, cookies=cookies)
