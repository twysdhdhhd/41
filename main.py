from flask import Flask, jsonify
import requests, random, string
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_account():
    url = "https://www.oxaam.com/index.php"
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.oxaam.com",
        "Referer": "https://www.oxaam.com/index.php",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\""
    }

    random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@gv.com"
    raw_data = f"name=test&email={random_email}&phone=8882345674&password=cgj86rdchjj&country=Bangladesh"

    with requests.Session() as session:
        response = session.post(url, headers=headers, data=raw_data)

    soup = BeautifulSoup(response.text, 'html.parser')

    email_button = soup.find('button', {'class': 'copy-btn', 'data-copy': True})
    email = email_button['data-copy'] if email_button else 'Not Found'

    password = 'Not Found'
    password_divs = soup.find_all('div', style=lambda value: value and 'gap:.45rem' in value)
    for div in password_divs:
        if 'Password' in div.get_text():
            password_button = div.find('button', {'class': 'copy-btn'})
            if password_button:
                password = password_button['data-copy']
                break

    verification_link = 'Not Found'
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'code' in href and href.endswith('.php'):
            verification_link = href if href.startswith('http') else "https://www.oxaam.com/" + href.lstrip('/')
            break

    return jsonify({
        "email": email,
        "password": password,
        "verification_link": verification_link
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
