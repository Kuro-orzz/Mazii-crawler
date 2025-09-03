from convert_xml import convert_xml_to_txt
from general import get_continue_id, save_current_id, log_crawler_error
from crawler import crawler_word_data
import time, random, json, sys
from multiprocessing import Process

def main(args = None):
    if args is None:
        args = sys.argv[1:]

    XML_FILE = args[0]
    VOCAB_FILE = args[1]
    OUTPUT_FILE = args[2]
    SAVE_FILE = args[3]
    ERROR_FILE = args[4]
    convert_xml_to_txt(XML_FILE, VOCAB_FILE)

    with open(VOCAB_FILE, 'r', encoding='utf-8') as f, \
         open(OUTPUT_FILE, 'a', encoding='utf-8') as output:

        lines = f.readlines()
        id = get_continue_id(SAVE_FILE)

        for row in lines[id:]:
            # Avoid ban
            time.sleep(random.uniform(0.3, 0.8))
            id += 1

            word = row.strip()
            if not word:
                log_crawler_error(ERROR_FILE, id, word, 'vocab')
                continue

            data = None
            for _ in range(5):
                try:
                    data = crawler_word_data(word)
                except Exception as e:
                    log_crawler_error(ERROR_FILE, id, word, 'exception' + str(e))
                    continue
                if data: break

            if not data:    
                log_crawler_error(ERROR_FILE, id, word, 'no_data')
                continue


            record = {"id": str(id), "data": data}
            output.write(json.dumps(record, ensure_ascii=False) + "\n")
            output.flush()

            save_current_id(SAVE_FILE, id)


if __name__ == "__main__":
    thread_1 = (["crawl_vocab_1/dict-word-1.xml","crawl_vocab_1/vocab1.txt","crawl_vocab_1/vocab1.ndjson","crawl_vocab_1/save.txt","crawl_vocab_1/error.log"],)
    thread_2 = (["crawl_vocab_2/dict-word-2.xml","crawl_vocab_2/vocab2.txt","crawl_vocab_2/vocab2.ndjson","crawl_vocab_2/save.txt","crawl_vocab_2/error.log"],)
    thread_3 = (["crawl_vocab_3/dict-word-3.xml","crawl_vocab_3/vocab3.txt","crawl_vocab_3/vocab3.ndjson","crawl_vocab_3/save.txt","crawl_vocab_3/error.log"],)
    thread_4 = (["crawl_vocab_4/dict-word-4.xml","crawl_vocab_4/vocab4.txt","crawl_vocab_4/vocab4.ndjson","crawl_vocab_4/save.txt","crawl_vocab_4/error.log"],)
    thread_5 = (["crawl_vocab_5/dict-word-5.xml","crawl_vocab_5/vocab5.txt","crawl_vocab_5/vocab5.ndjson","crawl_vocab_5/save.txt","crawl_vocab_5/error.log"],)
    thread_6 = (["crawl_vocab_6/dict-word-6.xml","crawl_vocab_6/vocab6.txt","crawl_vocab_6/vocab6.ndjson","crawl_vocab_6/save.txt","crawl_vocab_6/error.log"],)


    crawlers = [
        Process(target=main, args=thread_1),
        Process(target=main, args=thread_2),
        Process(target=main, args=thread_3),
        Process(target=main, args=thread_4),
        Process(target=main, args=thread_5),
        Process(target=main, args=thread_6),
    ]
    for c in crawlers:
        c.start()
    for c in crawlers:
        c.join()

    