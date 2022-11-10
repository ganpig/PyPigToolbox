from common import *
import json
import random

app_name = 'Pixabay图片搜索'
api_url = 'https://pixabay.com/api/'
api_key = '17240666-2c0f76f1ba2df07176f573fe7'
hd_preview = True


def apiget(key, page):
    got = urlget(
        f'{api_url}?key={api_key}&q={urlencode(key)}&image_type=photo&lang=zh&page={page}&per_page=200', 3)
    if got:
        return json.loads(autodecode(got))
    else:
        return None


def parse(data):
    ret = []
    for i in data['hits']:
        ret.append(
            (i['webformatURL' if hd_preview else 'previewURL'], i['largeImageURL']))
    return ret


def search(key):
    log(f'正在搜索“{key}”')
    data = apiget(key, 1)
    if data:
        ret = parse(data)
    else:
        error('获取图片列表失败!')
        return None
    for i in range(2, min((int(data['total'])+399)//200, 4)):
        data = apiget(key, i)
        if data:
            ret += parse(data)
    log('获取图片列表成功!')
    return ret


def download_all(data, key, save_dir):
    cnt = 0
    for i in range(len(data)):
        log(f'正在批量下载({i+1}/{len(data)})')
        url = data[i][1]
        ty = url.split('.')[-1]
        got = urlget(url, 3)
        if got:
            fwrite(os.path.join(save_dir, f'{key}_{i+1}.{ty}'), got)
        else:
            cnt += 1
            error(f'第{i+1}张图片下载失败!')
    log(f'批量下载完成，{len(data)-cnt}张图片下载成功，{cnt}张图片下载失败!')
    msgbox('批量下载完成!', app_name)


def main():
    last_path = getdesktop()
    last_search = ''
    while True:
        inp = enterbox('请输入搜索关键词', app_name, last_search)
        if not inp:
            return
        last_search = inp
        data = search(inp)
        if not data:
            msgbox('未搜索到图片!', app_name)
            continue
        log(f'搜索到 {len(data)} 张图片')
        index = 0
        while True:
            index %= len(data)
            path = getimage(data[index][0])
            ch = buttonbox(
                '可点击图片保存。', f'{app_name} - 搜索结果({index+1}/{len(data)})', ('<<', '跳转', '随机', '批量', '>>'), path)
            if not ch:
                break
            elif ch == '<<':
                index -= 1
            elif ch == '跳转':
                ch = enterbox(f'想要查看第几张图片(共{len(data)}张)?', app_name)
                try:
                    if 0 < int(ch) <= len(data):
                        index = int(ch)-1
                    else:
                        msgbox('输入超出范围!', app_name)
                except:
                    msgbox('输入不是整数!', app_name)
            elif ch == '随机':
                index = random.randint(1, len(data))
            elif ch == '批量':
                savedir = diropenbox('请选择保存文件夹', app_name, last_path)
                if savedir:
                    last_path = savedir
                    newthread(download_all, data, inp, savedir)
            elif ch == '>>':
                index += 1
            elif ch == path:
                url = data[index][1]
                ty = url.split('.')[-1]
                path = filesavebox(
                    '保存图片', app_name, os.path.join(last_path, f'{inp}_{index+1}.{ty}'))
                if path:
                    last_path = '\\'.join(path.split('\\')[:-1])
                    log('正在下载图片')
                    got = urlget(url, 3)
                    if got:
                        fwrite(path, got)
                        log('下载成功!')
                    else:
                        error('下载失败!')
                        msgbox('下载失败!', app_name)


if __name__ == '__main__':
    main()
