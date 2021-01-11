import os, shutil

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
input('Done.')
