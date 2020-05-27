import flask
from flask import request, jsonify
from ics import Calendar
import requests
import datetime as dt
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

USER_CONFIG = {
    'NOAH': {
        'cal_url': 'http://p01-calendars.icloud.com/published/2/R7z0NY0Ja-eATwYdxvL0Cj5_0suPQs9_NokawvmHwpTuh04vObEvNZuL3-mYKubUqej19L4ZXAETnqZqlGuUb0bkBON4r9c7vUIHp7Ba2S0?start_date=2020-03-15',
        'canonical_categories': [
            {
                'name': 'Work',
                'pom_names': [
                    "Build: Generic Forward",
                    "Build: Generic [Forward]",
                    "Day Prep/Planning Forward",
                    "Day Prep/Planning [Forward]",
                    "Meeting Forward",
                    "Meeting: 1:1 Forward",
                    "Meeting: 1:1 [Forward]",
                    "Meeting: Generic Forward",
                    "Meeting: Generic [Forward]",
                    "Telemed ramp up Forward",
                    "Working Forward",
                    "Lunch Personal",
                    "[build] Covid re-assessment Forward"
                ],
                'goal_hrs_week': 50 
            },
            {
                'name': 'Reading',
                'pom_names': [
                    "Read [Personal]",
                    "Reading Articles [Personal]",
                    "Reading [Personal]",
                    "Reading articles Personal",
                    "Reading articles [Personal]",
                    "Reading book Personal"
                ],
                'goal_hrs_week': 5
            }, 
            {
                'name': 'Meditate',
                'pom_names': [
                    "Meditate [Personal]"
                ],
                'goal_hrs_week': 4 
            }, 
            {
                'name': 'Photography',
                'pom_names': [
                    "Photography",
                    "Photography [Personal]"
                ],
                'goal_hrs_week': 2.5
            }, 
            {
                'name': 'Workout',
                'pom_names': [
"Workout [Personal]", "Strength Workout [Personal]"
                ],
                'goal_hrs_week': 3
            }, 
            {
                'name': 'Writing',
                'pom_names': [
"Writing [Personal]"
                ],
                'goal_hrs_week': 2
            }, 
            {
                'name': 'Cycling',
                'pom_names': [
"Cycling Personal", "Cycling [Personal]"
                ],
                'goal_hrs_week': 8
            }, 
            {
                'name': 'Socializing',
                'pom_names': [
                    "Facetime w/ Emily [Personal]",
                    "Hanging out with Friends [Personal]",
                    "Hanging out with roommates [Personal]",
                    "Hanging with Roommates [Personal]",
                    "Hanging with roommates [Personal]",
                    "Call Mom [Personal]",
                    "Catch up with Friends [Personal]",
                    "Messaging Friends [Personal]",
                    "Message Friends [Personal]",
                    "Talking to Family [Personal]"
                ],
                'goal_hrs_week': 10
            },
            {
                'name': 'Side Projects',
                'pom_names': [
                    "Side Project [Personal]",
                    "Side Projects [Personal]",
                    "Side projects Personal",
                    "Side projects [Personal]"
                ],
                'goal_hrs_week': 6
            }, 
            {
                'name': 'Chores and Food',
                'pom_names': [
                    "Chores [Personal]",
                    "Cooking and Cleaning",
                    "Cooking and Eating [Personal]"
                ],
                'goal_hrs_week': 4
            }
        ]
    },
    'EMILY': {
        'cal_url': 'http://p01-calendars.icloud.com/published/2/MTAxNDUyODIyMTEwMTQ1MnFDAoDu9WOTPYC1M363VCgk71g1pKfKKlVbrvDkUxCHNbhp66b2q44js0X1uD3WWiP0osjL-RcA_HE6SYl1_UQ',
        'canonical_categories': [
            {
                'name': 'Work',
                'pom_names': ['Coding [Airbnb]', 'Not-coding [Airbnb]', 'Meeting [Airbnb]'],
                'goal_hrs_week': 40
            },
            {
                'name': 'Journaling',
                'pom_names': ['Journaling [Personal]'],
                'goal_hrs_week': 5
            },
            {
                'name': 'Meditation',
                'pom_names': ['Meditation [Personal] Default Project'],
                'goal_hrs_week': 3
            },
            {
                'name': 'Personal Website',
                'pom_names': ['Website [Personal]', 'Website [Personal] Default Project'],
                'goal_hrs_week': 4
            },
            {
                'name': 'Cycling',
                'pom_names': ['Cycling [Exercise]'],
                'goal_hrs_week': 15
            },
            {
                'name': 'Photo Editing',
                'pom_names': ['Photo editing [Personal]'],
                'goal_hrs_week': 3
            },
            {
                'name': 'Coding Personal Project',
                'pom_names': ['Coding personal project [Personal]'],
                'goal_hrs_week': 5
            },
            {
                'name': 'Drawing',
                'pom_names': ['Art [Personal]'],
                'goal_hrs_week': 5
            },
            {
                'name': 'Handstand Practice',
                'pom_names': ['Core Play [Exercise]', 'Aligned [Exercise]'],
                'goal_hrs_week': 3
            }
        ]
    }
}


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    print('hit api/v1')
    print(request.args)
    if 'id' in request.args:
        id = int(request.args['id'])
        print('id', id)
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

