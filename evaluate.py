import os
import csv
from bs4 import BeautifulSoup

# 指向目录，而非具体文件
dest_dir = r"C:\Users\20342\Desktop\final"  # 或使用 "C:/Users/..."
output_file = os.path.join(dest_dir, "douban_movies.csv")  # 输出CSV文件路径
error_log = os.path.join(dest_dir, "parsing_errors.log")  # 错误日志路径

# 创建错误日志文件
with open(error_log, 'w', encoding='utf-8') as f:
    f.write("解析错误日志\n")

# 检查目录是否存在
if not os.path.isdir(dest_dir):
    raise FileNotFoundError(f"目录不存在: {dest_dir}")

# 准备CSV文件并写入表头
with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['标题', '评分', '评论数', '导演与演员', '链接', '图片链接']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# 遍历目录下的所有HTML文件
for html_file in os.listdir(dest_dir):
    if html_file.endswith('.html'):
        file_path = os.path.join(dest_dir, html_file)
        print(f"\n处理文件: {file_path}")
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
      
        # 抽取文件内容
        soup = BeautifulSoup(html, 'html.parser')
        movie_list = soup.find('ol', class_='grid_view')
        
        if not movie_list:
            print(f"警告: 文件 {html_file} 中未找到电影列表，跳过")
            with open(error_log, 'a', encoding='utf-8') as f:
                f.write(f"文件 {html_file}: 未找到电影列表\n")
            continue
            
        movie_items = movie_list.find_all('li')
        print(f"找到 {len(movie_items)} 个电影项")
        
        # 准备数据并追加到CSV
        success_count = 0
        for i, movie in enumerate(movie_items):
            try:
                # 提取标题
                title_span = movie.find('div', class_='hd').find('span', class_='title')
                title = title_span.get_text(strip=True) if title_span else "未找到标题"
                
                # 提取评分
                star_div = movie.find('div', class_='star')
                rating_span = star_div.find('span', class_='rating_num') if star_div else None
                rating_num = rating_span.get_text(strip=True) if rating_span else "未找到评分"
                
                # 提取评论数
                comment_span = star_div.find_all('span')[-1] if star_div and star_div.find_all('span') else None
                comment_num = comment_span.get_text(strip=True) if comment_span else "未找到评论数"
                
                # 提取导演和演员
                bd_div = movie.find('div', class_='bd')
                p_tag = bd_div.find('p') if bd_div else None
                directors = p_tag.get_text(strip=True) if p_tag else "未找到导演信息"
                
                # 提取链接和图片
                pic_div = movie.find('div', class_='pic')
                a_tag = pic_div.find('a') if pic_div else None
                link = a_tag.get('href', '未找到链接') if a_tag else '未找到链接'
                
                img_tag = a_tag.find('img') if a_tag else None
                pic = img_tag.get('src', '未找到图片') if img_tag else '未找到图片'
                
                # 保存数据
                movie_data = {
                    '标题': title,
                    '评分': rating_num,
                    '评论数': comment_num,
                    '导演与演员': directors,
                    '链接': link,
                    '图片链接': pic
                }
                
                # 写入CSV
                with open(output_file, 'a', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(movie_data)
                
                success_count += 1
                
            except Exception as e:
                error_msg = f"解析电影项 {i+1} 时出错: {str(e)}"
                print(f"警告: {error_msg}")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"文件 {html_file}, 电影项 {i+1}: {error_msg}\n")
                    f.write(f"HTML片段: {movie.prettify()[:500]}...\n\n")  # 记录出错的HTML片段
        
        print(f"成功保存 {success_count} 条电影数据到 {output_file}")
        print(f"解析错误: {len(movie_items) - success_count} 条")

print(f"\n全部处理完成！数据已保存到: {output_file}")
print(f"错误日志已保存到: {error_log}")    