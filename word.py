from common import *
import json


app_name = '金山词霸英语查词'
api_url = 'https://dict-mobile.iciba.com/interface/'


def apiget(key):
    got = urlget(f'{api_url}?c=word&m=getsuggest&word={urlencode(key)}', 3)
    if got:
        return json.loads(autodecode(got))
    else:
        return None


def parse(data):
    ret = {}
    for i in data['message']:
        ret[i['key']] = i['paraphrase'].replace(';', '\n')
    return ret


def search(key):
    log(f'正在搜索“{key}”')
    data = apiget(key)
    if data:
        log('获取单词列表成功!')
        return parse(data)
    else:
        error('获取单词列表失败!')
        return None


def main():
    last_search = ''
    while True:
        ch = enterbox('请输入英语单词/短语', app_name, last_search)
        if not ch:
            return
        last_search = ch
        data = search(ch)
        if not data:
            msgbox('未查询到单词!', app_name)
            continue
        elif len(data) == 1:
            log('搜索到 1 个单词')
            textbox(f'{next(iter(data.keys()))}的解释如下。',
                    app_name, next(iter(data.values())))
        else:
            log(f'搜索到 {len(data)} 个单词')
            while True:
                ch = choicebox('想要查看哪个单词/短语?', app_name, data)
                if not ch:
                    break
                textbox(f'{ch}的解释如下。', app_name, data[ch])


if __name__ == '__main__':
    main()
