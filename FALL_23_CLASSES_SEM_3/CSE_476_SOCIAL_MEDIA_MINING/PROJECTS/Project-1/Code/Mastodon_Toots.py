from datetime import datetime
import json
from html import unescape
import html2text
import re
from urllib.parse import urlparse

from googletrans import Translator, LANGUAGES
url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class MastodonToot:
    def __init__(self, data):
        self.id = data.get('id', None)
        self.account_id = data['account']['id'] if 'account' in data and 'id' in data['account'] else None
        accountNoteContent = self.preProcessStr(data['account']['note']) if 'account' in data and 'note' in data['account'] else None
        nonHTMLContent = self.preProcessStr(data.get('content', ''))
        if data.get('language') == 'en':
            self.content = nonHTMLContent
            self.account_note = accountNoteContent
        else:
            try:
                self.content = self.get_en_version(nonHTMLContent)
                self.account_note = self.get_en_version(accountNoteContent)
            except Exception as e:
                print(f"Translation error: {e}")
                self.content = None  # Set content to None on exception
                self.account_note = None  # Set account_note to None on exception


    def preProcessStr(self, input_str):
        return self.remove_urls(self.parse_html_content(input_str).replace(r'\n',''))
    
    def get_en_version(self, text_to_translate):
        translator = Translator()
        target_language = "en"
        return translator.translate(text_to_translate, dest=target_language).text

    def parse_html_content(self, html_content):
        # Remove HTML tags and unescape HTML entities
        h = html2text.HTML2Text()
        h.ignore_links = True
        return h.handle(html_content)

    def to_dict(self):
        # Convert the MastodonToot object to a dictionary
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_note': self.account_note.replace('\n', ''),
            'content': self.content.replace('\n', ''),
        }

    def remove_urls(self, text):        
        return re.sub(url_pattern, '', text)
    
def parse_toots(data_list):
    return [MastodonToot(data) for data in data_list]


def get_user_ids(data_list):
    user_ids = []
    for user in data_list:
        user_ids.append(user.account_id)
    return user_ids

def store_to_json(filename, toots):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump([vars(toot) for toot in toots], json_file, ensure_ascii=False, indent=4, cls=DateTimeEncoder)

def read_data_from_JSON(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data