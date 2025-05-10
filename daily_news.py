import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = " ".join([para.get_text() for para in paragraphs])
        return article_text
    except:
        return ""

# Chuẩn bị nội dung email
email_content = ""

# Lấy tin từ RSS
for source, url in rss_feeds.items():
    email_content += f"\n>>> {source} <<<\n"
    feed = feedparser.parse(url)
    for entry in feed.entries[:3]:  # Lấy 3 bài đầu mỗi nguồn
        article_text = get_article_content(entry.link)
        if article_text:
            summary = summarize_text(article_text)
            # Format theo yêu cầu
            email_content += f"Tiêu đề: {entry.title}\n"
            email_content += f"Link: {entry.link}\n"
            email_content += f"Tóm tắt: {summary}\n\n"

# -------- GỬI EMAIL --------
sender = "migoi1410@gmail.com"
receiver = "migoi1410@gmail.com"
password = "xlmz yrcj meuy gqwr"  # App password

subject = "Tóm tắt tin tức hôm nay"
body = f"Chào bạn,\n\nDưới đây là các tin nổi bật hôm nay:\n\n{email_content}\nChúc bạn một ngày tốt lành!"

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    print("Email đã được gửi.")
except Exception as e:
    print("Lỗi khi gửi email:", e)
