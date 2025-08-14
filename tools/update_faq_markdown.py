"""
This script is used to update the markdown file for FAQs. It fetches the FAQs from the pinned post on r/PESU and
generates a markdown file with the questions and answers. It also marks the questions with the most upvotes as
"Most Asked".
"""

import argparse
import re

import numpy as np
import praw
from dotenv import load_dotenv

load_dotenv()

# read percentile and reddit credentials from command line
parser = argparse.ArgumentParser()
parser.add_argument("--client-id", "-cid", type=str, help="Reddit client ID")
parser.add_argument("--client-secret", "-cs", type=str, help="Reddit client secret")
parser.add_argument("--user-agent", "-ua", type=str, help="Reddit user agent")
parser.add_argument("--percentile", "-p", type=int, default=85,
                    help="percentile value for most asked tag", required=False)
args = parser.parse_args()
print(args)

reddit = praw.Reddit(
    client_id=args.client_id,
    client_secret=args.client_secret,
    user_agent=args.user_agent,
)

# markdown templates
FAQ_TEMPLATE = """---
order: -9
---

# FAQs

These FAQs have been directly sourced from the [r/PESU](https://www.reddit.com/r/PESU/comments/14c1iym/faqs/) subreddit. 
If you would like to add a question or make suggestions, please contact [u/rowlet-owl](https://www.reddit.com/user/rowlet-owl/).

"""

QUESTION_TEMPLATE = "==- {}\n{}\n<br><br>\n\n==-\n\n<br>\n\n"
QUESTION_TEMPLATE_MOST_ASKED = "==- [!badge variant=\"danger\" text=\"Most Asked\"] {}\n{}\n<br><br>\n\n==-\n\n<br>\n\n"

# fetch the FAQs post and obtain the markdown text
faq_post_link = "https://www.reddit.com/r/PESU/comments/14c1iym/faqs/"
faq_post = reddit.submission(url=faq_post_link)
content = faq_post.selftext

# skip these links
skip = [
    "https://www.reddit.com/r/PESU/comments/14c1jiw/how_to_ask_a_question_on_rpesu/",
    "https://www.reddit.com/r/PESU/comments/142gani/pesu_discord/"
]

# find all markdown text which have a link: [example test for link](https://example.com)
question_links = re.findall(r'\[(.*?)\]\((.*?)\)', content)
question_data = list()
upvote_counts = list()
for question, link in question_links:
    try:
        comment = reddit.comment(url=link)
        answer = comment.body.strip()
        upvotes = comment.score
    except praw.exceptions.InvalidURL:
        answer = link
        upvotes = 1

    if link in skip:
        continue

    # add the question and answer to the listt
    question_data.append({
        "question": question.strip(),
        "answer": answer,
        "upvotes": upvotes,
        "link": link,
    })
    upvote_counts.append(upvotes)

# find the nth percentile of upvotes to mark questions with upvotes greater than that as most asked
percentile_value = np.percentile(upvote_counts, args.percentile)
for question in question_data:
    if question["upvotes"] >= percentile_value:
        template = QUESTION_TEMPLATE_MOST_ASKED
    else:
        template = QUESTION_TEMPLATE
    template = template.format(question["question"], question["answer"])
    FAQ_TEMPLATE += template

# write the markdown to a file
with open("faqs.md", "w") as f:
    f.write(FAQ_TEMPLATE)
