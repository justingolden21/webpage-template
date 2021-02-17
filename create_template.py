import os, datetime

def create_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

project_name = input('project name:\n')
project_description = input('project description:\n')
project_dev_name = project_name.lower().replace(' ', '-')
print('Creating Files...')

data = {
	'project_name': project_name,
	'project_description': project_description,
	'project_dev_name': project_dev_name,
	'project_author': 'Justin Golden',
	'homepage': 'https://justingolden.me',
	'github': 'justingolden21',
	'email': 'contact@justingolden.me',
	'year': str(datetime.datetime.now().year)
}

readme_text = """# %(project_name)s

### About

%(project_description)s

### Links

- Live demo: %(homepage)s/%(project_dev_name)s

- This repo: https://github.com/%(github)s/%(project_dev_name)s

<hr>

- My website: %(homepage)s

- My repos: https://github.com/%(github)s

- Contact me: %(email)s"""

license_text = """MIT License

Copyright (c) %(year)s %(project_author)s

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

gitattributes_text = """# Auto detect text files and perform LF normalization
* text=auto"""

gitignore_text = """
"""

localhost_text = """ECHO OFF
ECHO Starting server in current directory to port 8000

start chrome --new-tab "http://localhost:8000/"
py -m http.server
PAUSE"""

css_text = """::-moz-selection {
	background: #e6e6e6;
}
::selection {
	background: #e6e6e6;
}

* {
	font-family: system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji';
}

body {
	margin: 1rem;
}
h1 {
	text-align: center;
	font-weight: lighter;
	letter-spacing: 0.1rem;
}

@media (min-width: 640px) { /* sm */
}

@media (min-width: 768px) { /* md */
}

@media (min-width: 1024px) { /* lg */
}

@media (min-width: 1280px) { /* xl */
}"""

js_text = """window.onload = ()=> {
	console.log('page loaded');
};"""

html_text = """<!DOCTYPE html>
<html lang="en">
<head>
	<title>%(project_name)s</title>
	<meta charset="utf-8">
	<meta name="title=" content="%(project_name)s">
	<meta name="robots" content="index, follow">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="%(project_description)s">
	<meta name="keywords" content="">
	<!-- <link rel="shortcut icon" href="img/icon.png"> -->

	<link rel="stylesheet" href="css/styles.css">
	<script src="js/scripts.js"></script>
</head>
<body>
	<h1>%(project_name)s</h1>
</body>
</html>"""

files_to_create = {
	'README.md': readme_text%data,
	'LICENSE': license_text%data,
	'.gitattributes': gitattributes_text,
	'.gitignore': gitignore_text,
	'localhost.bat': localhost_text,
	'index.html': html_text%data,
}

folder_name = project_dev_name

create_dir(folder_name)

for key in files_to_create:
	with open(folder_name + '/' + key, 'x') as f:
		f.write(files_to_create[key])

create_dir(folder_name + '/css')
create_dir(folder_name + '/js')
create_dir(folder_name + '/img')

with open(folder_name + '/css/styles.css', 'x') as f:
	f.write(css_text)
with open(folder_name + '/js/scripts.js', 'x') as f:
	f.write(js_text)

input('Press any key to continue . . .')
