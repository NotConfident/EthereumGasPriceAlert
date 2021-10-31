import json 
import requests
import time
import urllib

TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
chatIDs = []
offset = 0
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset):
    url = URL + "getUpdates"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    offset = js['result'][0]['update_id']
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    try:
      text = updates["result"][last_update]["message"]["text"]
      chat_id = updates["result"][last_update]["message"]["chat"]["id"]
      return (text, chat_id)
    except Exception as e:
      pass

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_update_verify(updates, chatIDs):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    try:
      if(updates["result"][last_update]['my_chat_member']['new_chat_member']['status'] == 'kicked'):
        chatIDs.remove(updates["result"][last_update]['my_chat_member']['chat']['id'])
      
      if(updates["result"][last_update]['my_chat_member']['new_chat_member']['status'] == 'member'):
        chatIDs.append(updates["result"][last_update]['my_chat_member']['chat']['id'])
      
    except Exception as e:
        pass


def echo_all(chatIDs):
  for i in chatIDs:
        message = ''
        try:
            url_Gas = ""
            response = requests.request(
            "GET",
            url_Gas
            )

            text = json.loads(response.text)
            low = text['result']['SafeGasPrice']
            medium = text['result']['ProposeGasPrice']
            high = text['result']['FastGasPrice']

            if (int(medium) <= 40):
              message = "GO GO GO LOW GAS PRICE ✅ \n\nLow ❤️: " + low + " gwei \nMedium 🤔: " + medium + " gwei \nHigh 😢: " + high + " gwei"
              send_message(message, i)
            else:
              message = "Current Gas Price 😒 \n\nLow ❤️: " + low + " gwei \nMedium 🤔: " + medium + " gwei \nHigh 😢: " + high + " gwei"
              send_message(message, i)

        except Exception as e:
            print(e)


def main():
    while True:
      get_last_update_verify(get_updates(offset), chatIDs)
      updates = get_last_chat_id_and_text(get_updates(offset))
      print(updates)
      print(chatIDs)

      try:
        if updates[1] not in chatIDs:
          chatIDs.append(updates[1])
          echo_all(chatIDs)
          time.sleep(5)
        else:
          echo_all(chatIDs)
          time.sleep(5)
          continue

      except Exception as e:
        pass


if __name__ == '__main__':
    main()