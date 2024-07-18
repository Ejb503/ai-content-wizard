api_key = "tufvkF8zRBWT8n5MxwZdo7T1s"
api_secret_key = "XwKIWpOFGDR7D19H51ibiMqJuxEpQ4bm25iPInyll2aG7SX9xY"
access_token = "1796149119817334784-5QX51547jvmYXn5GlAzkKt4XQmuoy2"
access_token_secret = "t4FaArbDBmfLLSUfdyuh2yEofGFvwdMGKA1T93bMsFOXE"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANBquwEAAAAAaYYL5kMQcb1928gWuB1Jb0k%2FLPM%3DjX2AGI9QpYG5pgL8toAqWv5aIrnNgddNhp945BQrRViVzR3XJN"

from requests_oauthlib import OAuth1Session

request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(api_key, client_secret=api_secret_key)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the api_key or api_secret_key you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    api_key,
    client_secret=api_secret_key,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    api_key,
    client_secret=api_secret_key,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def post_tweet(text, reply_to_id=None):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}
    response = oauth.post(url, json=payload)
    if response.status_code == 201:
        print("Successfully posted tweet.")
        return response.json()['data']['id']
    else:
        print(f"Failed to post tweet: {response.status_code} {response.text}")
        return None

def post_thread(tweets):
    conversation_id = None
    for tweet in tweets:
        conversation_id = post_tweet(tweet, reply_to_id=conversation_id)

tweets = [
        "1. Breakthrough: Large Vision-Language Models revolutionize emotion recognition! New study shows AI can understand context-aware emotions without extensive training. #AIEmotionRecognition",
        "2. Traditional emotion recognition models are limited by datasets and bias. LVLMs offer a solution with their vast knowledge and generalization abilities. #AIInnovation",
        "3. Researchers propose a training-free framework for emotion recognition using LVLMs. This could make advanced AI more accessible and adaptable. #AIAccessibility",
        "4. LVLMs outperform traditional models in context-aware emotion recognition tasks, even without additional training. A game-changer for AI applications. #AIAdvancement",
        "5. Few-shot learning with LVLMs shows competitive results in emotion recognition. This could reduce the need for large labeled datasets in AI development. #AIEfficiency",
        "6. The study explores three paradigms: fine-tuning, zero-shot/few-shot evaluation, and Chain-of-Thought reasoning. Each shows unique strengths in emotion recognition. #AIResearch",
        "7. LVLMs demonstrate powerful reasoning and generalization capabilities, paving the way for more comprehensive and fine-grained emotion analysis. #AIUnderstanding",
        "8. Incorporating Chain-of-Thought reasoning in LVLMs improves interpretability in emotion recognition, crucial for building trust in AI systems. #ExplainableAI",
        "9. The future of emotion analysis: moving towards broader, more nuanced emotional landscapes using large AI models. #FutureOfAI",
        "10. This research could impact fields beyond AI, including psychology and neuroscience, by providing new tools for studying emotional expression and perception. #AIImpact"
    ]

post_thread(tweets)
