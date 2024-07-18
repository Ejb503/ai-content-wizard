
import requests
from typing import Optional, List, Tuple
from research_config import HEADERS, SEARCH_URL, SUMMARIZER_URL
from system.logger import setup_logger
logger = setup_logger()
import json

class APIError(Exception):
    """Exception raised for API errors."""
    pass

def get_response_data(question: str) -> Optional[dict]:
    """Send a GET request to the API and return the response data."""
    try:
        params = {"q": question, "summary": "1"}
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
        response.raise_for_status()  
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get response data for question '{question}'. Error: {e}")
        raise APIError from e

def get_summary_response(initial_response: dict, question: str) -> Optional[str]:
    """Get the summary data from the initial response."""
    try:
        summarizer_key = initial_response.get('summarizer', {}).get('key')
        response = requests.get(SUMMARIZER_URL.format(summarizer_key), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get summary data for question '{question}'. Error: {e}")
        raise APIError from e
    
def get_summary_content(summary_response: dict, question: str) -> Optional[str]:
    """Get the summary data from the initial response."""
    try:
        logger.info("Summary response: %s:", summary_response)
        summary_content = summary_response.get('summary', [{}])[0].get('data')
        return summary_content
    except Exception as e:
        logger.error(f"Failed to get summary data for question '{question}'. Error: {e}")
        raise APIError from e
    
def get_research_links(json_response: dict) -> List[str]:
    """Extract the research links from the JSON response."""
    try:
        context = json_response.get('enrichments').get('context', [])
        return [item.get('url') for item in context]
    except Exception as e:
        logger.error(f"Failed to get research links. Error: {e}")
        raise APIError from e

def get_followup_questions(json_response: dict) -> List[str]:
    """Extract the follow-up questions from the JSON response."""
    try:
        followups = json_response.get('followups')
        return followups if followups is not None else []
    except Exception as e:
        logger.error(f"Failed to get followup questions. Error: {e}")
        raise APIError from e

def ask_followup_questions(followup_questions, content_counter, contents, research_links):
    followup_index = 0
    while content_counter < 4 and followup_index < len(followup_questions):
        question = followup_questions[followup_index]
        summary_response, links = ask_question_and_process_response(question)
        summary_content = get_summary_content(summary_response, question)
        if summary_content is not None:
            content_counter += 1 
            contents.append(summary_content)
            research_links.extend(links)
            new_followup_questions = get_followup_questions(summary_response)
            if new_followup_questions:
                content_counter, contents, research_links = ask_followup_questions(new_followup_questions, content_counter, contents, research_links)
        followup_index += 1
    return content_counter, contents, research_links

def ask_question_and_process_response(question: str) -> Tuple[Optional[str], List[str]]:
    """Ask a question and process the response."""
    initial_lookup = get_response_data(question)
    summary_response = get_summary_response(initial_lookup, question)
    research_links = get_research_links(summary_response)
    return summary_response, research_links

def research_post(title, id):
    """Identify the data processor for a company."""
    questions = [title]
    contents = []
    research_links = []
    followup_questions = []
    content_counter = 0

    for i, question in enumerate(questions):
        summary_response, links = ask_question_and_process_response(question)
        summary_content = get_summary_content(summary_response, question)
        if summary_content is not None:
            content_counter += 1 
            contents.append(summary_content)
            research_links.extend(links)
            followup_questions = get_followup_questions(summary_response)
            content_counter, contents, research_links = ask_followup_questions(followup_questions, content_counter, contents, research_links)

    research_links = ",".join(research_links)

    result = ({
            "question": title,
            "content": contents[0] if len(contents) > 0 else "",
            "content_1": contents[1] if len(contents) > 1 else "",
            "content_2": contents[2] if len(contents) > 2 else "",
            "content_3": contents[3] if len(contents) > 3 else "",
            "content_titles": ','.join(questions + followup_questions),
            "link": research_links
        })
    logger.info("Research complete: %s" % result)

    # Save result to a file named research_id.json
    with open(f'/research/{id}_research.json', 'w') as file:
        json.dump(result, file, indent=4)

    return result