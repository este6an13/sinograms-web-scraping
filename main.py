import requests
from bs4 import BeautifulSoup
import urllib.request
from googletrans import Translator
from gtts import gTTS
from PyDictionary import PyDictionary
import translators as ts

translator = Translator()
dictionary = PyDictionary()


def run():
    for page in range(115, 116):

        print("===============================================================")
        print("PAGE {}/164".format(page))
        print("===============================================================")

        response = requests.get('https://graphemica.com/unicode/characters/page/{}'.format(page))
        soup = BeautifulSoup(response.text, 'html.parser')
        char_containers = soup.select('.has-char')

        with open('chars_{}.txt'.format(page), 'w+', encoding = "utf-8") as chars_file:
            for container in range(0, 256):

                #if page == 81 and container < 231:
                #    continue

                #if page == 164 and container == 21:
                #    break

                print("CHAR {}/255".format(container))

                char = char_containers[container].div.string
                char = char.replace("\n", "")
                char_response = requests.get('https://graphemica.com/{}'.format(char))
                char_soup = BeautifulSoup(char_response.text, 'html.parser')

                try:
                    tts = gTTS(char, lang='zh-CN')
                    tts.save('C:\\users\\dequi\\Desktop\\Coding\\Python_Codes\\sinochars\\pronunciations\\{}.mp3'.format(char))
                    pronun_file_name = '{}.mp3'.format(char)
                except:
                    pronun_file_name = 'unable to generate'

                try:
                    definition = char_soup.find(id="kdefinition-body").contents[0]
                    definition = definition.replace("\n", "")
                except:
                    definition = "NONE"

                definitions = definition.split(';')

                translations_obj = []

                for df in definitions:
                    try:
                        translations_obj.append(ts.bing(df, 'es'))
                    except:
                        translations_obj.append("Not able to translate")

                translations = []

                for translation in translations_obj:
                    try:
                        translations.append(translation.text)
                    except:
                        translations.append('NONE')


                images_urls = []

                for df in definitions:
                    if df == "NONE":
                        break
                    if df == '(Cant.)' or df == '(Can.)':
                        df = df.split(') ')[1]
                    imgs_response = requests.get('https://www.gettyimages.es/fotos/{}?family=creative&license=rf&phrase={}&sort=mostpopular#license'.format(df.replace(' ', '-'), df.replace(' ', '%20')))
                    imgs_soup = BeautifulSoup(imgs_response.text, 'html.parser')
                    try:
                        img = imgs_soup.select('.gallery-asset__thumb')[0]
                        images_urls.append(img.get('src'))
                    except:
                        images_urls.append("NONE")



                attributes = char_soup.find_all('td')
                for attr in attributes:
                    try:
                        if attr.string.replace("\n", "") == 'Unicode Code Point':
                            ucp = attr.find_next_sibling('td').string
                            ucp = ucp.replace("\n", "")
                            continue
                        if attr.string.replace("\n", "") == 'Strokes':
                            strokes = attr.find_next_sibling('td').string
                            strokes = strokes.replace("\n", "")
                            continue
                        if attr.string.replace("\n", "") == 'Pinyin (Mandarin Romanization)':
                            pinyin = attr.find_next_sibling('td').string
                            pinyin = pinyin.replace("\n", "")
                            continue
                        if attr.string.replace("\n", "") == 'kRSKangXi' or attr.string.replace("\n", "") == 'kRSUnicode':
                            radical = attr.find_next_sibling('td').find_next_sibling('td').string
                            radical = radical.replace("\n", "")
                            continue
                    except:
                        continue

                chars_file.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(char, definitions, translations, images_urls, ucp, strokes, pinyin, radical, pronun_file_name))
                chars_file.write('\n\n')
                print('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(char, definitions, translations, images_urls, ucp, strokes, pinyin, radical, pronun_file_name))
                print()




if __name__ == '__main__':
    run()
