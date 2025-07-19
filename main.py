import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string
import logging
import config  # Import the configuration file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download required NLTK data (only needs to be done once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def load_data(file_path, message_column):
    """
    Loads data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        message_column (str): The name of the column containing the message text.

    Returns:
        pandas.DataFrame: A DataFrame containing the data.  Returns None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        if message_column not in df.columns:
            logging.error(f"Message column '{message_column}' not found in the CSV file.")
            return None
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        logging.error(f"The CSV file is empty: {file_path}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the data: {e}")
        return None

def preprocess_text(text):
    """
    Preprocesses text by converting to lowercase, tokenizing, removing punctuation and stop words.

    Args:
        text (str): The text to preprocess.

    Returns:
        list: A list of cleaned tokens.
    """
    if not isinstance(text, str):  # Handle non-string values (e.g., NaN)
        return []

    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    cleaned_tokens = [
        token for token in tokens
        if token not in stop_words and token not in punctuation and token.isalnum()
    ]
    return cleaned_tokens


def analyze_messages(df, message_column):
    """
    Analyzes the messages in the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the message data.
        message_column (str): The name of the column containing the message text.

    Returns:
        tuple: A tuple containing the total messages, average words per message, total characters,
               most frequent words, and a topic counts dictionary.  Returns None if an error occurs.
    """
    try:
        messages = df[message_column].astype(str).tolist() # Ensure messages are strings

        total_messages = len(messages)
        all_tokens = []
        total_characters = 0

        for message in messages:
            cleaned_tokens = preprocess_text(message)
            all_tokens.extend(cleaned_tokens)
            total_characters += len(message)

        average_words_per_message = len(all_tokens) / total_messages if total_messages > 0 else 0
        word_counts = Counter(all_tokens)
        most_frequent_words = word_counts.most_common(10)

        topic_counts = identify_topics(messages)

        return total_messages, average_words_per_message, total_characters, most_frequent_words, topic_counts

    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")
        return None


def identify_topics(messages):
    """
    Identifies topics based on keyword matching.

    Args:
        messages (list): A list of messages (strings).

    Returns:
        dict: A dictionary of topic counts.
    """
    topic_counts = {topic: 0 for topic in config.TOPIC_KEYWORDS}

    for message in messages:
        cleaned_tokens = preprocess_text(message)
        for topic, keywords in config.TOPIC_KEYWORDS.items():
            for keyword in keywords:
                if keyword in cleaned_tokens:
                    topic_counts[topic] += 1
                    break  # Only count the topic once per message

    return topic_counts


def main():
    """
    Main function to execute the message analysis.
    """
    logging.info("Starting message analysis...")

    df = load_data(config.INPUT_CSV_FILE, config.MESSAGE_COLUMN)
    if df is None:
        logging.error("Failed to load data. Exiting.")
        return

    analysis_results = analyze_messages(df, config.MESSAGE_COLUMN)
    if analysis_results is None:
        logging.error("Failed to analyze messages. Exiting.")
        return

    total_messages, average_words_per_message, total_characters, most_frequent_words, topic_counts = analysis_results

    print("\n--- Message Analysis Results ---")
    print(f"Total Messages: {total_messages}")
    print(f"Average Words per Message: {average_words_per_message:.2f}")
    print(f"Total Characters: {total_characters}")
    print("\nMost Frequent Words:")
    for word, count in most_frequent_words:
        print(f"  {word}: {count}")

    print("\nTopic Counts:")
    for topic, count in topic_counts.items():
        print(f"  {topic}: {count}")

    logging.info("Message analysis complete.")


if __name__ == "__main__":
    main()