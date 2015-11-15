
from imdb import IMDb
import os

def ohyeah(movie_ids,root_dir):
	ia = IMDb()

	for movie_id in movie_ids:
		print("{0} ...".format(movie_id))
		movie1 = ia.get_movie(movie_id[2:])
		directors =  ",".join(map(lambda dir: dir['name'],movie1['director'])).encode('utf-8')
		title0 = movie1['title'].encode('utf-8')
		title1 = movie1['akas'][0].split("::")[0]

		# print movie1
		print title0
		print title1
		print directors
		print movie1['year']
		
		str_dir = '{0} [{1}] [{2}] ({3})'.format(title0,title1,directors,movie1['year'])
		print str_dir
		
		os.system('mkdir "{0}"'.format(str_dir))
	


