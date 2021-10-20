#   Copyright (C) 2021 Hemant Sachdeva <hemant.evolver@gmail.com>

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import requests

try:
    from flask import Flask, request, render_template
except ImportError:
    sys.exit("[!] Flask module not found. Install it by 'pip3 install flask'")

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        joke_category = request.form.getlist('catagory')
        # set joke category to Any if no category chosen, make ',' separated string otherwise
        joke_category = 'Any' if len(joke_category) == 0 else ','.join(joke_category)
        url = "https://v2.jokeapi.dev/joke/{}".format(joke_category)

        blacklist_joke = request.form.getlist('flag')
        if len(blacklist_joke) != 0:
            # making flag list a ',' separated string if multiple blacklists chosen
            blacklist_joke = ','.join(blacklist_joke)
            url += '?blacklistFlags={}'.format(blacklist_joke)
        resp = requests.get(url)
        data = resp.json()
        if data.get('type') == 'single':
            joke = data.get('joke')
            return render_template('index.html', showJoke=joke)
        else:
            joke = data.get('setup') + "\n\n" + data.get('delivery')
            return render_template('index.html', showJoke=joke)
    else:
        return render_template('index.html')
