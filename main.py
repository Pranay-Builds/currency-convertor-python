import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel, QComboBox, 
                             QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt

class CurrencyConvertorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Convertor")
        self.setFixedSize(500, 400)
        self.initUI()
    
    def initUI(self):
        
        vbox = QVBoxLayout()

        self.title = QLabel("Currency Convertor", self)
        self.title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.title)

        self.base_currency = QLabel("Base Currency: ", self)
        self.base_currency.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.base_currency)
        self.fromCurrency = QComboBox()
        
        vbox.addWidget(self.fromCurrency)
        
        self.target_currency = QLabel("Target Currency: ", self)
        self.target_currency.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.target_currency)
        self.toCurrency = QComboBox()
        
        vbox.addWidget(self.toCurrency)

        self.amount = QLineEdit(self)
        self.amount.setPlaceholderText("Enter Amount To Convert")
        vbox.addWidget(self.amount)

        self.submitBtn = QPushButton("Convert", self)
        vbox.addWidget(self.submitBtn)

        self.result = QLabel(self)
        vbox.addWidget(self.result)
        self.result.setAlignment(Qt.AlignCenter)

        self.fetchCurrencies()

        self.setLayout(vbox)

        self.title.setObjectName("title")
        self.base_currency.setObjectName("labelCurrency")
        self.target_currency.setObjectName("labelCurrency")
        self.amount.setObjectName("amount")
        self.submitBtn.setObjectName("submitBtn")
        self.result.setObjectName("result")


        self.setStyleSheet("""
        QWidget {
            background-color: #f0f0f0;
            font-family: calibri;
        }

        QLabel#title {
            font-size: 40px;
            font-weight: bold;
        }

        QLabel#labelCurrency {
            font-size: 25px;
        }

        QLineEdit {
            font-size: 25px;
            border: 1px solid black;
            padding: 10px;
            border-radius: 10px;
        }

        QComboBox {
            font-size: 20px;
            border: 1px solid black;
            padding: 5px;
            border-radius: 5px;
            margin-bottom: 8px;
        }

        QPushButton#submitBtn {
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            background-color: rgb(0, 234, 255);
            color: white;
            padding: 10px;
        }

        QLabel#result {
            font-size: 25px;
        }
        """)

        self.submitBtn.clicked.connect(self.fetchCurrency)
    
    def fetchCurrencies(self):
        api_key = "2829b4a3940a5a9bddce8803"

        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            conversion_rates = data["conversion_rates"]

            self.fromCurrency.addItems(conversion_rates.keys())
            self.toCurrency.addItems(conversion_rates.keys())

            self.fromCurrency.setCurrentIndex(-1)
            self.toCurrency.setCurrentIndex(-1)
        else:
            self.displayError("An error occured while trying to call the API")

    def fetchCurrency(self):
        base_currency = self.fromCurrency.currentText()
        target_currency = self.toCurrency.currentText()
        amount = float(self.amount.text().replace(",", ""))

        if not base_currency or not target_currency or not amount:
            self.displayError("Please fill all fields")
            QMessageBox.warning(self, "Error!", "Please fill all the fields")
            return


        if base_currency == target_currency:
            self.displayError("Base and Target currency cannot be the same")
            QMessageBox.warning(self, "Error!", "You are trying to convert a currency to itself")
            return
        
             
        try:
            amount = float(amount)
        except ValueError:
            self.displayError("Please enter a valid number for the amount")
            QMessageBox.warning(self, "Error!", "Invalid amount entered")
            return

        if amount <= 0:
            self.displayError("Amount cannot be 0 or lesser")
            QMessageBox.warning(self, "Error!", "The amount cannot be 0")
            return
        
        api_key = "2829b4a3940a5a9bddce8803"
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            conversion_rate = data["conversion_rates"][target_currency]

            result = conversion_rate * amount

            self.result.setText(f"{amount} {base_currency} = {result:.2f} {target_currency}")  
        else:
            QMessageBox.warning(self, "Error Fetching Data", f"An error occured while trying to fetch data: {response.status_code}")
            self.displayError("An error occured while trying to call the API")

    def displayError(self, message):
        self.result.setText(message)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConvertorApp()
    window.show()
    sys.exit(app.exec_())