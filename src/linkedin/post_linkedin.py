import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=783ujjjxg3mzod&redirect_uri=http://localhost&scope=profile%20w_member_social%20openid
# author = "YOUR_AUTHOR_ID"

# data = {
#     'grant_type': 'authorization_code',
#     'code': 'AQSzgQu2Py07J4wpqc0RKt5n7aq2ZnQxJcc57ePXjbPB3fsB7ogJYoxl4JDHfZ7DGO4u1_ATGUtrxVEoTacn-R4STj0jk7GUS-uE2rWrNHM0qLwmUOkVv1rd8emWXu8Kf8Vuzb235po_gAtFlI6FcvsMpvAtgteApXvT0vhbS_VFPrYvnGTHWNbzwbUWdCjGhn8Qk19E5V-ZTbAyXXc',
#     'redirect_uri': 'http://localhost',
#     'client_id': '783ujjjxg3mzod',
#     'client_secret': 'aTojCHz7BUOeQSZx'
# }

# response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data=data)
# access_token = response.json()
access_token = 'AQSzgQu2Py07J4wpqc0RKt5n7aq2ZnQxJcc57ePXjbPB3fsB7ogJYoxl4JDHfZ7DGO4u1_ATGUtrxVEoTacn-R4STj0jk7GUS-uE2rWrNHM0qLwmUOkVv1rd8emWXu8Kf8Vuzb235po_gAtFlI6FcvsMpvAtgteApXvT0vhbS_VFPrYvnGTHWNbzwbUWdCjGhn8Qk19E5V-ZTbAyXXc'
print("Access token:", access_token)

linkedin_post = {
    "headline": "Large Vision-Language Models Show Promise in Context-Aware Emotion Recognition",
    "paragraph1": "A recent study explores the potential of Large Vision-Language Models (LVLMs) in context-aware emotion recognition (CAER). Traditional approaches often struggle with dataset limitations and annotator biases. This research investigates how LVLMs can overcome these challenges through fine-tuning, zero-shot/few-shot learning, and Chain-of-Thought reasoning.",
    "paragraph2": "The authors propose a novel training-free framework that leverages LVLMs' in-context learning capabilities. Their methodology includes a Demonstration Retrieval Module, carefully designed prompts, and an Inference Module. Experiments were conducted on EMOTIC and HECO datasets using LLAVA-7B and VILA-8B models.",
    "paragraph3": "Results show that LVLMs can achieve competitive performance in CAER tasks, even without additional training. The few-shot paradigm demonstrated particularly promising results, with VILA achieving 47.55% accuracy on the HECO dataset, surpassing the traditional EMOT-Net model's 38.80%.",
    "paragraph4": "This research has significant implications for emotion recognition technology. It suggests the potential for more nuanced, adaptable, and generalizable emotion recognition systems that require less training data. Future work will focus on improving the Chain-of-Thought process for better reasoning and decision-making during inference.",
    "hashtags": [
        "#EmotionRecognition",
        "#AI",
        "#MachineLearning",
        "#ComputerVision",
        "#NLP"
    ],
    "call_to_action": "What are your thoughts on the potential impact of this research on human-AI interaction and emotion understanding?"
}

post_text = """
Large Vision-Language Models Show Promise in Context-Aware Emotion Recognition

A recent study explores the potential of Large Vision-Language Models (LVLMs) in context-aware emotion recognition (CAER). Traditional approaches often struggle with dataset limitations and annotator biases. This research investigates how LVLMs can overcome these challenges through fine-tuning, zero-shot/few-shot learning, and Chain-of-Thought reasoning.

The authors propose a novel training-free framework that leverages LVLMs' in-context learning capabilities. Their methodology includes a Demonstration Retrieval Module, carefully designed prompts, and an Inference Module. Experiments were conducted on EMOTIC and HECO datasets using LLAVA-7B and VILA-8B models.

Results show that LVLMs can achieve competitive performance in CAER tasks, even without additional training. The few-shot paradigm demonstrated particularly promising results, with VILA achieving 47.55% accuracy on the HECO dataset, surpassing the traditional EMOT-Net model's 38.80%.

This research has significant implications for emotion recognition technology. It suggests the potential for more nuanced, adaptable, and generalizable emotion recognition systems that require less training data. Future work will focus on improving the Chain-of-Thought process for better reasoning and decision-making during inference.

#EmotionRecognition, #AI, #MachineLearning #ComputerVision #NLP
"""

def post_to_linkedin(access_token, post_text):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    post_data = {
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    # Log the attempt to post
    logging.info("Attempting to post to LinkedIn...")
    
    try:
        response = requests.post(url, headers=headers, json=post_data)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        # Log successful post
        logging.info("Successfully posted to LinkedIn.")
        return response.json()
    except requests.exceptions.HTTPError as err:
        # Log HTTP errors
        logging.error(f"HTTP error occurred: {err}")
    except Exception as err:
        # Log any other errors
        logging.error(f"An error occurred: {err}")

post_to_linkedin(access_token, post_text)

def get_user_info(access_token):
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for 4XX/5XX responses
        user_info = response.json()
        print("User Info:", user_info)
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")

# Example usage
# get_user_info(access_token)