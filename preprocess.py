#! /usr/bin/python3
import xml.etree.ElementTree as ET

import mwparserfromhell

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english", ignore_stopwords=True)


tree = ET.parse('dump.xml')
root = tree.getroot()

ns = '{http://www.mediawiki.org/xml/export-0.10/}'

sectionsToRemove = ['References', 'Further Reading', 'See also', 'External Links']


for article in root.findall(f'./{ns}page'):
    title = article.find(f'{ns}title').text # Type: str
    raw_body = article.find(f'{ns}revision/{ns}text').text

    wikicode = mwparserfromhell.parse(raw_body)
    
    sections = wikicode.get_sections()
    for section in sections:
        try:
            sectionTitle = section.filter_headings()[0].title
            if sectionTitle in sectionsToRemove:
                sections.remove(section)
        except IndexError:
            continue

    # remove slashes from titles
    title = title.replace('/','_')

    stripped = wikicode.strip_code()
    with open(f'text/{title}.txt','w') as myFile:
        myFile.write(stripped)

    stemmed = ' '.join([stemmer.stem(word) for word in stripped.split(' ')])
    with open(f'text/{title}-stemmed.txt','w') as myFile:
        myFile.write(stemmed)