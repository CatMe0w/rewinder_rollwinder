import requests
import logging
import time

TIEBA_NAME = ''
TIEBA_FID = ''
TBS = ''
BDUSS = ''


def rollback(tid, pid, is_comment):
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
        'Referer': 'https://tieba.baidu.com/p/' + tid,
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'commit_fr': 'pb',
        'ie': 'utf-8',
        # 'tbs': 'ade683d96421bb181639555518',
        'tbs': TBS,
        'kw': TIEBA_NAME,
        'fid': TIEBA_FID,
        'tid': tid,
        'is_vipdel': '0',
        'reason': '6',
    }

    if pid != 0:
        data.update({'pid': pid})
        if is_comment == '1':
            data.update({'id_finf': '1'})
        else:
            data.update({'is_finf': 'false'})  # 百！！！！！！！度！！！！！！！！！！！

    while True:
        try:
            logging.info('Rollbacking thread {}, post {}'.format(tid, pid if pid else None))
            response = requests.post('https://tieba.baidu.com/f/commit/post/delete',
                                     headers=headers, data=data, cookies=cookies)
            if response.status_code != 200:
                raise ValueError
            logging.info('Response: {}'.format(response.text))
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
            logging.FileHandler('rollwinder.log'),
            logging.StreamHandler()
        ])

    with open('./rollback.txt', 'r', encoding='UTF-8') as f:
        thread_list = f.readlines()

    for thread in reversed(thread_list):
        tid, pid, is_comment = thread.strip().split(' ')
        rollback(tid, pid, is_comment)

    logging.info('All done! Have fun!')


if '__main__' == __name__:
    main()
