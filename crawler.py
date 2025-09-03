import requests
from bs4 import BeautifulSoup

def crawler_word_data(word: str):
    url = f"https://mazii.net/vi-VN/search/word/javi/{word}"

    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = None

    for item in soup.select("div.box-main-word"):
        vocab = item.select_one("h3.main-word")
        phonetic = item.select_one("p.phonetic-word")
        han_viet = item.select_one("p.han-viet-word")
        pronunciation = item.select_one("div.txt-pronun")
        type_word = item.select_one("div.type-word")
        meanings = []

        for block in item.select("div.mean-detail-range > div.ng-star-inserted"):
            word_meaning = block.select_one("h4.mean-word")
            if not word_meaning: continue
            word_meaning = word_meaning.get_text(strip=True)

            examples = []
            for detail in block.select("div.item-example"):
                jp = [k.text.strip() for k in detail.select("div.txt-word ruby")]
                vi = detail.select_one("div.example-mean-word span")
                examples.append({
                    "jp": "".join(jp),
                    "vi": vi.text.strip() if vi else None
                })

            meanings.append({
                "meaning": word_meaning,
                "examples": examples
            })


        results = {
            "word": vocab.text.strip() if vocab else None,
            "phonetic": phonetic.text.strip() if phonetic else None,
            "han-viet": han_viet.text.strip() if han_viet else None,
            "pronunciation": pronunciation.text.strip() if pronunciation else None,
            "type": type_word.text.strip() if type_word else None,
            "meaning_detail": meanings
        }

    return results
