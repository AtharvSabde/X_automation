from agno.team.team import Team  
from agno.agent import Agent
from agno.models.groq import Groq


from agents import create_agents



def main():
    # Get user input for Twitter username
    twitter_username = input("Enter Twitter username to analyze (press Enter for default 'elonmusk'): ")
    if not twitter_username:
        twitter_username = "elonmusk"
    
    # Get user input for topic
    topic = input("Enter the topic for the Twitter post: ")
    if not topic:
        topic = "Llama 3 AI capabilities"
    
    # Create the agents
    twitter_scraper_agent, web_researcher_agent, doppelganger_agent = create_agents()
    
    # Create a multi-agent using the Agent class with team parameter
    multi_ai_agent = Agent(
        team=[twitter_scraper_agent, web_researcher_agent, doppelganger_agent],
        show_tool_calls=True,
        model=Groq(id="llama-3.3-70b-versatile"),
        markdown=True
    )
    
    # Run the multi-agent with a prompt incorporating the user inputs
    result = multi_ai_agent.print_response(
        f"""Please perform the following tasks in sequence:
        1. Scrape recent posts from {twitter_username}'s Twitter account to analyze writing style
        2. Research information about "{topic}"
        3. Create a Twitter post about "{topic}" in the writing style of {twitter_username}
        """
    )

# Only call the main function if this file is run directly
if __name__ == "__main__":
    main()