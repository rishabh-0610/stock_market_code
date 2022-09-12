import requests
TOKEN = "5676411409:AAF9ORfw7-6Aa3cPQL8Jq-Tmne6cupzH_40"
chat_id = "5736256441"
message = "hello from your telegram bot"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # this sends the message