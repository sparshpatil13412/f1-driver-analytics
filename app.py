from flask import Flask, render_template
import pandas as pd
from ast import literal_eval

app = Flask(__name__)


def parse_seasons(value):
    if isinstance(value, list):
        return value
    return literal_eval(value)


df = pd.read_csv(
    r'E:\Sparsh Python Programming folder\f1-driver-analytics\data\F1Drivers_Dataset.csv',
    converters={"Seasons": parse_seasons}
)
groups = pd.read_csv(
    r'E:\Sparsh Python Programming folder\f1-driver-analytics\data\Driver_clusters.csv'
)
teams = pd.read_csv(
    r'E:\Sparsh Python Programming folder\f1-driver-analytics\data\f1_teams_complete_full_names.csv'
)
teams['constructor_championships'] = teams['constructor_championships'].fillna(0)
teams["total_podiums"] = teams["total_podiums"].fillna(0)
teams["total_points"] = teams["total_points"].fillna(
    teams['total_points'].mean()
)
teams["last_year"] = teams["last_year"].fillna(
    teams['last_year'].mode()[0]
)
teams["first_year"] = teams["first_year"].fillna(
    teams['first_year'].mode()[0]
)
teams["win_rate"] = teams["win_rate"].fillna(
    teams['win_rate'].mean()
)
teams["podium_rate"] = teams["podium_rate"].fillna(
    teams['podium_rate'].mean()
)
team_groups = pd.read_csv(
    r'E:\Sparsh Python Programming folder\f1-driver-analytics\data\Team_clusters.csv')

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    head = df.head(2)
    return render_template('dashboard.html', head=head)


@app.route('/drivers')
def drivers():
    drivers_list = []

    for driver in df["Driver"].unique():
        nationality = df[df["Driver"] == driver]["Nationality"].iloc[0]

        drivers_list.append({
            "name": driver,
            "nationality": nationality
        })

    return render_template(
        "drivers.html",
        drivers=drivers_list
    )

@app.route('/drivers/<string:driver_id>')
def driver_detail(driver_id):
    driver_id = driver_id.replace('-', ' ')

    driver = df[df["Driver"] == driver_id].iloc[0]
    championships = driver["Championships"]
    if isinstance(championships, float):
        championships = int(championships)
        driver["Championships"] = championships

    group = None

    if driver_id in groups["Driver"].values:
        group = groups.loc[
            groups["Driver"] == driver_id,
            "Group"
        ].iloc[0]
        if group == "Group 1":
            group = "Champion Tier"
        elif group == "Group 2":
            group = "Established Drivers"
        elif group == "Group 3":
            group = "GOAT Tier"
        else:
            group = "Supporting Grid"

    return render_template(
        'driver_detail.html',
        driver=driver,
        group=group
    )


@app.route('/teams')
def teams_page():
    team_list = []
    for team in teams["name"].unique():
        championships = teams[teams["name"] == team]["constructor_championships"].iloc[0]
        podiums = teams[teams["name"] == team]["total_podiums"].iloc[0]
        points = teams[teams["name"] == team]["total_points"].iloc[0]
        first_year = teams[teams["name"] == team]["first_year"].iloc[0]
        last_year = teams[teams["name"] == team]["last_year"].iloc[0]
        if isinstance(first_year, float):
            first_year = int(float(first_year))
        if isinstance(last_year, str):
            if last_year == "Still on the goddamn grid":
                last_year = last_year
            else:
                last_year = int(float(last_year))
        championships = int(championships)

        team_list.append(
            {
                "name": team,
                "championships": championships,
                "podiums": podiums,
                "points": points,
                "first_year": first_year,
                "last_year": last_year
            }
        )
    return render_template('teams.html', teams=team_list)


@app.route('/teams/<string:team_id>')
def team_detail(team_id):
    team_id = team_id.replace('-', ' ')

    team_data = teams[
        teams["name"].str.lower() == team_id.lower()
    ]

    if team_data.empty:
        return "Team not found", 404

    team = team_data.iloc[0]

    first_year = team["first_year"]
    if isinstance(first_year, float):
        first_year = int(first_year)
        team["first_year"] = first_year
    
    championships = team["constructor_championships"]
    if isinstance(championships, float):
        championships = int(championships)
        team["constructor_championships"] = championships
    
    podiums = team["total_podiums"]
    if isinstance(podiums, float):
        podiums = int(podiums)
        team["total_podiums"] = podiums

    group = None

    if team_id in team_groups["Team"].values:
        group = team_groups.loc[
            team_groups["Team"] == team_id,
            "Group"
        ].iloc[0]
        if group == "Group 1":
            group = "Legendary Constructors"
        elif group == "Group 2":
            group = "Grid Participants"
        elif group == "Group 3":
            group = "Elite Dynasties"
        else:
            group = "Competitive Constructors"
    
    return render_template('team_detail.html', team=team, group=group)


@app.route('/champions')
def champions():
    return render_template('champions.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')

    
if __name__ == '__main__':
    app.run(debug=True)
