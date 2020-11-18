import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

@app.route('/')
def home():
    response = requests.post("http://hidden-journey-62459.herokuapp.com/piglatinize/", allow_redirects=False, data = {'input_text': get_fact()})
    pig_latin_url = str(response.headers['Location'])
    pig_latin_page = requests.get(pig_latin_url)
    soup = BeautifulSoup(pig_latin_page.content, "html.parser")
    pig_latin = soup.body.get_text()
    return f"""
    <p><a href=\"{pig_latin_url}\">{pig_latin_url}</a><p>
    <p>{pig_latin}</p>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

