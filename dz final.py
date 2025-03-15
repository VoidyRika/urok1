import sqlite3
import requests
from bs4 import BeautifulSoup


conn = sqlite3.connect('black_clover_characters.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
)
''')
conn.commit()


url = 'https://blackclover.fandom.com/ru/wiki/Список_персонажей'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}


response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


characters = []

for item in soup.select('.mw-parser-output ul li a'):
    try:
        name = item.text.strip()
        link = item['href']
        full_link = f'https://blackclover.fandom.com{link}'

        char_response = requests.get(full_link, headers=headers)
        char_soup = BeautifulSoup(char_response.text, 'html.parser')

        description_tag = char_soup.find('div', class_='mw-parser-output').find('p')
        description = description_tag.text.strip() if description_tag else "Описание отсутствует"

        characters.append((name, description))
    except Exception:
        continue

cursor.executemany('INSERT INTO characters (name, description) VALUES (?, ?)', characters)
conn.commit()

cursor.execute('SELECT * FROM characters')
rows = cursor.fetchall()

print("\nСохранённые персонажи из 'Чёрного клевера':")
for row in rows:
    print(f'ID: {row[0]}, Имя: {row[1]}, Описание: {row[2]}')

conn.close()