from agno.agent import Agent 
from agno.models.groq import Groq 
from agno.tools.website import WebsiteTools
from crewai_tools import SerperDevTool

from tools.twitter import scrape_twitter_fn

def create_agents():

    scrape_website_tool = WebsiteTools()
    search_tool = SerperDevTool()

    twitter_scraper_agent = Agent(
        name="Twitter Post Scraper",
        role="your goal is to scrape a twitter profile to get a list of posts from a given profile",
        tools=[scrape_twitter_fn],
        model=Groq(id="llama-3.3-70b-versatile")
    )

    web_researcher_agent = Agent(
        name="Web Researcher",
        role="Your goal is to search for relevant content about the comparison between Llama 2 and Llama 3",
        tools=[search_tool],
        tool_call_limit=15000,
        #max_content_length=7000,
        model=Groq(id="gemma2-9b-it")
    )
    
    # Doppelganger agent
    doppelganger_agent = Agent(
        name="Doppelganger Agent",
        role="You will create a Twitter post on given topic similar to the given username's writing style "
             "observed in the Twitter posts scraped by the Twitter Post Scraper.",
        model=Groq(id="llama-3.3-70b-versatile")
    )
    
    return twitter_scraper_agent, web_researcher_agent, doppelganger_agent




