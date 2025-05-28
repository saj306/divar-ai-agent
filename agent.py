import os
from scrapling import Fetcher
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import requests

# Get DIVAR_API_KEY from environment variables
# This will be set by the main.py file when it loads the .env file
DIVAR_API_KEY = os.getenv('DIVAR_API_KEY')


def search_car_in_divar(city: str = "tehran", tool_context: ToolContext = None) -> dict:
    """Searches for cars in Divar.ir based on specified city.

    Args:
        city (str): The city to search in (default: "tehran").
        tool_context (ToolContext): Provides access to session state.

    Returns:
        dict: A dictionary containing the search results.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'result' key with car listings.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: search_car_in_divar called for city: {city} ---")
    
    try:
        fetcher = Fetcher()
        x = fetcher.get(f"https://divar.ir/s/{city}/auto", stealthy_headers=True)

        name = x.css('div.unsafe-kt-post-card__info > h2::text')
        price = x.css('div.unsafe-kt-post-card__info > div:nth-child(3)::text')
        km = x.css('div.unsafe-kt-post-card__info > div:nth-child(2)::text')

        output = list(zip(name, price, km))
        
        # Save the last search details to state if tool_context exists
        if tool_context:
            tool_context.state["last_search_city"] = city
            tool_context.state["last_search_type"] = "car"
            print(f"--- Tool: Updated state 'last_search_city': {city} ---")

        return {"status": "success", "result": output}
    except Exception as e:
        print(f"--- Tool: Error searching cars in {city}: {str(e)} ---")
        return {"status": "error", "error_message": f"Could not search for cars in {city}: {str(e)}"}

# Tool 2: Get details for a specific Divar post
def get_divar_post_details(post_id: str, tool_context: ToolContext = None) -> dict:
    """Retrieves detailed information for a specific Divar post by ID.

    Args:
        post_id (str): The unique identifier for the post.
        tool_context (ToolContext): Provides access to session state.

    Returns:
        dict: A dictionary containing the post details.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'details' key with post information.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_divar_post_details called for post_id: {post_id} ---")
    
    try:
        url = f"https://api.divar.ir/v1/open-platform/finder/post/{post_id}"
        headers = {"X-Api-Key": DIVAR_API_KEY}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            post_data = response.json()
            
            # Save the last viewed post to state if tool_context exists
            if tool_context:
                tool_context.state["last_viewed_post_id"] = post_id
                print(f"--- Tool: Updated state 'last_viewed_post_id': {post_id} ---")
                
            return {"status": "success", "details": post_data}
        else:
            error_msg = f"API returned status code: {response.status_code}"
            return {"status": "error", "error_message": error_msg}
    except Exception as e:
        print(f"--- Tool: Error getting post details for {post_id}: {str(e)} ---")
        return {"status": "error", "error_message": f"Could not get post details: {str(e)}"}


# Tool 3: Search for real estate in Divar
def search_real_estate_in_divar(city: str = "tehran", tool_context: ToolContext = None) -> dict:
    """Searches for real estate listings in Divar.ir based on specified city.

    Args:
        city (str): The city to search in (default: "tehran").
        tool_context (ToolContext): Provides access to session state.

    Returns:
        dict: A dictionary containing the search results.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'result' key with real estate listings.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: search_real_estate_in_divar called for city: {city} ---")
    
    try:
        fetcher = Fetcher()
        x = fetcher.get(f"https://divar.ir/s/{city}/real-estate", stealthy_headers=True)

        title = x.css('div.unsafe-kt-post-card__info > h2::text')
        price = x.css('div.unsafe-kt-post-card__info > div:nth-child(3)::text')
        details = x.css('div.unsafe-kt-post-card__info > div:nth-child(2)::text')

        output = list(zip(title, price, details))
        
        # Save the last search details to state if tool_context exists
        if tool_context:
            tool_context.state["last_search_city"] = city
            tool_context.state["last_search_type"] = "real_estate"
            print(f"--- Tool: Updated state 'last_search_city': {city} ---")

        return {"status": "success", "result": output}
    except Exception as e:
        print(f"--- Tool: Error searching real estate in {city}: {str(e)} ---")
        return {"status": "error", "error_message": f"Could not search for real estate in {city}: {str(e)}"}

# Tool 4: Simple greeting tool
def say_hello(name: str = "عزیز") -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str, optional): The name of the person to greet. Defaults to "there".

    Returns:
        str: A friendly greeting message.
    """
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"سلام {name}! به دستیار هوشمند دیوار خوش آمدی!"

# Tool 5: Simple farewell tool
def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "خدانگهدار! امیدوارم که توانسته باشم کمکتان کنم. روز خوبی داشته باشید!"

