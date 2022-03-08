from bs4 import BeautifulSoup as bs
import os
import re
import requests as rq
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('pos_arg', type=str)

args = parser.parse_args()

def save_image(blog, url_name, mycount, total):
    rf = rq.get(url_name)
    with open(f"down/{blog}/{url_name.split('/')[-1]}", 'wb') as f:
        f.write(rf.content)
        print(f'({mycount}/{total}) {url_name}')

blog = f'{args.pos_arg}'
offset = mycount = 0

r = rq.get(f'https://{blog}.tumblr.com/api/read?type=photo&num=0')
html = bs(r.content, 'html.parser')
total = html.select('posts')[0]['total']

print(total)
all_images = []

while True:
    r = rq.get(f'https://{blog}.tumblr.com/api/read?type=photo&num=50&start={offset}')
    html = bs(r.content, 'html.parser')
    posts = html.select('post')
    if len(posts):
        for post in posts:
            url_names = post.select('photo-url[max-width="1280"]')
            if len(url_names):
                pass
                for url_name in url_names:
                    if not url_name.text.split('.')[-1] == 'gif':
                        all_images.append(url_name.text)
            else:
                post_rb = post.select('regular-body')
                if len(post_rb):
                    img_list = re.findall('src="([^"]+)"', str(post_rb[0]))
                    if len(img_list):
                        for url_name in img_list:
                            if not url_name.split('.')[-1] == 'gif':
                                all_images.append(url_name)
        offset += 50
        print(f'Parse next 50 posts with offset {offset}/{total}')
    else:
        break

total = len(all_images)

if not os.path.exists('down'):
    os.mkdir('down')

if not os.path.exists(f'down/{blog}'):
    os.mkdir(f'down/{blog}')

for img_num, img_addr in enumerate(all_images):
    save_image(blog, img_addr, img_num, total)
