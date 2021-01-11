import os, datetime, subprocess, shutil

def create_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

project_name = input('project name:\n')
project_description = input('project description:\n')
project_dev_name = project_name.lower().replace(' ', '-')
project_keywords = input('project keywords (separate by commas):\n')
project_keywords_list = str([s.strip(' ') for s in project_keywords.split(',')] ).replace('\'','"') # double quotes for json
project_color = input('project color:\n')
if(project_color == ''):
	project_color = '#FFFFFF'
print('Creating Files...')

data = {
	'project_name': project_name,
	'project_description': project_description,
	'project_dev_name': project_dev_name,
				'project_keywords': project_keywords,
				'project_keywords_list': project_keywords_list,
				'project_color': project_color,
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

Localhost: run `localhost.bat` if you have Python3 installed

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

gitignore_text = """node_modules/
dist/css/"""

package_text = """{
	"name": "%(project_dev_name)s",
	"version": "1.0.0",
	"description": "%(project_description)s",
	"scripts": {
		"dev-no-watch": "postcss src/styles.css -o dist/css/styles.css",
		"dev": "postcss src/styles.css -o dist/css/styles.css --watch",
		"build": "cross-env NODE_ENV=production postcss src/styles.css -o dist/css/styles.css && cleancss -o dist/css/styles.css dist/css/styles.css"
	},
	"keywords": %(project_keywords_list)s,
	"author": "%(project_author)s",
	"license": "MIT",
	"dependencies": {
		"autoprefixer": "^10.1.0",
		"clean-css-cli": "^4.3.0",
		"cross-env": "^7.0.3",
		"postcss-cli": "^8.3.1",
		"tailwindcss": "^2.0.2"
	}
}"""

tailwind_config_text = """module.exports = {
	purge: [
		'./dist/**/*.html',
		'./dist/**/*.js'
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
		require('tailwindcss'),
		require('autoprefixer')
	]
};"""

manifest_json_text = """{
	"name": "%(project_name)s",
	"short_name": "%(project_name)s",
	"description": "%(project_description)s",
	"start_url": "index.html",
	"display": "standalone",
	"background_color": "%(project_color)s",
	"theme_color": "%(project_color)s",
	"orientation": "portrait-primary",
	"icons": [
		{
			"src": "/img/icons/icon-48x48.png",
			"type": "image/png",
			"sizes": "48x48"
		},
		{
			"src": "/img/icons/icon-72x72.png",
			"type": "image/png",
			"sizes": "72x72"
		},
		{
			"src": "/img/icons/icon-96x96.png",
			"type": "image/png",
			"sizes": "96x96"
		},
		{
			"src": "/img/icons/icon-144x144.png",
			"type": "image/png",
			"sizes": "144x144"
		},
		{
			"src": "/img/icons/icon-192x192.png",
			"type": "image/png",
			"sizes": "192x192"
		},
		{
			"src": "/img/icons/icon-512x512.png",
			"type": "image/png",
			"sizes": "512x512"
		}
	]
}"""

src_styles_text = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
	::-moz-selection {
		@apply bg-gray-100;
	}
	::selection {
		@apply bg-gray-100;
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

dist_js_text = """if('serviceWorker' in navigator){
	navigator.serviceWorker.register('/sw.js')
		.then(reg => console.log('service worker registered'))
		.catch(err => console.log('service worker not registered', err));
}"""

service_worker_js_text = """const staticCacheName = 'site-static-v1';
const dynamicCacheName = 'site-dynamic-v1';
const assets = [
	'/',
	'/index.html',
	'/404.html',
	'/pages/fallback.html',
	'/js/scripts.js',
	'/css/styles.css',
	'/img/icons/icon-96x96.png',
];

// cache size limit function
const limitCacheSize = (name, size) => {
	caches.open(name).then(cache => {
		cache.keys().then(keys => {
			if(keys.length > size){
				cache.delete(keys[0]).then(limitCacheSize(name, size));
			}
		});
	});
};

// install event
self.addEventListener('install', evt => {
	//console.log('service worker installed');
	evt.waitUntil(
		caches.open(staticCacheName).then((cache) => {
			console.log('caching shell assets');
			cache.addAll(assets);
		})
	);
});

// activate event
self.addEventListener('activate', evt => {
	//console.log('service worker activated');
	evt.waitUntil(
		caches.keys().then(keys => {
			//console.log(keys);
			return Promise.all(keys
				.filter(key => key !== staticCacheName && key !== dynamicCacheName)
				.map(key => caches.delete(key))
			);
		})
	);
});

// fetch event
self.addEventListener('fetch', evt => {
	//console.log('fetch event', evt);
	evt.respondWith(
		caches.match(evt.request).then(cacheRes => {
			return cacheRes || fetch(evt.request).then(fetchRes => {
				return caches.open(dynamicCacheName).then(cache => {
					cache.put(evt.request.url, fetchRes.clone());
					// check cached items size
					limitCacheSize(dynamicCacheName, 100);
					return fetchRes;
				})
			});
		}).catch(() => {
			if(evt.request.url.indexOf('.html') > -1){
				return caches.match('/pages/fallback.html');
			} 
		})
	);
});"""

index_html_text = """<!DOCTYPE html>
<html lang="en">
<head>
	<title>%(project_name)s</title>
	<meta charset="utf-8">
	<meta name="title=" content="%(project_name)s">
	<meta name="robots" content="index, follow">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="%(project_description)s">
	<meta name="keywords" content="%(project_keywords)s">
	<link rel="shortcut icon" href="/img/icons/icon-96x96.png">
	<link rel="manifest" href="/manifest.json">
	<link rel="apple-touch-icon" href="/img/icons/icon-96x96.png">
	<meta name="apple-mobile-web-app-status-bar" content="%(project_color)s">
	<meta name="theme-color" content="%(project_color)s">

	<link rel="stylesheet" href="css/styles.css">
	<script src="js/scripts.js"></script>
</head>
<body class="text-center m-2 text-gray-900">
	<section>
		<h1>%(project_name)s</h1>
	</section>
</body>
</html>"""

fallback_html_text = """<!DOCTYPE html>
<html lang="en">
<head>
	<title>%(project_name)s</title>
	<meta charset="utf-8">
	<meta name="title=" content="%(project_name)s">
	<meta name="robots" content="index, follow">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="%(project_description)s">
	<meta name="keywords" content="%(project_keywords)s">
	<link rel="shortcut icon" href="/img/icons/icon-96x96.png">
	<link rel="manifest" href="/manifest.json">
	<link rel="apple-touch-icon" href="/img/icons/icon-96x96.png">
	<meta name="apple-mobile-web-app-status-bar" content="%(project_color)s">
	<meta name="theme-color" content="%(project_color)s">

	<link rel="stylesheet" href="css/styles.css">
	<script src="js/scripts.js"></script>
</head>
<body class="text-center m-2 text-gray-900">
	<section>
		<h1>%(project_name)s</h1>
		<div>
			<h3>Oops!</h3>
			<p>Currently you can't view this page without a connection.</p>
			<a href="/">Go back to the homepage</a>
		</div>
	</section>
</body>
</html>"""

html_404_text = """<!DOCTYPE html>
<html lang="en">
<head>
	<title>%(project_name)s</title>
	<meta charset="utf-8">
	<meta name="title=" content="%(project_name)s">
	<meta name="robots" content="index, follow">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="%(project_description)s">
	<meta name="keywords" content="%(project_keywords)s">
	<link rel="shortcut icon" href="/img/icons/icon-96x96.png">
	<link rel="manifest" href="/manifest.json">
	<link rel="apple-touch-icon" href="/img/icons/icon-96x96.png">
	<meta name="apple-mobile-web-app-status-bar" content="%(project_color)s">
	<meta name="theme-color" content="%(project_color)s">

	<link rel="stylesheet" href="css/styles.css">
	<script src="js/scripts.js"></script>
</head>
<body class="text-center m-2 text-gray-900">
	<section>
		<h1>%(project_name)s</h1>
		<div>
			<h3>404 Page Not Found</h3>
			<p>The specified file was not found on this website. Please check the URL for mistakes and try again.</p>
			<a href="/">Go back to the homepage</a>
		</div>
	</section>
</body>
</html>"""

deploy_to_docs_py = """import os, shutil

def recursive_copy(src, dest):
	for item in os.listdir(src):
		file_path = os.path.join(src, item)

		if os.path.isfile(file_path):
			shutil.copy(file_path, dest)

		elif os.path.isdir(file_path):
			new_dest = os.path.join(dest, item)
			os.mkdir(new_dest)
			recursive_copy(file_path, new_dest)

if os.path.exists('docs/'):
	shutil.rmtree('docs/')
os.makedirs('docs/')
recursive_copy('dist/', 'docs/')
input('Done.')"""

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
	'localhost.bat': 'ECHO OFF\nECHO Starting server in current directory to port 8000\n\ncd dist\nstart chrome --new-tab "http://localhost:8000/"\npy -m http.server\nPAUSE',
	'deploy_to_doc.py': deploy_to_docs_py,
}

folder_name = project_dev_name

create_dir(folder_name)

for key in files_to_create:
	with open(folder_name + '/' + key, 'x') as f:
		f.write(files_to_create[key])

create_dir(folder_name + '/src')
create_dir(folder_name + '/dist')
create_dir(folder_name + '/dist/css')
create_dir(folder_name + '/dist/img')
create_dir(folder_name + '/dist/img/icons')
create_dir(folder_name + '/dist/js')
create_dir(folder_name + '/dist/pages')

with open(folder_name + '/src/styles.css', 'x') as f:
	f.write(src_styles_text)
with open(folder_name + '/dist/js/scripts.js', 'x') as f:
	f.write(dist_js_text)
with open(folder_name + '/dist/sw.js', 'x') as f:
	f.write(service_worker_js_text%data)
with open(folder_name + '/dist/manifest.json', 'x') as f:
	f.write(manifest_json_text%data)
with open(folder_name + '/dist/index.html', 'x') as f:
	f.write(index_html_text%data)
with open(folder_name + '/dist/404.html', 'x') as f:
	f.write(html_404_text%data)
with open(folder_name + '/dist/pages/fallback.html', 'x') as f:
	f.write(fallback_html_text%data)

# copy icons
src_files = os.listdir('icons/')
for file_name in src_files:
	full_file_name = os.path.join('icons/', file_name)
	if os.path.isfile(full_file_name):
		shutil.copy(full_file_name, folder_name + '/dist/img/icons/')

input('Press any key to continue . . .')

print('Installing Packages...')

# npm install
dir_path = os.path.dirname(os.path.realpath(__file__) ) # directory containing this script
dir_path += '/' + folder_name
os.chdir(dir_path)
subprocess.check_call('npm install', shell=True)

input('Press any key to continue . . .')
print('Building CSS for the first time')

# build css first time
subprocess.check_call('npm run dev-no-watch', shell=True)

print('Setup finished. Run localhost.bat and dev.bat to begin working. Ctrl+Shift+R to hard reload the webpage if cached from another project.')
input('Press any key to continue . . .')
