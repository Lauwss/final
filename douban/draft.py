import requests
import os

# 创建 html 文件夹，如果文件夹已存在则不会报错
if not os.path.exists('html'):
    os.makedirs('html')

# 基础 URL
base_url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
proxies = {
    "http": None,
    "https": None
}

# 遍历所有页面
for start in range(0, 250, 25):
    url = f"{base_url}?start={start}"
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功

        # 保存 HTML 文件到 html 文件夹中
        file_name = os.path.join('html', f"douban_top250_page_{start//25 + 1}.html")
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"成功保存 {file_name}")
    except requests.RequestException as e:
        print(f"请求 {url} 时出错: {e}")