import feedparser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt_tab')

# Danh sách RSS feed
rss_feeds = {
    "Cafef_dn": "https://cafef.vn/doanh-nghiep.rss",
    "Cafef_kt": "https://cafef.vn/vi-mo-dau-tu.rss",
    "VnExpress": "https://vnexpress.net/rss/tin-moi-nhat.rss"
}

# Hàm tóm tắt văn bản
def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# Lấy nội dung bài viết từ link
def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = " ".join([para.get_text() for para in paragraphs])
    return article_text

# Lấy tin từ RSS
for source, url in rss_feeds.items():
    print(f"\n>>> {source} <<<")
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:  # lấy 5 bài đầu
        print(f"- {entry.title}")
        print(f"  {entry.link}")
        article_content = get_article_content(entry.link)
        summarized_content = summarize_text(article_content)
        print(f"  Tóm tắt: {summarized_content}")