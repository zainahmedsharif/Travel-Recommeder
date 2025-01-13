# Travel Recommender Application

This repository contains a Python-based travel recommender application that suggests travel destinations based on weather conditions and flight availability. The application uses APIs for weather data and flight inspirations and leverages natural language processing with a large language model (LLM) to interpret user queries.

## Features

- **Weather Analysis**: Fetch historical weather data for specific destinations using the OpenWeather API.
- **Flight Suggestions**: Suggest affordable travel destinations using the Amadeus Flight Inspiration Search API.
- **Natural Language Processing**: Extract user intent and parameters from natural language queries with an LLM.
- **Customizable Agent**: Use LangChain to build and integrate tools into a Zero-Shot Agent for dynamic query handling.

## Prerequisites

1. Python 3.8+
2. An OpenWeather API key
3. An Amadeus API key
4. An OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following keys:
   ```env
   OPENWEATHER_API_KEY=your_openweather_api_key
   AMADEUS_KEY=your_amadeus_client_id
   AMADEUS_SECRET=your_amadeus_client_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

### Running the Application

1. Run the script to get travel suggestions:
   ```bash
   python travel_agent_refactor.py
   ```

2. Modify the query in the script to customize your request. Example:
   ```python
   query = "Suggest a travel destination from Madrid with warm weather on 15-02-2025."
   ```

### Tools Used

- **Weather Fetcher**: Retrieves historical weather data for destinations.
- **Flight Inspiration Search**: Fetches flight destinations and indicative prices.
- **Current DateTime Fetcher**: Resolves relative terms like "next week" to specific dates.

## Example Query

Sample output for the query:
```bash
Suggest a travel destination from Madrid with warm weather on 15-02-2025.
```

Response:
```plaintext
The average temperature at LIS over the last 2 years is 18.5°C. Affordable flights are available to Lisbon for €120.
```

## Repository Structure

- `travel_agent_refactor.py`: Main script for the application.
- `README.md`: Documentation for the project.
- `.env`: Environment variables (not committed to the repository).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributions

Contributions are welcome! Feel free to fork the repository and submit a pull request.

