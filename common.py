from easygui import *
import _thread
import chardet
import faker
import io
import os
import PIL
import time
import urllib.parse
import urllib.request


def autodecode(data):
    return data.decode(chardet.detect(data)['encoding'])


def error(message):
    log(message, 'red', mode=1)


def fread(path):
    with open(path, 'rb') as f:
        data = f.read()
    return data


def fwrite(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def getdesktop():
    return os.path.expanduser('~\\desktop')


def getimage(url):
    path = gettemp(url.split('/')[-1])
    if not os.path.isfile(path):
        got = urlget(url, 3)
        if got:
            fwrite(path, got)
    return path


def gettemp(name):
    path = os.path.join(os.environ["TEMP"], 'PyPigToolbox')
    if not os.path.isdir(path):
        msg('缓存目录不存在，于是工具箱创建了一个')
        os.mkdir(path)
    return os.path.join(path, urlencode(name))


def imagescale(path, size):
    j = path.split('.')
    k = '.'.join(j[:-1])
    to = f'{k}{size}.{j[-1]}'
    PIL.Image.open(path).resize(size).save(to)
    return to


def log(message, text=None, back=None, mode=0):
    color_list = ['black', 'red', 'green',
                  'yellow', 'blue', 'purple', 'cyan', 'black']
    color = str(mode)
    if text:
        color = f'{color};3{color_list.index(text)}'
    if back:
        color = f'{color};4{color_list.index(back)}'
    message = f'\033[{color}m{message}\033[0m'
    print(time.strftime('[%H:%M:%S]', time.localtime()), message)


def msg(message):
    log(message, 'blue', mode=3)


def newthread(func, *args, **kwargs):
    msg('启动了一个新线程')
    _thread.start_new_thread(func, args, kwargs)


def sprint(*args, **kwargs):
    output = io.StringIO()
    print(*args, **kwargs, file=output)
    contents = output.getvalue()
    output.close()
    return contents


def urlencode(name):
    return urllib.parse.quote(name)


def urlget(url, retry=1):
    try:
        msg(f'正在访问 URL {url}')
        req = urllib.request.Request(url, headers={'User-Agent': faker.Factory.create().user_agent()})
        return urllib.request.urlopen(req).read()
    except:
        if retry > 1:
            msg(f'网络访问出错，没关系，还有{retry-1}次尝试机会')
            return urlget(url, retry-1)
        else:
            error(f'网络访问失败!')
            return None
