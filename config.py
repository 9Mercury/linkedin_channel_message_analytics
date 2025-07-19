import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default values for configuration
INPUT_CSV_FILE = os.getenv("INPUT_CSV_FILE", "messages.csv")  # Changed to environment variable
MESSAGE_COLUMN = os.getenv("MESSAGE_COLUMN", "message")  # Changed to environment variable


TOPIC_KEYWORDS = {
    "Project Management": ["project", "schedule", "deadline", "task", "planning", "agile", "scrum"],
    "Marketing": ["marketing", "advertising", "brand", "campaign", "SEO", "social media"],
    "Technology": ["technology", "AI", "machine learning", "cloud", "data science", "software"],
    "General": ["hello", "thanks", "agree", "comment", "thoughts", "meeting"] #example for general messages
}