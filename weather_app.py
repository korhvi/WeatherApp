import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from config import API_KEY
from PyQt5.QtGui import QPixmap

class WeatherApp(QWidget):
  def __init__(self):
    super().__init__()
    self.city_label = QLabel("Enter city name: ", self)
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

    self.city_label.setObjectName("city_label")
    self.city_input.setObjectName("city_input")
    self.get_weather_button.setObjectName("get_weather_button")
    self.temperature_label.setObjectName("temperature_label")
    self.emoji_label.setObjectName("emoji_label")
    self.description_label.setObjectName("description_label")

    self.setStyleSheet("""
    QLabel, QPushButton {
        font-family: Calibri;
        color: #333;
    }

    QLabel#city_label {
        font-size: 40px;
        font-style: italic;
        color: #2c3e50;
    }

    QLineEdit#city_input {
        font-size: 40px;
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 10px;
        color: #2c3e50;
        background-color: #ecf0f1;
    }

    QLineEdit#city_input:focus {
        border: 2px solid #2980b9;
        background-color: #ffffff;  
    }

    QPushButton#get_weather_button {
        font-size: 30px;
        font-weight: bold;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px;
    }

    QPushButton#get_weather_button:hover {
        background-color: #2980b9;
    }

    QLabel#temperature_label {
        font-size: 75px;
    }

    QLabel#emoji_label {
        font-size: 100px;
        font-family: "Segoe UI Emoji";
        text-align: center;
    }

    QLabel#description_label {
        font-size: 50px;
        color: #34495e;
        font-style: italic;
    }
""")
    
    self.get_weather_button.clicked.connect(self.get_weather)
    self.city_input.returnPressed.connect(self.get_weather)

  def get_weather(self):
    
    API_KEY = "ea7821ad613d4eec3b56bf7ef9887576"
    city = self.city_input.text()
    url =f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    try:
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()

      if data ["cod"] == 200:
        self.display_weather(data)

    except requests.exceptions.HTTPError as http_error:
      match response.status_code:
        case 400:
          self.display_error("Bad Request:\nPlease check your input")
        case 401:
          self.display_error("Unauthorized:\nInvalid Api key")
        case 403:
          self.display_error("Forbidden:\nAccess is denied")
        case 404:
          self.display_error("Not Found:\nCity not found")
        case 500:
          self.display_error("Internal Server Error:\nPlease try later")
        case 502:
          self.display_error("Bad Gateway:\nInvalid response from the server")
        case 503:
          self.display_error("Service Unavaible:\nServer is down")
        case 504:
          self.display_error("Gateway Timeout:\nNo respose from the server")
        case _:
          self.display_error(f"HTTP error occured:\n{http_error}")
          
    except requests.exceptions.ConnectionError:
      self.display_error("Connection Error:\nCheck your internet connection")
    except requests.exceptions.Timeout:
      self.display_error("Timeout Error:\nThe request timed out")
    except requests.exceptions.TooManyRedirects:
      self.display_error("Too many Redirects:\nCheck th URL")
    except requests.exceptions.RequestException as req_error:
      self.display_error(req_error)
    
    

  def display_error(self, message):
    self.temperature_label.setStyleSheet("font-size: 30px;")
    self.temperature_label.setText(message)
    self.emoji_label.clear()
    self.description_label.clear()

  def display_weather(self, data):
      self.temperature_label.setStyleSheet("font-size: 75px;")
      temperature_k = data["main"]["temp"]
      temperature_c = temperature_k - 273.15
      weather_id = data["weather"][0]["id"]
      weather_description = data["weather"][0]["description"]

      self.temperature_label.setText(f"{temperature_c:.0f}°C")

      weather_icon_path = self.get_weather_icon(weather_id)
      if weather_icon_path.endswith('.png'):
          pixmap = QPixmap(weather_icon_path)

          scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
          self.emoji_label.setPixmap(scaled_pixmap)
      else:
          self.emoji_label.clear()
          self.emoji_label.setText(weather_icon_path)

      self.description_label.setText(weather_description)

  @staticmethod
  def get_weather_icon(weather_id):
      if 200 <= weather_id <= 232:
          return "icons/200.png"
      elif 300 <= weather_id <= 321:
          return "icons/300.png"
      elif 500 <= weather_id <= 531:
          return "icons/500.png"
      elif 600 <= weather_id <= 622:
          return "icons/600.png"
      elif 701 <= weather_id <= 741:
          return "icons/701.png"
      elif weather_id == 762:
          return "🌋"
      elif weather_id == 771:
          return "icons/771.png"
      elif weather_id == 781:
          return "🌪️"
      elif weather_id == 800:
          return "icons/800.png"
      elif 801 <= weather_id <= 804:
          return "icons/801.png"
      else:
          return ""

if __name__ == "__main__":
  app = QApplication(sys.argv)
  weather_app = WeatherApp()
  weather_app.show()
  sys.exit(app.exec_())