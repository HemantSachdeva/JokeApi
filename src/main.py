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
        cat = request.form.getlist('catagory')
        cat = ','.join(cat)  # making cat list a ',' separated string
        flag = request.form.getlist('flag')
        flag = ','.join(flag)  # making flag list a ',' separated string
        url = "https://v2.jokeapi.dev/joke/{}?blacklistFlags={}".format(
            cat, flag)
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
