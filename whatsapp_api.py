import requests

def send_message_to_bot(message):
    TOKEN = "5676411409:AAF9ORfw7-6Aa3cPQL8Jq-Tmne6cupzH_40"
    chat_id = "5736256441"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())
