from bs4 import BeautifulSoup
import urllib.parse

def convert_xml_to_txt(input: str, output: str):

    with open(input, 'r', encoding='utf-8') as f, \
         open(output, 'w', encoding='utf-8') as out:

        data = f.read()
        soup = BeautifulSoup(data, 'xml')

        prefix = "https://mazii.net/vi-VN/search/word/javi/"

        for item in soup.find_all('loc'):
            if item.text.startswith(prefix): 
                out.write(urllib.parse.unquote(item.text[len(prefix):]) + '\n')