from common import *
import json
import shutil

app_name = '网易云音乐搜索'
api0_url = 'https://v2.alapi.cn/api/music/detail'
api1_url = 'https://v2.alapi.cn/api/music/search'
api2_url = 'http://music.163.com/api/song/media'
api3_url = 'https://v2.alapi.cn/api/music/url'
api_key = '8V399wDUkyMaQc94'
last_path = getdesktop()
api0mem = {}


def api0get(key):
    global api0mem
    if key in api0mem:
        return api0mem[key]
    got = urlget(f'{api0_url}?token={api_key}&id={key}', 3)
    if got:
        data = json.loads(autodecode(got))
        if data:
            if 'data' in data:
                ret = data['data']['songs'][0]['al']['picUrl']
                api0mem[key] = ret
                return ret
    return None


def api1get(key):
    got = urlget(
        f'{api1_url}?token={api_key}&keyword={urlencode(key)}&limit=30', 3)
    if got:
        return json.loads(autodecode(got))
    return None


def api2get(key):
    got = urlget(f'{api2_url}?id={key}', 3)
    if got:
        data = json.loads(autodecode(got))
        if 'lyric' in data:
            return data['lyric']
    return None


def api3get(key):
    got = urlget(f'{api3_url}?token={api_key}&id={key}&format=json', 3)
    if got:
        data = json.loads(autodecode(got))
        if 'data' in data and data['data']:
            return urlget(data['data']['url'], 3)
    return None


def parse(data):
    ret = {}
    if 'data' in data:
        for i in data['data']['songs']:
            artists = '、'.join([j['name'] for j in i['artists']])
            ret[artists+' - '+i['name']] = i['id']
    return ret


def search(key):
    log(f'正在搜索“{key}”')
    data = api1get(key)
    if data:
        log('获取音乐列表成功!')
        return parse(data)
    else:
        error('获取音乐列表失败!')
        return None


def view(name, id):
    global last_path
    while True:
        inp = buttonbox(
            '可点击图片保存。', f'{app_name} - {name}', ('在线播放', '查看歌词', '下载歌词', '下载音频'), imagescale(getimage(api0get(id)), (100, 100)))
        if not inp:
            return
        elif inp == '在线播放':
            os.system(
                f'start https://music.163.com/#/song?id={id}')
        elif inp == '查看歌词':
            log(f'正在获取 {name} 的歌词')
            got = api2get(id)
            if got:
                log('获取成功!')
                textbox('歌词如下。', f'{app_name} - {name}', got)
            else:
                error('歌词获取失败!')
                msgbox('歌词获取失败!', app_name)
        elif inp == '下载歌词':
            path = filesavebox(
                f'保存歌词', app_name, os.path.join(last_path, f'{name}.lrc'))
            if path:
                last_path = '\\'.join(path.split('\\')[:-1])
                log(f'正在下载 {name} 的歌词')
                got = api2get(id)
                if got:
                    fwrite(path, got.encode('utf-8'))
                    log('下载成功!')
                else:
                    error('下载失败!')
                    msgbox('下载失败!', app_name)
        elif inp == '下载音频':
            path = filesavebox(
                f'保存音频', app_name, os.path.join(last_path, f'{name}.mp3'))
            if path:
                last_path = '\\'.join(path.split('\\')[:-1])
                log(f'正在下载 {name} 的音频')
                got = api3get(id)
                if got:
                    fwrite(path, got)
                    log('下载成功!')
                else:
                    error('下载失败!')
                    msgbox('下载失败!', app_name)
        elif inp == getimage(api0get(id)):
            path = filesavebox(
                f'保存图片', app_name, os.path.join(last_path, f'{name}.jpg'))
            if path:
                last_path = '\\'.join(path.split('\\')[:-1])
                log(f'正在复制图片到 {path}')
                shutil.copy(getimage(api0get(id)), path)
                log('保存成功!')


def main():
    last_search = '蔗蓝'
    while True:
        ch = enterbox('请输入搜索内容', app_name, last_search)
        if not ch:
            return
        last_search = ch
        data = search(ch)
        if not data:
            msgbox('未搜索到音乐!', app_name)
            continue
        elif len(data) == 1:
            log('搜索到 1 首音乐')
            view(*next(iter(data.items())))
        else:
            log(f'搜索到 {len(data)} 首音乐')
            while True:
                ch = choicebox('搜索结果如下。', app_name, data)
                if not ch:
                    break
                view(ch, data[ch])


if __name__ == '__main__':
    main()
