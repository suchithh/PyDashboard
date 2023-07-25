# PyDashboard
Functional and intuitive dashboard application written in Python.
![screenshot](https://raw.githubusercontent.com/suchithh/PyDashboard/master/res/screenshot.png)

## Summary
PyDashboard is a clean, intuitive, and functional GUI written in Python. It utilizes the Tkinter module to create a native GUI and leverages various APIs to collect diverse data such as the latest news, financial information, weather data, and COVID-19 statistics. The data is fetched from APIs using the Python requests library in JSON format and subsequently parsed by the json module. The parsed data is then presented in an organized manner within the GUI using Tkinter widgets, including buttons, labels, canvas, and frames, all neatly arranged in a grid layout.

APIs used in the project include:
- Newsapi.org
- Yahoo Finance
- OpenWeatherMap

## Features
- **Intuitive Layout**: PyDashboard is designed with a user-friendly interface, ensuring easy navigation and smooth user experience.
- **Automatic Location Detection: The application automatically detects the user's country and location using the network IP address, providing relevant localized information.
- **Current Weather Information**: Users can access up-to-date weather information for their city, helping them plan their day accordingly.
- **Financial Data**: PyDashboard displays the latest information about user-inputted stocks in a graph, providing a quick overview of stock values.
- **Top News**: Stay informed with the latest news in the user's country, complete with related pictures and a short snippet of the article. Clicking on the news item or text will open the full article in the default web browser.
- **Currency Converter and Exchange Rates**: The application offers a currency converter with real-time exchange rates, making it convenient for users dealing with international currencies.
- **Calendar Manager**: Manage your schedule effectively with a dynamic listing of events based on user preferences.
- **Automatic Dark Theme**: PyDashboard features an automatic dark theme that adjusts based on the time of the day, reducing strain on the user's eyes during low-light conditions.

## How to Use
- Make sure you have Python 3.6 or higher installed on your machine.
- Clone the repository.
- Change directory to the root folder of the project.
- Install the required dependencies by running `pip install -r requirements.txt` in the terminal.
- Run the application by running `python main.py`.
