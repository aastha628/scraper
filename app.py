from flask import Flask,render_template,request, session
import urllib.request
import re
import requests
from requests.models import Response
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs


app=Flask(__name__)

app.secret_key = 'SECRET KEY'

def find_vdo(word):
    keyword=word
    keyword=keyword.replace(" ","+")
    url="https://www.youtube.com/results?search_query="+keyword
    html = urllib.request.urlopen(url)
    vdo_id=re.findall(r"watch\?v=(\S{11})",(html.read().decode()))
    return vdo_id




def get_vdo_meta_data(url):
    vdo_meta={}
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    titleSoupMeta = soup.find("meta", property="og:title")
    vdo_meta['title']=titleSoupMeta["content"]
    thumbSoupMeta2 = soup.find("meta", property="og:image")
    vdo_meta['image'] = thumbSoupMeta2["content"] 
    vdo_meta["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
    return vdo_meta

def get_details(vdo_id):
    details=[]
    for i in range(0,10):
        url_use="https://www.youtube.com/watch?v="+vdo_id[i]
        details.append(get_vdo_meta_data(url_use))
    return details

@app.route('/',methods =["GET", "POST"])
def home():
    return render_template('SEOwave.html')

    
@app.route('/tagsinfo',methods =["GET", "POST"])
def main():
    word=request.form.get("search-input")
    id=find_vdo(word)
    data=get_details(id)
    # print (data)
    return render_template('SEOwave2.html',data=data,search=word)

@app.route('/about')
def about():
    return render_template('About.html')

if __name__=="__main__":
    app.run(debug=True)