### 
def is_this_month_or_last(d):
    today = dt.date.today()
    first_of_this_month = today.replace(day=1)
    first_of_last_month = (first_of_this_month - dt.timedelta(days=1)).replace(day=1)
    
    if d >= first_of_this_month:
        return 'Current'
    
    if d >= first_of_last_month:
        return 'Previous'
    
    return None


def is_this_week_or_last(d):
    today = dt.date.today()
    first_of_this_week = today - dt.timedelta(days=today.weekday())
    last_of_last_week = first_of_this_week - dt.timedelta(days=1)
    first_of_last_week = last_of_last_week - dt.timedelta(days=last_of_last_week.weekday())
    
    if d >= first_of_this_week:
        return 'Current'
    
    if d >= first_of_last_week:
        return 'Previous'
    
    return None


def get_canonical_category(name, canonical_categories):
    name_res = name
    for cat in canonical_categories:
        for n in cat.get('pom_names', []):
            if name == n:
                name_res = cat.get('name')
    return name_res


def get_canonical_goal(name, canonical_categories):
    for cat in canonical_categories:
        if name == cat.get('name'):
            return cat.get('goal_hrs_week')
    return None


def get_and_parse_calendar_data(user_id):
    cal_route = USER_CONFIG.get(user_id, {}).get('cal_url')
    canonical_categories = USER_CONFIG.get(user_id, {}).get('canonical_categories')
    print('getting cal data')
    raw = requests.get(cal_route).text
    print('parsing cal data')
    c = Calendar(raw.replace('BEGIN:VCALENDAR', 'BEGIN:VCALENDAR\r\nPRODID:noah-rocks'))
    print('done parsing cal data')
    items = []
    for e in list(c.events):
        items.append({
            'name': e.name,
            'begin': str(e.begin),
            'end': str(e.end),
            'duration_min': (e.duration.total_seconds())/60.0,
            'duration_hr': (e.duration.total_seconds())/60.0/60.0
        })

    df = pd.DataFrame(items)
    df['name'] = df['name'].apply(lambda x: get_canonical_category(x, canonical_categories))
    df['begin'] = pd.to_datetime(df.begin)
    df['begin'] = df.begin.apply(lambda x: x.replace(tzinfo=None))
    df['date'] = df.begin.dt.date
    df['end'] = pd.to_datetime(df.end)
    df['end'] = df.begin.apply(lambda x: x.replace(tzinfo=None))
    return df

def get_cumulative_monthly_totals_by_type(df):
    end = dt.datetime.now().date()
    start = end - dt.timedelta(days=90)

    dft = df[
        (df['date'] > start) &\
        (df['date'] <= end)
    ]

    idx = pd.date_range(dft['date'].min(), dft['date'].max())
    dft = dft.groupby(['date', 'name'])['duration_hr'].agg(['sum']).unstack(fill_value=0)
    dft = dft.reindex(idx, fill_value=0)
    dft.columns = dft.columns.get_level_values(1)
    # dft.to_csv('./pom_daily_sums_start={}_end={}.csv'.format(start, end))
    df1 = dft.copy()

    dft = df1.stack().reset_index()
    dft.rename(columns={'level_0': 'date', 0: 'hours'}, inplace=True)
    dft = dft.sort_values(by=['name', 'date'])
    dft['is_current_or_last'] = dft['date'].apply(is_this_month_or_last)
    dft = dft[dft['is_current_or_last'].apply(lambda x: x is not None)].copy()
    dft['cumulative_hours'] = dft.groupby(['name', 'is_current_or_last'])['hours'].cumsum()
    dft['day_indexed'] = dft['date'].dt.day
    return dft.to_dict(orient='records')


def get_cumulative_weekly_totals_by_type(df):
    end = dt.datetime.now().date()
    start = end - dt.timedelta(days=90)

    dft = df[
        (df['date'] > start) &\
        (df['date'] <= end)
    ]

    idx = pd.date_range(dft['date'].min(), dft['date'].max())
    dft = dft.groupby(['date', 'name'])['duration_hr'].agg(['sum']).unstack(fill_value=0)
    dft = dft.reindex(idx, fill_value=0)
    dft.columns = dft.columns.get_level_values(1)
    # dft.to_csv('./pom_daily_sums_start={}_end={}.csv'.format(start, end))
    df1 = dft.copy()

    dft = df1.stack().reset_index()
    dft.rename(columns={'level_0': 'date', 0: 'hours'}, inplace=True)
    dft = dft.sort_values(by=['name', 'date'])
    dft['is_current_or_last'] = dft['date'].apply(is_this_week_or_last)
    dft = dft[dft['is_current_or_last'].apply(lambda x: x is not None)].copy()
    dft['cumulative_hours'] = dft.groupby(['name', 'is_current_or_last'])['hours'].cumsum()
    dft['day_indexed'] = dft['date'].dt.weekday
    return dft.to_dict(orient='records')


@app.route('/api/v1/getcal', methods=['GET'])
def get_cal():
    if 'user_id' in request.args:
        user_id = request.args['user_id']
        print('user_id', user_id)
        if user_id not in USER_CONFIG:
            return {'error': 'Error: Unknown User'}
    else:
        return {'error': 'Error: Please provide user_id'}

    df = get_and_parse_calendar_data(user_id)
    res = {
        'sparkline_user_data': {
            'monthly': get_cumulative_monthly_totals_by_type(df),
            'weekly': get_cumulative_weekly_totals_by_type(df)
        },
        'categories': USER_CONFIG.get(user_id, {}).get('canonical_categories')
    }

    return jsonify(res)


app.run()