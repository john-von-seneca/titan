from imdbpie import Imdb
import os
import re
import my_utils

dir_movies = '/media/titan/videos/movies'
dir_cache = '/media/titan/videos/imdbpie-cache'

imdb = Imdb(anonymize=True, cache = dir_cache)
b_first_file_found = False

for dirName, subdirList, fileList in os.walk(dir_movies):
	for fname in fileList:
		
		if(my_utils.can_skip_file(dirName, fname)):
			continue

		search_str = my_utils.form_search_string(fname)
		print(imdb.search_for_title(search_str))
		
		b_first_file_found = True
		break

		
	if b_first_file_found:
		break

