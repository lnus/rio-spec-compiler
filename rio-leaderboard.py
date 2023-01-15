# API Documentation: https://raider.io/api
# This specific route is for the Mythic+ Leaderboard
# But it isn't actually documented on the API page
# Is it private? Is it undocumented? Who knows
# But it works, so I'm using it
#
# https://raider.io/api/mythic-plus/rankings/specs?region=world&season=season-df-1&class=shaman&spec=enhancement&page=1

from matplotlib import pyplot as plt
import pandas as pd
import requests

from time import sleep
from tqdm import tqdm

# Top x players
top_x = 5000

# Get the page where the top x player is
# There are 20 players per page
max_page = top_x // 20

# Set the region, season, class, and spec
region = "world"
season = "season-df-1"
class_ = "shaman"
spec = "enhancement"

# Set the page number (starts at 0)
page = 0

# Set the URL
url = "https://raider.io/api/mythic-plus/rankings/specs?region=" + region + \
    "&season=" + season + "&class=" + class_ + \
    "&spec=" + spec + "&page=" + str(page)

# Get the data for page 0
data = requests.get(url).json()

# Polling the API for the rest of the pages
print("Polling the API for the rest of the pages...")

# We need to rate limit the API calls to 300 calls per minute
# So we'll sleep for 0.21 seconds between each call
# The 0.01 second sleep is to REALLY make sure we don't go over the limit
for page in tqdm(range(1, max_page)):
    # Set the URL
    url = "https://raider.io/api/mythic-plus/rankings/specs?region=" + region + \
        "&season=" + season + "&class=" + class_ + \
        "&spec=" + spec + "&page=" + str(page)

    # Get the data for the page
    data_page = requests.get(url).json()

    # Append the data
    data["rankings"]["rankedCharacters"].extend(
        data_page["rankings"]["rankedCharacters"])

    # Sleep for 0.21 seconds
    sleep(0.21)


# Create a list of the talent builds
talent_builds = []
ranked_characters = data["rankings"]["rankedCharacters"]

# Loop through the data
print("Compiling talent builds...")

for character in tqdm(ranked_characters):
    # Get the talent build
    talent_build = character["character"]["talentLoadoutText"]

    # Add the talent build to the list
    talent_builds.append(talent_build)

# Create a dataframe
df = pd.DataFrame(talent_builds, columns=["Talent Build"])

# Get the top x talent builds
number_of_builds = 10

top_talent_builds = df["Talent Build"].value_counts().head(10)
top_talent_builds.plot(
    kind="barh", title=f"Top {number_of_builds} Talent Builds")
plt.savefig("rio-leaderboard-talent-builds.png", bbox_inches="tight")

# Also export the data to a CSV file
top_talent_builds = top_talent_builds.to_frame()
top_talent_builds.columns = ["Count"]
top_talent_builds.index.name = "Talent Build"

# Add a column for the percentage
top_talent_builds["Percentage"] = top_talent_builds["Count"] / \
    top_talent_builds["Count"].sum() * 100

# Add a column for the talent calculator URL
# The URL follows this format:
# https://www.wowhead.com/talent-calc/blizzard/{talent_string}"
top_talent_builds["Talent Calculator URL"] = "https://www.wowhead.com/talent-calc/blizzard/" + \
    top_talent_builds.index

top_talent_builds.to_csv("rio-leaderboard-talent-builds.csv")

exit(0)
