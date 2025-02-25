
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self) 
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)


        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.get_weather_button.clicked.connect(self.get_weather)


        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri; 
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 74px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji; 
            }
                QLabel#description_label{
                    font-size:     
            }           
        """)

    def get_weather(self):
        
        api_key ="514027084a20d1630bb1a5a34b4f3139"   
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data ["cod"] == 200:
                self.display_weather(data)
        
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")   
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Intenal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")   
                case 503:
                    self.display_error("Service Unavailable\n Server is down")        
                case 504:
                    self.display_error("Gateway Timeout\nNo response form the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")
                
        except requests.execeptions.connectionError:
            self.display_error("connection Error;|nCheck your internet connection")
        except requests.execeptions.Timeout:
            self.display_error("timeone Error:\nThe request is timed out")
        except requests.execeptions.ToomanyRedirects:
            self.display_error("Too many Redirects:\nCheck URL")
        except requests.execeptions.RequestExeception as req_error: 
            self.display_error(f"Request Error:\n{req_error}")
            print(f"Request Error\n{req_error}")

    def display_error(self,):
        pass

    def display_weather(self, data):
        print(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_App = WeatherApp()
    Weather_App.show()
    sys.exit(app.exec_())