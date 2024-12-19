import requests
from bs4 import BeautifulSoup
from database import save_event
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

URL = 'https://afisha.ru/chelyabinsk/'


def get_event_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Проверка успешности запроса
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []

        # Измените селекторы в соответствии с текущей структурой сайта
        for event in soup.select('oP17O'):
            name = event.select_one('CjnHd y8A5E nbCNS yknrM').get_text(strip=True)
            date = event.select_one('CEXp3').get_text(strip=True)
            location = event.select_one('PqAdz').get_text(strip=True)
            contact_info = event.select_one('.contact-info').get_text(strip=True) if event.select_one(
                '.contact-info') else 'Информация недоступна'

            events.append({
                'name': name,
                'date': date,
                'location': location,
                'contact_info': contact_info,
                'free_spaces': None
            })

        logging.info(f"Найдено мероприятий: {len(events)}")
        return events

    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


def save_events_to_db(events):
    for event in events:
        save_event(event['name'], event['date'], event['location'], event['free_spaces'], event['contact_info'])


if __name__ == "__main__":
    event_data = get_event_data()
