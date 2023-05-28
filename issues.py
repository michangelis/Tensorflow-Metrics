import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


# Load all the data from json file and prints attributes
def all_data():
    with open('issues.json') as f:
        for line in f:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)

                # Extract desired fields
                backend_name = data.get('backend_name')
                backend_version = data.get('backend_version')
                category = data.get('category')
                body = data['data'].get('body')
                closed_at = data['data'].get('closed_at')
                comments = data['data'].get('comments')
                created_at = data['data'].get('created_at')
                html_url = data['data'].get('html_url')
                labels = data['data'].get('labels')
                title = data['data'].get('title')
                updated_at = data['data'].get('updated_at')
                user_login = data['data']['user'].get('login')

                # Print the extracted data
                print('Backend Name:', backend_name)
                print('Backend Version:', backend_version)
                print('Category:', category)
                print('Body:', body)
                print('Closed At:', closed_at)
                print('Comments:', comments)
                print('Created At:', created_at)
                print('HTML URL:', html_url)
                print('Labels:', labels)
                print('Title:', title)
                print('Updated At:', updated_at)
                print('User Login:', user_login)
                print('---')

            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue


def total_issues_plot():
    # Load JSON data from file
    issues_by_date = {}

    with open('issues.json') as f:
        for line in f:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)

                # Extract desired fields
                created_at = data['data'].get('created_at')

                if created_at:
                    # Convert the creation date to a datetime object and then format it as a string
                    created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").date()

                    # Increase the count of issues created on this date
                    if created_date in issues_by_date:
                        issues_by_date[created_date] += 1
                    else:
                        issues_by_date[created_date] = 1

            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue

    # Sort the data by date
    sorted_dates = sorted(issues_by_date.items())

    # Split the data into two lists for plotting
    dates, issue_counts = zip(*sorted_dates)

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(dates, issue_counts)
    plt.title('Number of Issues Created Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Issues')
    plt.tight_layout()
    plt.show()


# pie chart of issues open and closed
def open_close_issues():
    # Load JSON data from file
    issues_by_state = {"open": 0, "closed": 0}

    with open('issues.json') as f:
        for line in f:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)

                # Extract desired fields
                state = data['data'].get('state')

                if state:
                    # Increase the count of issues in this state
                    issues_by_state[state] += 1

            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue

    # Prepare data for pie chart
    states = list(issues_by_state.keys())
    counts = list(issues_by_state.values())

    # Plot the data
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=states, autopct='%1.1f%%')
    plt.title('Issue States')
    plt.show()


# prints bar chart depending on the filter type of the issue

# comp:tensorboard: This label indicates that the issue or pull request is related to TensorBoard, a suite of visualization tools provided with TensorFlow. "Comp" likely stands for "component".

# type:#docs-bug: #This label denotes that the issue is related to a bug in the projects documentation.

# cla: yes: The "cla" stands for Contributor License Agreement. The "yes" indicates that the contributor has signed the CLA, which is usually a requirement for contributing to open source projects. This helps ensure that the project has the right to use their contribution.

# cla: no: Conversely, this label means that the contributor has not yet signed the CLA, and their contribution cannot be accepted until they do.

# stat:contribution welcome: This label is an invitation for contributors, indicating that help from the community on this issue would be appreciated. "Stat" is likely short for "status".
def issue_type():
    # Load JSON data from file
    issues_by_label = defaultdict(int)

    with open('issues.json') as f:
        for line in f:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)

                # Extract desired fields
                labels = data['data'].get('labels')

                if labels:
                    for label in labels:
                        # Increase the count of issues with this label
                        issues_by_label[label['name']] += 1

            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue

    # Prepare data for bar chart
    labels = list(issues_by_label.keys())
    print(labels)
    counts = list(issues_by_label.values())

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='blue')
    plt.ylabel('Number of Issues')
    plt.xlabel('Labels')
    plt.title('Issues by Label')
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.tight_layout()
    plt.show()

issue_type()
