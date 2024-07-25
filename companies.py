from flask import Flask, request, render_template_string, send_file
from bs4 import BeautifulSoup
import tempfile
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>HTML Data Extractor and Link Generator</title>
    <style>
      body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        font-family: 'Arial', sans-serif;
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        color: #333;
      }
      .container {
        text-align: center;
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }
      h1 {
        font-family: 'Helvetica', sans-serif;
        color: #444;
      }
      textarea {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        margin-bottom: 10px;
      }
      input[type="submit"], button {
        background: #ff7e5f;
        border: none;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin: 5px;
      }
      input[type="submit"]:hover, button:hover {
        background: #feb47b;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>HTML Data Extractor and Link Generator</h1>
      <form method="POST" action="/" enctype="multipart/form-data">
        <textarea name="html_content" rows="20" placeholder="Paste your HTML code here"></textarea><br>
        <input type="submit" value="Extract and Generate Links">
      </form>
    </div>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
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
                    name = parts[0].strip('/')
                    number = parts[1].strip('/') if len(parts) > 1 else ''
                    extracted_data.append({"name": name, "number": number})

            links = [f"https://targetare.ro/{item['number']}/{item['name']}" for item in extracted_data]

            # Save the links to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt')
            for link in links:
                temp_file.write(link + '\n')
            temp_file.close()

            return send_file(temp_file.name, as_attachment=True, download_name='links.txt', mimetype='text/plain')

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
