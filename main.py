from common import *
import traceback

app_name = 'PyPigToolbox'
tools_module = ['netease', 'pixabay', 'word']

if __name__ == '__main__':
    os.system(f'title {app_name}')
    log('工具箱启动', 'cyan', mode=1)
    toollist = {}
    for i in tools_module:
        try:
            tool = __import__(i)
            toollist[tool.app_name] = tool.main
            log(f'成功加载模块{i}')
        except:
            error(f'加载模块{i}失败!')

    while True:
        ch = choicebox(f'欢迎使用{app_name}!', app_name, toollist)
        if not ch:
            log('工具箱关闭', 'cyan', mode=1)
            exit()
        log(f'“{ch}”启动', 'green')
        try:
            toollist[ch]()
        except:
            error(f'“{ch}”出现错误!错误信息如下:')
            print(traceback.format_exc())
        finally:
            log(f'“{ch}”关闭', 'green')
