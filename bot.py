import requests
import time
from configs import settings
from botfunctions import *


def get_last_updates(offset):
    update = requests.get(f'{settings.URL}{settings.BOT_TOKEN}/getUpdates'
                          f'?offset={offset}')

    return update


def send_message(user_id, text):
    requests.post(
        f'{settings.URL}{settings.BOT_TOKEN}/sendMessage?chat_id={user_id}&text={text}')


def start_bot():
    offset = 0

    while True:
        time.sleep(5)
        print('за работу')
        last_messages = get_last_updates(offset).json()
        buttons_with_diets_in_message = {"inline_keyboard": [show_diets_for_buttons()]}

        for message in last_messages['result']:

            if 'message' in message:
                discussion_id = message['message']['chat']['id']

                if 'text' not in message['message']:
                    continue

                if message['message']['text'] == '/start':

                    if is_user_in_db(discussion_id):
                        send_message(discussion_id,
                                     'вы уже зарегистрированы')

                    else:
                        create_user_in_db(discussion_id)
                        send_message(discussion_id,
                                     'теперь выберите диету (для ознакомления с перечнем диет напишите /список)')

                elif message['message']['text'] == '/список':
                    show_diets()
                    send_message(discussion_id, f"перечень доступных диет: {show_diets()}")
                    send_message(discussion_id,
                                 'для выбора диеты напишите /диеты)')

                elif message['message']['text'] == '/диеты':
                    buttons = {"chat_id": str(discussion_id), "text": "какую диету желаете выбрать?",
                               "reply_markup": buttons_with_diets_in_message}
                    requests.post(
                        f'{settings.URL}{settings.BOT_TOKEN}/sendMessage', json=buttons)

                if message['message']['text'] == '/закончить диету':
                    if is_user_details_in_db(discussion_id):
                        delete_user(discussion_id)
                    else:
                        send_message(discussion_id,
                                     'вы не зарегистрированы')

                if message['message']['text'] == '/питание':
                    if is_user_in_db(discussion_id):
                        send_message(discussion_id,
                                     f"список продуктов, входящих в выбранную диету: {show_products_in_message(discussion_id)}."
                                     f"\nдля продуктивного соблюдения диеты суммарное количество потребленных каллорий не дылжно привышать X."
                                     f"\nучитывайте, количество каллорий указано на 100 грамм продукта.")


            elif "callback_query" in message:
                discussion_id = message["callback_query"]["message"]["chat"]["id"]
                message_id_for_editing = message["callback_query"]["message"]["message_id"]
                diet = message["callback_query"]["data"]
                edited_reply = {"inline_keyboard": [edit_buttons()]}
                requests.post(
                    f"{settings.URL}{settings.BOT_TOKEN}/editMessageReplyMarkup?chat_id={discussion_id}&message_id={message_id_for_editing}",
                    json=edited_reply)
                if is_user_details_in_db(discussion_id):
                    update_diet_in_user_details(discussion_id, diet)
                    send_message(discussion_id, 'вы успешно сменили диету')
                    send_message(discussion_id, 'чтобы узнать список продуктов входящих в вашу диету напишите /питание')
                else:
                    create_user_details_in_db(discussion_id, diet)
                    send_message(discussion_id, 'диета успешно выбрана')
                    send_message(discussion_id, 'чтобы узнать список продуктов входящих в вашу диету напишите /питание')
            if message:
                offset = message['update_id'] + 1
