import os, certifi, requests
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.tools import tool
import requests

# =====================
# LOAD ENV VARIABLES
# =====================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# =====================
# TOOLS
# =====================

search_tool = TavilySearch(max_result=2)


# custom tool to be used by agent
@tool
def get_weather_data(latitude: float, longitude: float) -> str:
    """
    Fetch current weather information for a location using its
    latitude and longitude.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "units": "metric",
        "appid": OPENWEATHERMAP_API_KEY,
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    response.raise_for_status()
    return (
        f"latitude = {latitude} & longitude = {longitude}\n"
        f"name = {data["name"]}\n"
        f"Temperature = {data["main"]["temp"]}°C\n"
        f"Weather = {data["weather"][0]["description"]}\n"
        f"Humidity = {data["main"]["humidity"]}%"
    )


# =====================
# LLM
# =====================

llm = ChatOpenAI(model="gpt-6-luna", reasoning_effort="none", api_key=OPENAI_API_KEY)

# =====================
# PROMPT
# =====================
agent = create_agent(model=llm, tools=[search_tool, get_weather_data])

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Find the capital of burkino faso "
                    "and then find its weather",
                }
            ]
        }
    )
    print(response["messages"])
    print(response["messages"][-1].text)
