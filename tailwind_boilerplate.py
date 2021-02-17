import os, datetime, subprocess, webbrowser

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

### Development

First time setup: `npm install`

Development: `npm run dev`

Production: `npm run build`

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

gitignore_text = """node_modules/"""

package_text = """{
  "name": "%(project_dev_name)s",
  "version": "1.0.0",
  "description": "%(project_description)s",
  "scripts": {
    "dev": "postcss src/styles.css -o docs/css/styles.css --watch",
    "build": "cross-env NODE_ENV=production postcss src/styles.css -o docs/css/styles.css && cleancss -o docs/css/styles.css docs/css/styles.css"
  },
  "keywords": [],
  "author": "%(project_author)s",
  "license": "MIT",
  "devDependencies": {
    "autoprefixer": "^10.1.0",
    "clean-css-cli": "^4.3.0",
    "cross-env": "^7.0.3",
    "postcss-cli": "^8.3.1",
    "postcss-import": "^14.0.0",
    "tailwindcss": "^2.0.2"
  }
}"""

tailwind_config_text = """module.exports = {
  purge: [
    './docs/**/*.html',
    './docs/**/*.js'
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}"""

postcss_config_text = """module.exports = {
  plugins: [
    require('postcss-import'),
    require('tailwindcss'),
    require('autoprefixer')
  ]
};"""

src_styles_text = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
	::-moz-selection {
		@apply bg-indigo-100;
	}
	::selection {
		@apply bg-indigo-100;
	}
	*:focus, button:focus {
		@apply outline-none ring-2 ring-indigo-300;
	}

	h1 {
		@apply text-2xl font-light;
	}
	h2 {
		@apply text-xl font-medium;
	}
	p {
		@apply leading-relaxed;
	}
}

@layer components {

}

@media (min-width: 640px) { /* sm */
}

@media (min-width: 768px) { /* md */
}

@media (min-width: 1024px) { /* lg */
}

@media (min-width: 1280px) { /* xl */
}"""

js_text = """window.onload = ()=> console.log('page loaded');"""

index_html_text = """<!DOCTYPE html>
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
<body class="text-center m-2 text-gray-900">
	<section>
		<h1>%(project_name)s</h1>
	</section>
</body>
</html>"""

files_to_create = {
	'README.md': readme_text%data,
	'LICENSE': license_text%data,
	'.gitattributes': gitattributes_text,
	'.gitignore': gitignore_text,
	'package.json': package_text%data,
	'tailwind.config.js': tailwind_config_text,
	'postcss.config.js': postcss_config_text,
	'dev.bat': 'call npm run dev\nPAUSE',
	'prod.bat': 'call npm run build\nPAUSE',
}

folder_name = project_dev_name

create_dir(folder_name)

for key in files_to_create:
	with open(folder_name + '/' + key, 'x') as f:
		f.write(files_to_create[key])

create_dir(folder_name + '/src')
create_dir(folder_name + '/docs')
create_dir(folder_name + '/docs/css')
create_dir(folder_name + '/docs/img')
create_dir(folder_name + '/docs/js')

with open(folder_name + '/src/styles.css', 'x') as f:
	f.write(src_styles_text)
with open(folder_name + '/docs/js/scripts.js', 'x') as f:
	f.write(js_text)
with open(folder_name + '/docs/index.html', 'x') as f:
	f.write(index_html_text%data)

input('Press any key to continue . . .')
print('Installing Packages...')

# npm install
dir_path = os.path.dirname(os.path.realpath(__file__) ) # directory containing this script
dir_path += '/' + folder_name
os.chdir(dir_path)
subprocess.check_call('npm install', shell=True)

input('Setup complete. Press any key to continue . . .')
