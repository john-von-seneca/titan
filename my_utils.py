

import os
import re

def can_skip_file(dir_name, f_name):
	file_path = dir_name + '/' + f_name
	if(not(os.path.exists(file_path))):
		return True
	
	file_stats = os.stat(file_path)
	b_result = file_stats.st_size < 100*(2**20)
	if (b_result):
		return True

	# todo: print human readable form
	print('\t{0} -- {1}'.format(f_name, file_stats.st_size))

	return False

# todo: extend blacklist
# purge_words: divx,dvdscr,aac,dvdrip,brrip,UNRATED,WEBSCR,KLAXXON,xvid,r5,com--scOrp,300mbunited,1channel,3channel,bray,blueray,5channel,1GB,1080p,720p,480p,CD1,CD2,CD3,CD4,x264,x264-sUN,Special Edition,Sample,sample
blacklist = ['avi']
def form_search_string(f_name):
	words = re.split('\.| ', f_name)
	words_filtered = [w for w in words if (w not in blacklist)]
	search_str = ' '.join(words_filtered)
	print('=> ' + search_str)
	return search_str
