import requests
import openai
import nltk
nltk.download('punkt')

openai.api_key = "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"
PDF_URL = "https://arxiv.org/pdf/2303.12712.pdf"
res = requests.get(PDF_URL)
with open('xx.pdf', 'wb') as f:
    f.write(res.content)

from pypdf import PdfReader
from nltk.tokenize import sent_tokenize

pdf_name = "xx.pdf"
reader = PdfReader(pdf_name)
number_of_pages = len(reader.pages)

chunks = []

for i in range(number_of_pages):
    page = reader.pages[i]
    text = page.extract_text()
    sentences = sent_tokenize(text)
    input_sentences = ''

    for sentence in sentences:
        input_sentences += sentence
        if len(input_sentences) > 1000:
            chunks.append(input_sentences)
            input_sentences = ''
    chunks.append(input_sentences)

with open("text.txt", "w", encoding='utf-8') as file:
    for chunk in chunks:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "请你成为文章翻译的小帮手，请协助翻译以下技术文件，以简体中文输出"},
                {"role": "user", "content": chunk},
            ]
        )

        print('原文: ', chunk)

        print('翻译结果: ', completion.choices[0].message.content)
        try:
            file.write('原文: ' + chunk + "\n")
            file.write('翻译结果: ' + completion.choices[0].message.content + "\n")
        except Exception as e:
            print("程序发生错误: " + e + "\n")
            continue