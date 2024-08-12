import requests
import pandas as pd
from datetime import datetime, timedelta
import argparse

# List of topics to search for
topics = ["deep-learning", "machine-learning", "deep-neural-networks", "ml", "neural-network"]

# Function to get repositories for a specific topic
def get_repos_for_topic(topic, start_time):
    params = {
        "q": f"topic:{topic} created:>{start_time}",
        "sort": "stars",
        "order": "desc"
    }
    url = "https://api.github.com/search/repositories"
    response = requests.get(url,  params=params)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Failed to retrieve data for topic {topic}: {response.status_code} - {response.text}")
        return []
    

def get_repos(weeks: int = 12):

    start_time = (datetime.now() - timedelta(weeks=weeks)).isoformat() + "Z"


    # Combine results from all topics
    all_repos = []
    for topic in topics:
        repos = get_repos_for_topic(topic, start_time)
        all_repos.extend(repos)

    # Remove duplicates by repository ID (since some repos may have multiple matching topics)
    unique_repos = {repo["id"]: repo for repo in all_repos}.values()

    # Extract relevant information and convert to DataFrame
    repos_data = [{
        "name": repo["name"],
        "full_name": repo["full_name"],
        "description": repo["description"],
        "html_url": repo["html_url"],
        "stargazers_count": repo["stargazers_count"],
        "language": repo["language"],
        "created_at": repo["created_at"]
    } for repo in unique_repos]

    df = pd.DataFrame(repos_data)

    # Sort the DataFrame by stargazers_count in descending order
    df = df.sort_values(by="stargazers_count", ascending=False)


    # Save as formatted JSON with indentation
    df.to_json("deep_learning_repos.json", orient="records", indent=4)

    # Display the DataFrame
    print(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get top deep learning repositories on GitHub")
    parser.add_argument("--weeks", type=int, default=12, help="Number of weeks to search back")
     # Parse arguments
    args = parser.parse_args()

    # Call get_repos with the number of weeks provided
    get_repos(args.weeks)