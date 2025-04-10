import os
import time
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Load environment variables from .env file
dotenv.load_dotenv()

def parse_html_content(page_source: str):
    """
    Parses the HTML from Twitter's profile and returns a collection of Twitter posts.
    
    Args:
        page_source: The HTML content

    Returns:
        A list of article elements representing Twitter posts
    """
    twitter_soup = BeautifulSoup(page_source, "lxml")
    containers = twitter_soup.select('article[data-testid="tweet"]')
    return containers

def get_post_content(container):
    """
    Gets the content of a Twitter post container
    
    Args:
        container: The article container for a tweet

    Returns:
        The post content
    """
    try:
        text_element = container.select_one('div[data-testid="tweetText"]')
        if text_element:
            return text_element.text.strip()
    except Exception as e:
        print(f"Error extracting tweet content: {e}")
    return ""

def get_twitter_posts(page_source: str):
    """
    Extract tweets from Twitter profile page HTML
    
    Args:
        page_source: The HTML content of the Twitter profile page
        
    Returns:
        A list of tweet texts
    """
    containers = parse_html_content(page_source)
    posts = []

    for container in containers:
        post_content = get_post_content(container)
        if post_content:
            posts.append(post_content)

    return posts

def login_to_twitter(browser):
    """
    Login to Twitter using credentials from .env file
    
    Args:
        browser: Selenium webdriver instance
        
    Returns:
        True if login successful, False otherwise
    """
    # Get credentials from .env file
    username = os.environ.get("TWITTER_USERNAME")
    password = os.environ.get("TWITTER_PASSWORD")
    
    if not username or not password:
        print("Twitter credentials not found in .env file")
        return False
    
    try:
        # Navigate to Twitter login page
        browser.get("https://x.com/login")
        time.sleep(3)  # Wait for page to load
        
        # Enter username
        username_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for next page
        
        # Twitter sometimes asks for additional verification with email/phone
        try:
            # Check if verification screen appears
            verify_field = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            # If we're here, it's asking for verification
            # Get email or phone from env
            verification_id = os.environ.get("TWITTER_EMAIL", username)
            verify_field.send_keys(verification_id)
            verify_field.send_keys(Keys.RETURN)
            time.sleep(2)
        except:
            # No verification needed, continue
            pass
        
        # Enter password
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for login to complete
        time.sleep(5)
        
        # Check if login was successful (we should be on the home page)
        if "home" in browser.current_url or "x.com" in browser.current_url:
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False
            
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def scrape_twitter_fn(username=None):
    """
    A tool that can be used to scrape public Twitter/X posts from a specified username
    First logs in using credentials from .env file, then scrapes posts
    
    Args:
        username: The Twitter username to scrape posts from
        
    Returns:
        A string representation of the scraped posts
    """
    if not username:
        # Default to a username from environment variables, or use a default
        username = os.environ.get("TWITTER_TARGET", "elonmusk")
    
    # Initialize the browser
    browser = webdriver.Chrome()
    
    # Login to Twitter first
    login_success = login_to_twitter(browser)
    
    if not login_success:
        print("Could not login to Twitter. Attempting to scrape without login.")
    
    # Navigate to the target Twitter profile
    browser.get(f"https://x.com/{username}")
    
    # Wait for page to load
    time.sleep(3)
    
    # Scroll down a few times to load more tweets
    for _ in range(3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    # Extract tweets from the page
    posts = get_twitter_posts(browser.page_source)
    browser.quit()
    
    # Return the first few tweets
    return str(posts[:5])