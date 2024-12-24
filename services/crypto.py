import requests

CRYPTOBOT_API_URL = "https://pay.crypt.bot/api/"

class CryptoBot:
    def __init__(self, token: str):
        self.token = token

    def create_invoice(self, amount: float, currency: str, description: str) -> dict:
        url = CRYPTOBOT_API_URL + "createInvoice"
        payload = {
            "token": self.token,
            "amount": amount,
            "currency": currency,
            "description": description
        }
        response = requests.post(url, json=payload)
        return response.json()

    def check_invoice(self, invoice_id: str) -> dict:
        url = CRYPTOBOT_API_URL + "getInvoice"
        payload = {
            "token": self.token,
            "invoice_id": invoice_id
        }
        response = requests.post(url, json=payload)
        return response.json()
