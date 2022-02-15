import requests
import logging
import hashlib
import json
import time

TIEBA_NAME = ''
TIEBA_FID = ''
TBS = ''
BDUSS = ''


def add_sign(data):
    _ = ''
    for (k, v) in sorted(data.items()):
        _ += (k + '=' + v)
    _ += 'tiebaclient!!!'

    sign = hashlib.md5(_.encode('utf-8')).hexdigest().upper()
    data.update({'sign': str(sign)})
    return data


def delete_thread(tid):
    data = {
        'BDUSS': BDUSS,
        'fid': TIEBA_FID,
        'is_frs_mask': 0,
        'tbs': TBS,
        'z': tid
    }
    signed_data = add_sign(data)
    while True:
        try:
            logging.info('Rollbacking thread {}'.format(tid))
            response = requests.post('http://c.tieba.baidu.com/c/c/bawu/delthread', data=signed_data)
            if response.status_code != 200:
                raise ValueError
            content = json.loads(response.content)
            if int(content['error_code']):
                logging.error('Rollback failed.')
            logging.info('Response: {}'.format(content))
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


def delete_post(tid, pid):
    data = {
        'BDUSS': BDUSS,
        'fid': TIEBA_FID,
        'pid': pid,
        'tbs': TBS,
        'z': tid
    }
    signed_data = add_sign(data)
    while True:
        try:
            logging.info('Rollbacking thread {}, post {}'.format(tid, pid))
            response = requests.post('http://c.tieba.baidu.com/c/c/bawu/delpost', data=signed_data)
            if response.status_code != 200:
                raise ValueError
            content = json.loads(response.content)
            if int(content['error_code']):
                logging.error('Rollback failed.')
            logging.info('Response: {}'.format(content))
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


def rollback(tid, pid):
    if pid == 0:
        delete_thread(tid)
    else:
        delete_post(tid, pid)


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
        tid, pid, _ = thread.strip().split(' ')
        rollback(int(tid), int(pid))

    logging.info('All done! Have fun!')


if '__main__' == __name__:
    main()
