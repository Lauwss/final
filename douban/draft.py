"""
该模块用于从豆瓣电影 Top250 页面下载 HTML 内容，并保存到本地的 html 文件夹中。
"""
import os
import requests

# 创建 html 文件夹，如果文件夹已存在则不会报错
if not os.path.exists('html'):
    os.makedirs('html')

# 基础 URL
BASE_URL = "https://movie.douban.com/top250"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/131.0.0.0 Safari/537.36"
}
PROXIES = {
    "http": None,
    "https": None
}

# 遍历所有页面
for start in range(0, 250, 25):
    URL = f"{BASE_URL}?start={start}"
    try:
        # 添加 timeout 参数，避免程序无限期挂起
        response = requests.get(url=URL, headers=HEADERS, proxies=PROXIES, timeout=10)
        response.raise_for_status()  # 检查请求是否成功

        # 保存 HTML 文件到 html 文件夹中
        file_name = os.path.join('html', f"douban_top250_page_{start // 25 + 1}.html")
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"成功保存 {file_name}")
    except requests.RequestException as e:
        print(f"请求 {URL} 时出错: {e}")
