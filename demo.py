import os
from urllib.request import urlretrieve
from tkinter import *
from selenium import webdriver  # 找不到和Chrome对应版本的webdriver了，只能使用最新的一个版本

# 第二部分（python函数的逻辑是从底向上）
# https://music.163.com/#/search/m/?s=%E7%BB%BF%E8%89%B2&type=1
# 网页提供的外链接口 http://music.163.com/song/media/outer/url?id={}.mp3  但貌似不能下载vip了
# 针对动态网页  不能使用简单的request请求爬取


def song_load(item):
    song_id = item['song_id']
    song_name = item['song_name']
    song_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
    # 创建文件夹
    os.makedirs('music', exist_ok=True)
    path = 'music\{}.mp3'.format(song_name)
    # 文本框
    text.insert(END, '歌曲：{}，正在下载...'.format(song_name))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()
    # 下载
    urlretrieve(song_url, path)
    # 文本框
    text.insert(END, '歌曲：{}，下载完毕，请试听...'.format(song_name))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()


# 获取歌曲id
def get_music_name():

    name = entry.get()
    url = 'https://music.163.com/#/search/m/?s={}&type=1'.format(name)

    # 隐藏浏览器
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(options=option)
    driver.get(url=url)
    driver.switch_to.frame('g_iframe')

    req = driver.find_element_by_id('m-search')
    # 获取歌曲id
    a_id = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//a').get_attribute('href')  # xpath语法，用于解析网页
    # print(a_id)
    song_id = a_id.split('=')[-1]
    print(song_id)
    # 获取歌曲名称
    song_name = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//b').get_attribute('title')
    print(song_name)

    item = {}
    item['song_id'] = song_id
    item['song_name'] = song_name

    driver.quit()
    song_load(item)


# 第一部分
# 创建界面
root = Tk()
# 添加标题
root.title("test")
# 设置窗口的大小
root.geometry('560x450')  # 不是乘号×而是小写字母x
# 标签操作
label = Label(root, text='请输入下载歌曲：', font=('华文行楷', 20))
# 标签定位
label.grid()  # 默认row=0 col=0
# 输入框
entry = Entry(root, font=('隶书', 20))
entry.grid(row=0, column=1)
# 列表框
text = Listbox(root,font=('楷书', 16), width=50, heigh=15)
text.grid(row=1, columnspan=2)  # 横跨两列
# 开始下载按钮
button = Button(root,text='下载歌曲', font=('隶书',15), command=get_music_name)  # 不要加括号
button.grid(row=2, column=0, sticky=W)  #对齐方式（W代表West）
# 退出
button1 = Button(root,text='退出', font=('隶书',15), command=root.quit)
button1.grid(row=2, column=1, sticky=E)  #对齐方式（W代表West）
# 显示界面
root.mainloop()

# pyinstaller -F -w（去除命令行窗口） -i 图片路径 py文件
# pyinstaller -F -w -i icon.ico demo.py