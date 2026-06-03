from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
df = pd.read_csv(r'E:\Sparsh Python Programming folder\f1-driver-analytics\data\F1Drivers_Dataset.csv')

teams = [
    {
        "id": "mercedes",
        "name": "AMG Mercedes",
        "wins": 19,
        "logo": "/static/images/mercedes-logo.jpg",
        "championships": 18,
        "podiums": 317,
        "points": "8000+"
    },
    {
        "id": "ferrari",
        "name": "Scuderia Ferrari",
        "wins": 283,
        "logo": "/static/images/ferrari-logo.png",
        "championships": 31,
        "podiums": 842,
        "points": "10000+"
    },
    {
        "id": "redbull",
        "name": "Oracle Red Bull Racing",
        "wins": 130,
        "logo": "/static/images/redbull-logo.png",
        "championships": 6,
        "podiums": 285,
        "points": "8000+"
    },
    {
        "id": "mclaren",
        "name": "McLaren",
        "wins": 203,
        "logo": "/static/images/mclaren-logo.jpg",
        "championships": 10,
        "podiums": 530,
        "points": "7000+"
    },
    {
        "id": "astonmartin",
        "name": "Aston Martin Aramco",
        "wins": 0,
        "logo": "/static/images/astonmartin-logo.jpeg",
        "championships": 0,
        "podiums": 9,
        "points": "500+"
    },
    {
        "id": "alpine",
        "name": "BWT Alpine",
        "wins": 1,
        "logo": "/static/images/alpine-logo.png",
        "championships": 2,
        "podiums": 106,
        "points": "4000+"
    },
    {
        "id": "williams",
        "name": "Williams Racing",
        "wins": 114,
        "logo": "/static/images/williams-logo.jpg",
        "championships": 9,
        "podiums": 313,
        "points": "3800+"
    },
    {
        "id": "haas",
        "name": "MoneyGram Haas F1 Team",
        "wins": 0,
        "logo": "/static/images/haas-logo.jpg",
        "championships": 0,
        "podiums": 0,
        "points": "300+"
    },
    {
        "id": "sauber",
        "name": "Kick Sauber",
        "wins": 1,
        "logo": "/static/images/sauber-logo.png",
        "championships": 0,
        "podiums": 27,
        "points": "800+"
    },
    {
        "id": "racingbulls",
        "name": "Visa Cash App Racing Bulls",
        "wins": 2,
        "logo": "/static/images/racingbulls-logo.jpg",
        "championships": 0,
        "podiums": 5,
        "points": "1000+"
    }
]

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
    return render_template('driver_detail.html', driver=driver)


@app.route('/teams')
def teams_page():
    for t in teams:
        for k, v in t.items():
            if k == "logo":
                t[k] = v
    return render_template('teams.html', logo=v, teams=teams)


@app.route('/teams/<string:team_id>')
def team_detail(team_id):

    team = next((t for t in teams if t["id"] == team_id), None)

    if team:
        return render_template('team_detail.html', team=team)

    return "Team not found", 404


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