# Define specialized sub-agents

# Greeting Agent
greeting_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Handles simple greetings and welcomes users to the Divar assistant.",
    instruction="You are the Greeting Agent for Divar. Your ONLY task is to provide a friendly Persian greeting to the user. "
               "Use the 'say_hello' tool to generate the greeting. "
               "If the user provides their name, make sure to pass it to the tool. "
               "Do not engage in any other conversation or tasks.",
    tools=[say_hello],
)

# Farewell Agent
farewell_agent = Agent(
    name="farewell_agent",
    model="gemini-2.0-flash",
    description="Handles simple farewells and goodbyes in Persian.",
    instruction="You are the Farewell Agent for Divar. Your ONLY task is to provide a polite Persian goodbye message. "
               "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
               "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you', 'خداحافظ', 'بای'). "
               "Do not perform any other actions.",
    tools=[say_goodbye],
)

# Car Search Agent
car_search_agent = Agent(
    name="car_search_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for searching car listings on Divar.ir.",
    instruction="You are the Car Search Agent for Divar.ir. Your specific responsibility is to help users find car listings. "
               "Use the 'search_car_in_divar' tool to search for cars in the specified city (default 'tehran'). "
               "Present results in a clear, structured format with bullet points. "
               "Include important details such as price and specifications when available. "
               "Use a mix of Persian and English as appropriate. "
               "If errors occur, explain them clearly and suggest alternatives.",
    tools=[search_car_in_divar],
)

# Real Estate Search Agent
real_estate_agent = Agent(
    name="real_estate_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for searching real estate listings on Divar.ir.",
    instruction="You are the Real Estate Search Agent for Divar.ir. Your specific responsibility is to help users find property listings. "
               "Use the 'search_real_estate_in_divar' tool to search for properties in the specified city (default 'tehran'). "
               "Present results in a clear, structured format with bullet points. "
               "Include important details such as price, location, and property features when available. "
               "Use a mix of Persian and English as appropriate. "
               "If errors occur, explain them clearly and suggest alternatives.",
    tools=[search_real_estate_in_divar],
)

# Post Details Agent
post_details_agent = Agent(
    name="post_details_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for retrieving detailed information about specific Divar listings by their post ID.",
    instruction="You are the Post Details Agent for Divar.ir. Your specific responsibility is to retrieve and present detailed information about posts. "
               "Use the 'get_divar_post_details' tool to fetch comprehensive information about a specific listing using its ID. "
               "Present the details in a clear, structured format. "
               "Organize information into categories like title, price, description, contact information, and location. "
               "Use a mix of Persian and English as appropriate based on the data returned. "
               "If errors occur (like post not found or API issues), explain them clearly to the user and suggest alternatives. "
               "Remember to advise users that they need the specific post ID to use this functionality.",
    tools=[get_divar_post_details],
)

# Root Agent with delegation
root_agent = Agent(
    name="divar_assistant",
    model="gemini-2.0-flash",
    description=(
        "A helpful assistant for searching car and real estate listings on Divar.ir. "
        "This agent delegates to specialized agents for specific tasks."
    ),    instruction=(
        "You are the main coordinator for the Divar.ir assistant. Your role is to intelligently delegate tasks to specialized sub-agents: "
        
        "1. 'greeting_agent': Handles all greetings and welcome messages. Delegate to it for phrases like 'hello', 'hi', 'سلام'. "
        "2. 'farewell_agent': Handles all goodbyes and conversation endings. Delegate to it for phrases like 'bye', 'خداحافظ'. "
        "3. 'car_search_agent': Handles all car-related searches. Delegate to it for any car search queries. "
        "4. 'real_estate_agent': Handles all property-related searches. Delegate to it for any real estate queries. "
        "5. 'post_details_agent': Handles retrieving detailed information about specific Divar posts when users provide a post ID. "
           "Delegate to it when users mention 'details', 'specific post', 'more info', 'post ID', or provide an ID like 'post_123'. "
        
        "Analyze each user query carefully and delegate to the most appropriate agent. "
        "If a query doesn't clearly fit any specialized agent, provide a helpful response explaining the Divar assistant's capabilities. "
        
        "When delegating, let the specialized agents handle their domains completely - don't provide answers for their specialties yourself. "
        "If combining multiple topics, delegate sequentially to the appropriate agents."
        "َALWAYS ANSWER COMPLETE IN PERSIAN, USING A MIX OF PERSIAN AND ENGLISH AS APPROPRIATE, BUT YOUR MAIN LANGUAGE IS PERSIAN"
    ),    tools=[],
    sub_agents=[greeting_agent, farewell_agent, car_search_agent, real_estate_agent, post_details_agent]
)

