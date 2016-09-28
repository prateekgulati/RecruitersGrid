import re
from bs4 import BeautifulSoup
import urllib
import nltk

def pchunk(t):
    w_tokens = nltk.word_tokenize(t)
    pt = nltk.tag.pos_tag(w_tokens)
    # return pt
    ne = nltk.ne_chunk(pt)
    return ne

def concordanceOutput(target_word, tar_passage, left_margin=10, right_margin=10):
    tokens = nltk.word_tokenize(tar_passage)
    text = nltk.Text(tokens)
    c = nltk.ConcordanceIndex(text.tokens, key=lambda s: s.lower())
    concordance_txt = (
    [text.tokens[map(lambda x: x -5 if (x - left_margin) > 0 else 0, [offset])[0]:offset + right_margin]
     for offset in c.offsets(target_word)])
    ## join the sentences for each of the target phrase and return it
    return [''.join([x + ' ' for x in con_sub]) for con_sub in concordance_txt]

def email(text):
    try:
        match=re.search(r'\S+@\S+\.\S+',text)
        ID= match.group(0)
        return ID
    except: pass

def handles(text):
    ID=dict()
    result = concordanceOutput('Twitter', text)  # text.concordance('Twitter') substitute
    for occurrence in result:
        try:
            match=re.search(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@ ([A-Za-z]+[A-Za-z0-9]+)',occurrence)
            ID['twitter']= match.group(0)
        except: pass
    result = concordanceOutput('Facebook', text)  # text.concordance('Facebook') substitute
    for occurrence in result:
        try:
            match=re.search(r'/^[a-z\d.]{5,}$/i',occurrence)
            ID['facebook']= match.group(0)
        except: pass
    result = concordanceOutput('Google Plus', text)  # text.concordance('Google Plus') substitute
    for occurrence in result:
        try:
            match=re.search(r'\+[^/]+|\d{21}',occurrence)
            ID['googlePlus']= match.group(0)
        except: pass
    result = concordanceOutput('linkedin', text)  # text.concordance('LinkedIN') substitute
    for occurrence in result:
        try:
            match=re.search(r'((http(s?)://)*([a-zA-Z0-9\-])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]',occurrence)
            ID['linkedIN']= match.group(0)
        except: pass
    return ID

def link(soup):
    links=[]
    for div in soup.findAll('div',attrs={'class':'user-links'}):
        for li in div.findAll('li'):
            for href in li.findAll('a'):
                links.append(href.get('href'))
    return links

def location(soup):
    for div in soup.findAll('div',attrs={'class':'user-links'}):
        txts=[]
        for li in div.findAll('li'):
            txts.append(li.getText().strip())
    for t in txts:
        chunk= pchunk(t)
        for tag in chunk.subtrees():
            if tag.label()=='GPE' or tag.label()=='NE':
                for name,pos in tag.leaves():
                    print name

if __name__ == '__main__':
    # html = urllib.urlopen("http://stackoverflow.com/users/548225/anubhava")
    # soup=BeautifulSoup(html)
    soup = BeautifulSoup(open("User anubhava - Stack Overflow.html"))
    raw = soup.get_text()
    twitterID=handles(raw)
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)
    emailID=email(text)
    links=link(soup)
    print twitterID
    print emailID
    print links
    location(soup)