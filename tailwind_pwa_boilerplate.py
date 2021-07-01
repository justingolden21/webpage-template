
# todo: minify html and js
# have them start in src and copied to dist
# check file links after moving files
# copy script:
# const fs = require('fs-extra')
# fs.copySync('assets/', 'dist/assets')

# todo: test in depth
# deploy on netlify, install pwa on multiple devices
# check all tailwind styles applied (inline classes, stylesheets, imports)
# check file sizes, performance, lighthouse

import os, datetime, subprocess, shutil

def create_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

project_name = input('project name:\n')
project_description = input('project description:\n')
project_dev_name = project_name.lower().replace(' ', '-')
project_keywords = input('project keywords (separate by commas):\n')
project_keywords_list = str([s.strip(' ') for s in project_keywords.split(',')] ).replace('\'','"') # double quotes for json
project_color = input('project color (default #FFF):\n')
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

First time setup: `npm i`

Generate Assets: `npm run generate-assets` with icon.svg saved under /src/img

Development: `npm run dev`

Production: `npm run prod`

Serve: `npm run serve`

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
"""

netlify_text = """[build]
	publish = "dist/"
	command = "npm run prod"
"""

imgbot_config = """{
	"schedule": "daily",
	"ignoredFiles": [
		"src/img/icon.svg"
	],
	"minKBReduced": 10
}"""

increment_py = """import re
with open('dist/sw.js', 'r+') as f:
	lines = f.readlines()

	arr = lines[1].split('-')
	v_num = re.sub('[^0-9]', '', arr[2])
	v_num = str(int(v_num) + 1)
	arr[2] = 'v' + v_num + '\\';\\n'
	lines[1] = '-'.join(arr)

	f.seek(0)
	f.writelines(lines)

	print('Incremented to v' + v_num)"""

eslint_text = """{
	"env": {
		"browser": true,
		"es2021": true
	},
	"extends": [
		"airbnb-base"
	],
	"parserOptions": {
		"ecmaVersion": 12,
		"sourceType": "module"
	},
	"rules": {
		"indent": [
			"warn",
			"tab"
		],
		"quotes": [
			"warn",
			"single"
		],
		"no-unused-vars": "warn",
		"no-console": "off",
		"no-tabs": "off",
		"func-names": "off"
	}
}"""

package_text = """{
	"name": "%(project_dev_name)s",
	"version": "1.0.0",
	"description": "%(project_description)s",
	"scripts": {
		"dev": "postcss src/styles.css -o dist/css/styles.css --watch",
		"build": "cross-env NODE_ENV=production postcss src/styles.css -o dist/css/styles.css && cleancss -o dist/css/styles.css dist/css/styles.css",
		"prod": "npm run build && ( py -V && py increment.py ) || ( python3 -V && python3 increment.py )",
		"lint": "eslint dist/js/ --ext .js --ignore-pattern \\"dist/js/lib/*\\"",
		"serve": "live-server --open=dist",
		"dev-serve": "concurrently --kill-others \\"npm run dev\\" \\"npm run serve\\"",
		"generate-assets": "pwa-asset-generator src/img/icon.svg dist/img/icons --manifest dist/manifest.webmanifest --index dist/index.html --favicon --mstile --icon-only"
	},
	"keywords": %(project_keywords_list)s,
	"author": "%(project_author)s",
	"license": "MIT",
	"devDependencies": {
		"autoprefixer": "^10.1.0",
		"clean-css-cli": "^4.3.0",
		"concurrently": "^5.3.0",
		"cross-env": "^7.0.3",
		"eslint": "^7.29.0",
		"eslint-config-airbnb-base": "^14.2.1",
		"eslint-plugin-import": "^2.23.4",
		"live-server": "^1.2.1",
		"postcss-cli": "^8.3.1",
		"postcss-import": "^14.0.2",
		"pwa-asset-generator": "^4.1.1",
		"tailwindcss": "^2.0.2"
	}
}"""

tailwind_config_text = """module.exports = {
	mode: 'jit',
	purge: [
		'./dist/**/*.html'
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
			"src": "img/icons/manifest-icon-192.png",
			"sizes": "192x192",
			"type": "image/png",
			"purpose": "maskable any"
		},
		{
			"src": "img/icons/manifest-icon-512.png",
			"sizes": "512x512",
			"type": "image/png",
			"purpose": "maskable any"
		}
	]
}"""

src_styles_text = """@import "./components/button.css";

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
	::-moz-selection {
		@apply bg-gray-100;
	}
	::selection {
		@apply bg-gray-100;
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

src_btn_styles = """.btn {
	@apply border-2 border-gray-100 text-gray-700 rounded p-2 cursor-pointer hover:bg-gray-700 hover:text-white;
}"""

icon_svg = """<svg class="w-6 h-6" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" rx="4" fill="#FFF"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>"""

dist_js_text = """if('serviceWorker' in navigator){
	navigator.serviceWorker.register('sw.js')
		.then(reg => console.log('service worker registered'))
		.catch(err => console.log('service worker not registered', err));
}

window.addEventListener('load', () => {
	u('.btn').on('click', () => console.log('clicked') );
});
"""

service_worker_js_text = """const staticCacheName = 'site-static-v1';
const dynamicCacheName = 'site-dynamic-v1';
const assets = [
	'/',
	'/index.html',
	'/404.html',
	'/pages/fallback.html',
	'/js/scripts.js',
	'/css/styles.css',
	'/img/icons/manifest-icon-192.png',
	'/img/icons/manifest-icon-512.png',
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
	<link rel="shortcut icon" href="img/icons/manifest-icon-192.png">
	<link rel="manifest" href="manifest.webmanifest">
	<link rel="apple-touch-icon" href="/img/icons/manifest-icon-192.png">
	<meta name="apple-mobile-web-app-status-bar" content="%(project_color)s">
	<meta name="theme-color" content="%(project_color)s">

	<link rel="stylesheet" href="css/styles.css">
	<script src="js/scripts.js"></script>
	<script src="js/lib/umbrella.min.js"></script>
</head>
<body class="text-center m-2 text-gray-900">
	<section>
		<h1>%(project_name)s</h1>
		<button class="btn">Hello</button>
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
	<link rel="shortcut icon" href="../img/icons/manifest-icon-192.png">
	<link rel="manifest" href="../manifest.webmanifest">
	<link rel="apple-touch-icon" href="../img/icons/manifest-icon-192.png">
	<meta name="apple-mobile-web-app-status-bar" content="%(project_color)s">
	<meta name="theme-color" content="%(project_color)s">

	<link rel="stylesheet" href="../css/styles.css">
	<script src="../js/scripts.js"></script>
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
	<link rel="shortcut icon" href="img/icons/manifest-icon-192.png">
	<link rel="manifest" href="manifest.webmanifest">
	<link rel="apple-touch-icon" href="/img/icons/manifest-icon-192.png">
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

umbrella_js = """/* Umbrella JS 3.2.3 umbrellajs.com */
/* Fork: https://github.com/justingolden21/umbrella */
var u=function(t,e){return this instanceof u?t instanceof u?t:("string"==typeof t&&(t=this.select(t,e)),t&&t.nodeName&&(t=[t]),void(this.nodes=this.slice(t))):new u(t,e)};u.prototype={get length(){return this.nodes.length}},u.prototype.nodes=[],u.prototype.addClass=function(){return this.eacharg(arguments,function(t,e){t.classList.add(e)})},u.prototype.adjacent=function(i,t,n){return"number"==typeof t&&(t=0===t?[]:new Array(t).join().split(",").map(Number.call,Number)),this.each(function(r,o){var e=document.createDocumentFragment();u(t||{}).map(function(t,e){var n="function"==typeof i?i.call(this,t,e,r,o):i;return"string"==typeof n?this.generate(n):u(n)}).each(function(t){this.isInPage(t)?e.appendChild(u(t).clone().first()):e.appendChild(t)}),n.call(this,r,e)})},u.prototype.after=function(t,e){return this.adjacent(t,e,function(t,e){t.parentNode.insertBefore(e,t.nextSibling)})},u.prototype.append=function(t,e){return this.adjacent(t,e,function(t,e){t.appendChild(e)})},u.prototype.args=function(t,e,n){return"function"==typeof t&&(t=t(e,n)),"string"!=typeof t&&(t=this.slice(t).map(this.str(e,n))),t.toString().split(/[\\s,]+/).filter(function(t){return t.length})},u.prototype.array=function(o){o=o;var i=this;return this.nodes.reduce(function(t,e,n){var r;return o?((r=o.call(i,e,n))||(r=!1),"string"==typeof r&&(r=u(r)),r instanceof u&&(r=r.nodes)):r=e.innerHTML,t.concat(!1!==r?r:[])},[])},u.prototype.attr=function(t,e,r){return r=r?"data-":"",this.pairs(t,e,function(t,e){return t.getAttribute(r+e)},function(t,e,n){t.setAttribute(r+e,n)})},u.prototype.before=function(t,e){return this.adjacent(t,e,function(t,e){t.parentNode.insertBefore(e,t)})},u.prototype.children=function(t){return this.map(function(t){return this.slice(t.children)}).filter(t)},u.prototype.clone=function(){return this.map(function(t,e){var n=t.cloneNode(!0),r=this.getAll(n);return this.getAll(t).each(function(t,e){for(var n in this.mirror)this.mirror[n]&&this.mirror[n](t,r.nodes[e])}),n})},u.prototype.getAll=function(t){return u([t].concat(u("*",t).nodes))},u.prototype.mirror={},u.prototype.mirror.events=function(t,e){if(t._e)for(var n in t._e)t._e[n].forEach(function(t){u(e).on(n,t.callback)})},u.prototype.mirror.select=function(t,e){u(t).is("select")&&(e.value=t.value)},u.prototype.mirror.textarea=function(t,e){u(t).is("textarea")&&(e.value=t.value)},u.prototype.closest=function(e){return this.map(function(t){do{if(u(t).is(e))return t}while((t=t.parentNode)&&t!==document)})},u.prototype.css=function(e,n){if("object"!=typeof e)return e=e.replace(/-([a-z])/g,function(t){return t[1].toUpperCase()}),void 0===n?this.first().style[e]:("number"==typeof n&&(n+="px"),this.each(function(t){t.style[e]=n}));for(var t in e)e.hasOwnProperty(t)&&this.css(t,e[t]);return this},u.prototype.data=function(t,e){return this.attr(t,e,!0)},u.prototype.each=function(t){return this.nodes.forEach(t.bind(this)),this},u.prototype.eacharg=function(n,r){return this.each(function(e,t){this.args(n,e,t).forEach(function(t){r.call(this,e,t)},this)})},u.prototype.empty=function(){return this.each(function(t){for(;t.firstChild;)t.removeChild(t.firstChild)})},u.prototype.filter=function(e){var t=function(t){return t.matches=t.matches||t.msMatchesSelector||t.webkitMatchesSelector,t.matches(e||"*")};return"function"==typeof e&&(t=e),e instanceof u&&(t=function(t){return-1!==e.nodes.indexOf(t)}),u(this.nodes.filter(t))},u.prototype.find=function(e){return this.map(function(t){return u(e||"*",t)})},u.prototype.first=function(){return this.nodes[0]||!1},u.prototype.generate=function(t){return/^\\s*<tr[> ]/.test(t)?u(document.createElement("table")).html(t).children().children().nodes:/^\\s*<t(h|d)[> ]/.test(t)?u(document.createElement("table")).html(t).children().children().children().nodes:/^\\s*</.test(t)?u(document.createElement("div")).html(t).children().nodes:document.createTextNode(t)},u.prototype.handle=function(){var t=this.slice(arguments).map(function(e){return"function"==typeof e?function(t){t.preventDefault(),e.apply(this,arguments)}:e},this);return this.on.apply(this,t)},u.prototype.hasClass=function(){return this.is("."+this.args(arguments).join("."))},u.prototype.html=function(e){return void 0===e?this.first().innerHTML||"":this.each(function(t){t.innerHTML=e})},u.prototype.is=function(t){return 0<this.filter(t).length},u.prototype.isInPage=function(t){return t!==document.body&&document.body.contains(t)},u.prototype.last=function(){return this.nodes[this.length-1]||!1},u.prototype.map=function(t){return t?u(this.array(t)).unique():this},u.prototype.not=function(e){return this.filter(function(t){return!u(t).is(e||!0)})},u.prototype.off=function(t,e,n){var r=null==e&&null==n,o=null,i=e;return"string"==typeof e&&(o=e,i=n),this.eacharg(t,function(e,n){u(e._e?e._e[n]:[]).each(function(t){(r||t.orig_callback===i&&t.selector===o)&&e.removeEventListener(n,t.callback)})})},u.prototype.on=function(t,e,o){var i=null,n=e;"string"==typeof e&&(i=e,n=o,e=function(e){var n=arguments,r=!1;u(e.currentTarget).find(i).each(function(t){if(t===e.target||t.contains(e.target)){r=!0;try{Object.defineProperty(e,"currentTarget",{get:function(){return t}})}catch(t){}o.apply(t,n)}}),r||e.currentTarget!==e.target||o.apply(e.target,n)});var r=function(t){return e.apply(this,[t].concat(t.detail||[]))};return this.eacharg(t,function(t,e){t.addEventListener(e,r),t._e=t._e||{},t._e[e]=t._e[e]||[],t._e[e].push({callback:r,orig_callback:n,selector:i})})},u.prototype.pairs=function(n,t,e,r){if(void 0!==t){var o=n;(n={})[o]=t}return"object"==typeof n?this.each(function(t){for(var e in n)r(t,e,n[e])}):this.length?e(this.first(),n):""},u.prototype.param=function(e){return Object.keys(e).map(function(t){return this.uri(t)+"="+this.uri(e[t])}.bind(this)).join("&")},u.prototype.parent=function(t){return this.map(function(t){return t.parentNode}).filter(t)},u.prototype.prepend=function(t,e){return this.adjacent(t,e,function(t,e){t.insertBefore(e,t.firstChild)})},u.prototype.remove=function(){return this.each(function(t){t.parentNode&&t.parentNode.removeChild(t)})},u.prototype.removeClass=function(){return this.eacharg(arguments,function(t,e){t.classList.remove(e)})},u.prototype.replace=function(t,e){var n=[];return this.adjacent(t,e,function(t,e){n=n.concat(this.slice(e.children)),t.parentNode.replaceChild(e,t)}),u(n)},u.prototype.scroll=function(){return this.first().scrollIntoView({behavior:"smooth"}),this},u.prototype.select=function(t,e){return t=t.replace(/^\\s*/,"").replace(/\\s*$/,""),/^</.test(t)?u().generate(t):(e||document).querySelectorAll(t)},u.prototype.serialize=function(){var r=this;return this.slice(this.first().elements).reduce(function(e,n){return!n.name||n.disabled||"file"===n.type?e:/(checkbox|radio)/.test(n.type)&&!n.checked?e:"select-multiple"===n.type?(u(n.options).each(function(t){t.selected&&(e+="&"+r.uri(n.name)+"="+r.uri(t.value))}),e):e+"&"+r.uri(n.name)+"="+r.uri(n.value)},"").slice(1)},u.prototype.siblings=function(t){return this.parent().children(t).not(this)},u.prototype.size=function(){return this.first().getBoundingClientRect()},u.prototype.slice=function(t){return t&&0!==t.length&&"string"!=typeof t&&"[object Function]"!==t.toString()?t.length?[].slice.call(t.nodes||t):[t]:[]},u.prototype.str=function(e,n){return function(t){return"function"==typeof t?t.call(this,e,n):t.toString()}},u.prototype.text=function(e){return void 0===e?this.first().textContent||"":this.each(function(t){t.textContent=e})},u.prototype.toggleClass=function(t,e){return!!e===e?this[e?"addClass":"removeClass"](t):this.eacharg(t,function(t,e){t.classList.toggle(e)})},u.prototype.trigger=function(t){var o=this.slice(arguments).slice(1);return this.eacharg(t,function(t,e){var n,r={bubbles:!0,cancelable:!0,detail:o};try{n=new window.CustomEvent(e,r)}catch(t){(n=document.createEvent("CustomEvent")).initCustomEvent(e,!0,!0,o)}t.dispatchEvent(n)})},u.prototype.unique=function(){return u(this.nodes.reduce(function(t,e){return null!=e&&!1!==e&&-1===t.indexOf(e)?t.concat(e):t},[]))},u.prototype.uri=function(t){return encodeURIComponent(t).replace(/!/g,"%21").replace(/'/g,"%27").replace(/\\(/g,"%28").replace(/\\)/g,"%29").replace(/\\*/g,"%2A").replace(/%20/g,"+")},u.prototype.val=function(e){return void 0===e?this.first().value:this.each(function(t){t.value=e})},u.prototype.wrap=function(t){return this.map(function(e){return u(t).each(function(t){(function(t){for(;t.firstElementChild;)t=t.firstElementChild;return u(t)})(t).append(e.cloneNode(!0)),e.parentNode.replaceChild(t,e)})})},"object"==typeof module&&module.exports&&(module.exports=u,module.exports.u=u);"""

files_to_create = {
	'README.md': readme_text%data,
	'LICENSE': license_text%data,
	'.gitattributes': gitattributes_text,
	'.gitignore': gitignore_text,
	'.eslintrc.json': eslint_text,
	'netlify.toml': netlify_text,
	'.imgbotconfig': imgbot_config,
	'increment.py': increment_py,
	'package.json': package_text%data,
	'tailwind.config.js': tailwind_config_text,
	'postcss.config.js': postcss_config_text,
}

folder_name = project_dev_name

create_dir(folder_name)

for key in files_to_create:
	with open(folder_name + '/' + key, 'x') as f:
		f.write(files_to_create[key])

create_dir(folder_name + '/src')
create_dir(folder_name + '/src/components')
create_dir(folder_name + '/src/img')
create_dir(folder_name + '/dist')
create_dir(folder_name + '/dist/css')
create_dir(folder_name + '/dist/img')
create_dir(folder_name + '/dist/img/icons')
create_dir(folder_name + '/dist/js')
create_dir(folder_name + '/dist/js/lib')
create_dir(folder_name + '/dist/pages')

with open(folder_name + '/src/styles.css', 'x') as f:
	f.write(src_styles_text)
with open(folder_name + '/src/components/button.css', 'x') as f:
	f.write(src_btn_styles)
with open(folder_name + '/src/img/icon.svg', 'x') as f:
	f.write(icon_svg)
with open(folder_name + '/dist/js/scripts.js', 'x') as f:
	f.write(dist_js_text)
with open(folder_name + '/dist/js/lib/umbrella.min.js', 'x') as f:
	f.write(umbrella_js)
with open(folder_name + '/dist/sw.js', 'x') as f:
	f.write(service_worker_js_text%data)
with open(folder_name + '/dist/manifest.webmanifest', 'x') as f:
	f.write(manifest_json_text%data)
with open(folder_name + '/dist/index.html', 'x') as f:
	f.write(index_html_text%data)
with open(folder_name + '/dist/404.html', 'x') as f:
	f.write(html_404_text%data)
with open(folder_name + '/dist/pages/fallback.html', 'x') as f:
	f.write(fallback_html_text%data)

input('Press any key to continue . . .')

print('Installing Packages...')

# npm install
dir_path = os.path.dirname(os.path.realpath(__file__) ) # directory containing this script
dir_path += '/' + folder_name
os.chdir(dir_path)
subprocess.check_call('npm i', shell=True)

print('Setup finished. npm run dev-serve to begin working. Ctrl+Shift+R to hard reload the webpage if cached from another project. Copy your icon to src/img/icon.svg and npm run generate-assets to add your icon.')
input('Press any key to continue . . .')
