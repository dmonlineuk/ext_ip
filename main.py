import requests
import sqlite3
import dotenv
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

def fetch_ip():
    response = requests.get("https://icanhazip.com/")
    return response.text.strip()


def init_db():
    conn = sqlite3.connect("ip_address.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ip_address (
              id INTEGER PRIMARY KEY AUTOINCREMENT CHECK (id = 1)
            , ip_address TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO ip_address (ip_address) VALUES ('0.0.0.0')")
    conn.commit()
    conn.close()


def load_ip_from_db():
    conn = sqlite3.connect("ip_address.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ip_address FROM ip_address WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def save_ip_to_db(ip):
    conn = sqlite3.connect("ip_address.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE ip_address SET ip_address = ? WHERE id = 1", (ip,))
    conn.commit()
    conn.close()


def send_msg(old_ip, new_ip):
    config = dotenv.dotenv_values(".env")
    configuration = clicksend_client.Configuration()
    configuration.username = config.get("USERNAME")
    configuration.password = config.get("API_KEY")
    api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))
    sms_message = SmsMessage(
        source="python",
        body=f"IP Address changed from {old_ip} to {new_ip}",
        to=config.get("TO_NUMBER"),
        schedule=1436874701
    )
    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
    try:
        api_response = api_instance.sms_send_post(sms_messages)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMSApi->sms_send_post: %s\n" % e)


def main():
    config = dotenv.dotenv_values(".env")
    init_db()
    old_ip = load_ip_from_db()
    print(f"Old IP: {old_ip}")
    ip = fetch_ip()
    print(f"New IP: {ip}")
    save_ip_to_db(ip)
    if old_ip != ip:
        send_msg(old_ip, ip)

if __name__ == "__main__":
    main()