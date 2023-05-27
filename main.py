import pandas as pd
import json
import re

def check_bug_fix(pull_request_title, pull_request_description):
    keywords = ['fix', 'bug', 'issue', 'error', 'defect']
    lower_title = pull_request_title.lower() if pull_request_title else ''
    lower_description = pull_request_description.lower() if pull_request_description else ''
    pattern = '|'.join(keywords)
    match = re.search(pattern, lower_title + lower_description)
    if match:
        return True
    else:
        return False

def calculate_pr_that_fix_bug(pull_requests):
    count = 0
    for pull_request in pull_requests:
        if check_bug_fix(pull_request['data']['title'], pull_request['data']['body']):
            count += 1
    return count

# Load the pull requests from the JSON file
with open('pull_requests.json', 'r') as file:
    pull_requests = [json.loads(line) for line in file]

# Create a DataFrame from the pull request data
df = pd.DataFrame(pull_requests)

# Calculate code churn metrics
total_lines_added = df['data'].apply(lambda x: x['additions']).sum()
total_lines_deleted = df['data'].apply(lambda x: x['deletions']).sum()
net_lines_changed = total_lines_added - total_lines_deleted

print("Total lines added:", total_lines_added)
print("Total lines deleted:", total_lines_deleted)
print("Net lines changed (added - deleted):", net_lines_changed)

# Example analysis: Count the number of pull requests
total_pull_requests = len(df)
print("Total number of pull requests:", total_pull_requests)

# Example analysis: Print details of each pull request
for idx, row in df.iterrows():
    pr_number = row['data']['number']
    pr_title = row['data']['title']
    pr_description = row['data']['body']
    pr_author = row['data']['user']['login']
    print("Pull Request #{}: {} (by {})".format(pr_number, pr_title, pr_author))

# Example analysis: Calculate average number of comments per pull request
average_comments = df['data'].apply(lambda x: x['comments']).mean()
print("Average number of comments per pull request:", average_comments)
print(calculate_pr_that_fix_bug(pull_requests))
# Perform additional data analysis or calculations as needed
# ...

