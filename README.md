# ☁️ Historical Weather Scraping Project with Selenium

<div style="text-align: center;">
  <img src="assets/selenium_banner.png" alt="project-cover" />
</div>

## 📝 Project Overview

This project involves scraping historical weather data for **five cities** from the website [Wunderground](https://www.wunderground.com). The goal is to gather daily weather data, such as temperature, precipitation, and wind, from the start of the year up to the current date. This information will be used by **SetMagic Productions** to aid in film location planning, helping to analyze weather conditions for ideal shoot timing.

The data will be scraped with Selenium, cleaned, processed, and stored for further analysis, supporting the company's decision-making in choosing the best filming locations based on weather patterns.

### Key Objectives:
1. Scrape weather data for **five cities**.
2. Organize the data into a structured format (e.g., pandas DataFrame).
3. Save temporal checkpoint `.csv` files for every processed city.
4. Clean and process the weather data for easy access and analysis.
5. Enable data-driven decisions for optimal filming schedules.

## 📁 Project Structure

```bash
historical-weather-scraping/
├── assets/                      
│   └── selenium_banner.png
├── data/                        # Folder to store raw and processed weather data
│   └── historical_weather.csv
├── notebooks/                   # Jupyter notebook detailing the scraping process
│   └── historical_weather.ipynb
├── src/                         # Source code for the project
│   └── support_historical_weather.py
├── Pipfile                      # Pipenv dependency management file (optional)
├── Pipfile.lock
├── requirements.txt             # List of required Python packages
└── README.md                    # Project documentation (this file)
```

### Description of Key Files:
- **`notebooks/historical_weather.ipynb`**: Jupyter notebook detailing the full weather data scraping process, including cleaning and saving the data.
- **`src/support_historical_weather.py`**: Python script with helper functions for scraping and processing the data.
- **`data/`**: Directory where the scraped and processed weather data will be stored in CSV format.
- **`assets/`**: Holds external assets, such as images used in documentation or reports.

## 🛠️ Installation and Requirements

To run this project, you will need the following tools and libraries:

- Python 3.8+
- Jupyter Notebook
- `pandas` – Data manipulation and analysis
- `Selenium` – Browser automation and HTML parsing and scraping
- `requests` – Sending HTTP requests to retrieve the data

**Documentation Links:**
- [pandas Documentation](https://pandas.pydata.org/)
- [Selenium Documentation](selenium.dev/documentation/)
- [requests Documentation](https://docs.python-requests.org/en/master/)

### Installing Dependencies

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/historical-weather-scraping.git
   cd historical-weather-scraping
   ```

2. **Set up a virtual environment and install dependencies:**
   If you're using `Pipenv`, you can create the environment and install the packages:
   ```bash
   pipenv install
   pipenv shell
   ```

   Alternatively, use `requirements.txt` with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

## 📊 Usage

1. Open the `notebooks/historical_weather.ipynb` file in Jupyter.
2. Follow the steps inside the notebook to:
   - Scrape weather data for each city.
   - Process and clean the data using pandas.
   - Save intermediate and final results to CSV files.
   
3. **Customization**: You can customize the cities and time ranges by modifying the notebook code. Simply adjust the URLs or scraping parameters to fetch data for different cities or periods.

## 🔍 Results and Conclusions
- **Final Output**: A final, cleaned dataset will be generated, containing weather information for all the selected cities.
- **Analysis**: The collected data, when analysed will provide insights into temperature patterns, precipitation trends, and wind conditions, helping the production team plan for optimal weather conditions at various filming locations.


## 🔄 Next Steps

Some possible enhancements for the project include:
1. **Analysis & Visualization**: Add more advanced data visualization for weather patterns (e.g., heatmaps or trend analysis).
2. **Compare with AEMET data**: Contrast the scraped data with the AEMET database and assess information consistency.

## 🐛 Troubleshooting

### Common Issues:
1. **Connection Errors**: If requests to Wunderground fail, ensure your internet connection is stable. You may also want to implement a retry mechanism in the `support_historical_weather.py` script.
2. **Invalid Data**: Check if the HTML structure of the webpage has changed, which could break the scraper. Updating the BeautifulSoup parsing logic may be necessary.
3. **Dependencies**: If packages are not installed correctly, ensure that you have the right Python version and have installed all dependencies from the `requirements.txt` file.

## 🤝 Contributions

Contributions are welcome! If you have any ideas for improvements or would like to add new features, feel free to:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request detailing your changes.

## ✒️ Authors

- **Miguel López Virués** – [GitHub Profile](https://github.com/MiguelLopezVirues)

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
