import os
import urllib.request
import requests
import re
import img2pdf
import shutil
import zipfile
import sys
from bs4 import BeautifulSoup

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
manga_name=sys.argv[1]
manga_start=sys.argv[2]
manga_name=str(manga_name)
# manga_name="necromancer"
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

page = requests.get('http://www.mangapanda.com/'+manga_name)
soup = BeautifulSoup(page.content, 'html.parser')
for a in soup.find_all('a', href=True):
    if(a['href'].startswith('/'+manga_name)):
        chapters=a['href']
        break

chapter=chapters.split("/")[2]
for chapter_number in range(int(manga_start), int(chapter)+1):
    os.mkdir(str(chapter_number))
    page = requests.get('http://www.mangapanda.com/'+manga_name+'/' + str(chapter_number))
    soup = BeautifulSoup(page.content, 'html.parser')
    size=soup.find_all(text=re.compile('of'))[1].split()[1]
    for pages in range(1, int(size)+1):
        if(pages==1):
            page = requests.get('http://www.mangapanda.com/'+manga_name+'/' + str(chapter_number))
            soup = BeautifulSoup(page.content, 'html.parser')
            urllib.request.urlretrieve(soup.find_all('img')[0]['src'],'./'+str(chapter_number)+'/'+str(pages)+'.jpg')
        else :
            page = requests.get('http://www.mangapanda.com/'+manga_name+'/' + str(chapter_number)+'/'+str(pages))
            soup = BeautifulSoup(page.content, 'html.parser')
            urllib.request.urlretrieve(soup.find_all('img')[0]['src'],'./'+str(chapter_number)+'/'+str(pages)+'.jpg')
        #os.system('zip -vm cp0' + str(chapter_number) +'.pd *.jpg')
    
    with open(str(chapter_number)+".pdf", "wb") as f:
        os.chdir(str(chapter_number))
        f.write(img2pdf.convert([i for i in sorted_alphanumeric(os.listdir(os.getcwd())) if i.endswith(".jpg")]))
    os.chdir('..')

manga_zip = zipfile.ZipFile(os.getcwd()+'/'+manga_name+'.zip', 'w')
 
for folder, subfolders, files in os.walk(os.getcwd()):
 
    for file in files:
        if file.endswith('.pdf'):
            manga_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), os.getcwd()), compress_type = zipfile.ZIP_DEFLATED)
 
manga_zip.close()
for chapter_number in range(1, int(chapter)+1):
    shutil.rmtree(str(chapter_number))
    os.remove(str(chapter_number)+'.pdf')

 
