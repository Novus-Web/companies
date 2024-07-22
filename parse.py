# file: app.py
from flask import Flask, request, render_template_string
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

html_template = """
<!doctype html>
<html lang="en">
  <head>
    <title>HTML Data Extractor</title>
  </head>
  <body>
    <h1>Paste your HTML code here</h1>
    <form method="POST" action="/">
      <textarea name="html_content" rows="20" cols="100"></textarea><br>
      <input type="submit" value="Extract Data-Href">
    </form>
    {% if data %}
    <h2>Extracted Data</h2>
    <pre>{{ data }}</pre>
    {% endif %}
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        html_content = request.form['html_content']
        soup = BeautifulSoup(html_content, 'html.parser')
        tbody = soup.find('tbody')
        extracted_data = []

        if tbody:
            for row in tbody.find_all('tr'):
                td = row.find('td', class_='clickable-row')
                if td and 'data-href' in td.attrs:
                    data_href = td['data-href']
                    parts = data_href.rsplit('-', 1)
                    name = parts[0]
                    number = parts[1] if len(parts) > 1 else ''
                    extracted_data.append({"name": name, "number": number})

            data = json.dumps(extracted_data, indent=2)
        else:
            data = "No <tbody> element found in the provided HTML."

    return render_template_string(html_template, data=data)

if __name__ == '__main__':
    app.run(debug=True)
