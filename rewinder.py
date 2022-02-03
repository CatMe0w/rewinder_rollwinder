import requests
import logging
import time
import json

TIEBA_NAME = ''
TIEBA_FID = ''
BDUSS = ''


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

    while True:
        try:
            logging.info('Rewinding thread {}, post {}'.format(tid, pid if pid else None))
            response = requests.post('https://tieba.baidu.com/mo/q/bawurecoverthread',
                                     headers=headers, data=data, cookies=cookies)
            if response.status_code != 200:
                raise ValueError
            content = json.loads(response.content)
            if int(content['no']):
                logging.critical('Rewind failed. Response: {}'.format(content))
        except requests.exceptions.Timeout:
            print('Remote is not responding, sleep for 30s.')
            time.sleep(30)
            continue
        except ValueError:
            print('Rate limit exceeded, sleep for 30s.')
            time.sleep(30)
            continue
        else:
            break


def main():
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("rewinder.log"),
            logging.StreamHandler()
        ])

    with open('./threads.txt', 'r', encoding='UTF-8') as f:
        thread_list = f.readlines()

    for thread in thread_list:
        tid, pid, _ = thread.strip().split(' ')
        rewind(tid, pid)

    logging.info('All done! Have fun!')


if '__main__' == __name__:
    main()
