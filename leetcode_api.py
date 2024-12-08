import requests
from config import LEETCODE_AUTH_COOKIE
from suggest import suggest_questions


def fetch_all_questions():
    url = "https://leetcode.com/graphql"
    # headers = {
    #     "Content-Type": "application/json",
    #     "x-csrftoken": "8sB8s1cBW6WCBRH3UV5NYyJR9Ba6sMqzyXrLBFJwuIUGNYFZlxeOcjLZ1CnQPL0W",
    #     "Cookie": f"LEETCODE_SESSION={LEETCODE_AUTH_COOKIE}",
    # }
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        total: totalNum
        questions: data {
          acRate
          difficulty          
          frontendQuestionId: questionFrontendId                    
          status
          title
          titleSlug
          topicTags {
            name
            id
            slug
          }          
        }
      }
    }
    """
    payload = {
        "operationName": "problemsetQuestionList",
        "variables": {"categorySlug": "", "skip": 0, "limit": 50, "filters": {}},
        "query": query,
    }
    response = requests.post(url, json=payload)
    # print(response.json())
    if response.status_code == 200:
        return response.json()["data"]["problemsetQuestionList"]["questions"]
    else:
        raise Exception(
            f"Failed to fetch questions: {response.status_code}, {response.text}"
        )


def fetch_last_solved_questions(username, limit):
    """
    Fetch the solved question slugs of a particular user using LeetCode GraphQL API.

    Args:
        username (str): The LeetCode username.
        offset (int): Pagination offset (default: 0).
        limit (int): Number of solved questions to fetch (default: 10).

    Returns:
        list: A list of question slugs solved by the user.
    """
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={LEETCODE_AUTH_COOKIE}",
    }
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
    """
    payload = {
        "operationName": "recentAcSubmissions",
        "variables": {"username": username, "limit": limit},
        "query": query,
    }

    response = requests.post(url, json=payload, headers=headers)
    print(
        "Last solved question response",
        response.json()["data"]["recentAcSubmissionList"],
    )
    if response.status_code == 200:
        submissions = response.json()["data"]["recentAcSubmissionList"]
        return submissions
    else:
        raise Exception(
            f"Failed to fetch solved questions: {response.status_code}, {response.text}"
        )


def suggest_similar_questions(last_solved_data):
    """
    Suggest similar questions based on the last solved question.

    Args:
        last_solved_data (list): List containing the last solved question data.

    Returns:
        None: Prints suggested questions.
    """
    if not last_solved_data:
        print("No data found for the last solved question.")
        return

    # Extract the `titleSlug` of the last solved question
    last_question_slug = last_solved_data[0]["titleSlug"]
    print(f"Last solved question slug: {last_question_slug}")

    # Use the `titleSlug` to query for similar questions
    suggestions = suggest_questions(
        last_question_slug
    )  # Function queries the vector database

    return suggestions
    # Print the suggestions
    if suggestions:
        print("Here are the suggestions:")
        for suggestion in suggestions:
            print(
                f"- {suggestion['title']} (Difficulty: {suggestion['difficulty']}, Tags: {suggestion['tags']})"
            )
    else:
        print("No similar questions found.")
