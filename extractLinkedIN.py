import urllib

import nltk
from bs4 import BeautifulSoup
import re


def experience(soup):
    time = ['Present']
    position = []
    company = []
    combTime = []
    experience = soup.find(id='background-experience')
    for heading in experience.findAll(['time', 'header']):
        for lines in heading.get_text().splitlines():
            if re.search(r'[0-9]{4}', lines):
                time.append(lines)
            else:
                for title in heading.findAll('h4'):
                    position.append(title.get_text())
                for title in heading.findAll('h5'):
                    content = title.get_text()
                    if content != '':
                        company.append(content)
    for i in range(0, len(time), 2):
        combTime.append(time[i] + "-" + time[i + 1])
    company = dict(zip(combTime, company))
    position = dict(zip(combTime, position))
    return (company, position)


def education(soup):
    education = soup.find(id='background-education')
    print education
    # for heading in experience.findAll(['header']):
    #     print heading


def extractLabel(text, label):
    label = []
    for sent in nltk.sent_tokenize(text):
        # print sent
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            # print chunk
            if hasattr(chunk, 'label'):
                # print chunk.label()
                if chunk.label() == 'ORGANIZATION':
                    # print [c[0] for c in chunk.leaves()]
                    label.append(''.join(c[0] for c in chunk.leaves()))
    return label


def organisationNLP(soup):
    org=[]
    experience = soup.find(id='background-experience')
    for lines in experience.get_text().splitlines():
        if re.search(r"[0-9]{4}", lines):
             org.append(extractLabel(lines, 'ORGANIZATION'))
    return org


if __name__ == '__main__':
    # html = urllib.urlopen("http://stackoverflow.com/users/548225/anubhava")
    # soup=BeautifulSoup(html)
    soup = BeautifulSoup(open("Anubhava Srivastava _ LinkedIn.html"))
    company, position = experience(soup)
    print company
    print position
    print organisationNLP(soup)
