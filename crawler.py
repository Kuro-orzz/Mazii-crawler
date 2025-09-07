import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util.retry import Retry

def create_session(retries, backoff_factor):
    session = requests.Session()
    retry = Retry(
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504] # Retry with these status code
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter=adapter)
    session.mount('https://', adapter=adapter)
    return session


def crawler_word_data(url: str, session: Session):

    r = session.get(url, timeout=10)
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

    return None


def crawl_kanji_data(url: str, session: Session):

    r = session.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = None

    for item in soup.select("div.kanji-main-infor"):
        kanji = item.select_one("p.txt-kanji")
        Kunyomi = [k.text.strip() for k in item.select("span.txt-kun")]
        Onyomi = [k.text.strip() for k in item.select("span.txt-on")]
        lines = None
        jlpt = None
        meaning = None
        explain = []

        for block in item.select("div.line-item"):
            title = block.select_one("h4")
            if not title:
                continue
            title_text = title.get_text(strip=True)
            info = block.select_one("div.item-infor")
            if not info:
                continue

            if "Số nét" in title_text:
                lines = info.text.strip()
            elif "JLPT" in title_text:
                jlpt = info.text.strip()
            elif "Nghĩa" in title_text:
                meaning = info.text.strip()
        
        for ul in item.select("div.line-item ul.item-infor.show-less"):
            for li in ul.select("li"):
                explain.append(li.get_text(strip=True))

        results = {
            "word": kanji.text.strip() if kanji else None,
            "Kunyomi": Kunyomi if Kunyomi else None,
            "Onyomi": Onyomi if Onyomi else None,
            "Strokes": lines,
            "JLPT": jlpt,
            "Meaning": meaning,
            "Explain": explain
        }
        
        return results

    return None