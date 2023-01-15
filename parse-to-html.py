# Read from the CSV file and create a HTML file with the talent calculator embeds
import pandas as pd
from airium import Airium

# Read the CSV file
top_talent_builds = pd.read_csv("rio-leaderboard-talent-builds.csv")
embeds = []

# Create a fresh HTML file with embeds for the talent calculator
for index, row in top_talent_builds.iterrows():
    # Get the talent string
    talent_string = row[0]

    # Create the embed URL
    embed_url = "https://www.wowhead.com/talent-calc/embed/blizzard/" + talent_string

    # Create the HTML
    html = f'<iframe src={embed_url} width="100%" height="800" frameborder="0"></iframe>'

    data = {
        "index": index + 1,
        "talent_string": talent_string,
        "embed": html,
        "count": row[1],
        "percent": row[2],
    }

    embeds.append(data)

a = Airium()

a('<!DOCTYPE html>')

with a.html(lang='en'):
    with a.head():
        a.meta(charset='utf-8')
        a.title("Top 10 Talent Builds")
        # do not use CSS from this URL in a production, it's just for an educational purpose
        a.link(href='https://unpkg.com/@picocss/pico@1.4.1/css/pico.css',
               rel='stylesheet')
    with a.body():
        for data in embeds:
            with a.main(klass='container'):
                with a.h1():
                    a(f"{data['index']}. {data['count']} - {data['percent']}%")
                a.break_source_line()
                a(data["embed"])
                a.br()
                with a.span():
                    a(data["talent_string"])

filename = "rio-leaderboard-talent-builds"
with open(filename, "wb") as f:
    html = str(a)
    html_bytes = bytes(html, "utf-8")
    f.write(html_bytes)

exit(0)
