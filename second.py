


from imdbpie import Imdb
import os
import re
import mrules as mr

rootDir = '/media/titan/videos/python-tmp'
rootDir = '/media/titan/videos/movies/Guardians of the Galaxy'
rootDir = '/media/titan/videos/movies'
# rootDir = '/media/titan/videos/python-tmp'
words = dict()

def validate_file(file_path, file_name):
	if(not(os.path.exists(file_path))):
		return False

	file_stats = os.stat(file_path)
	b_result = file_stats.st_size < 100*(2**20)
	if (b_result):
		return False

	print('\t{0} -- {1}'.format(fname, file_stats.st_size))
	return True

def process_file_name(file_path, file_name):
	if not validate_file(file_path, file_name):
		return
	# for word in re.split('\.| ', fname):
	# 	if(words.get(word) is None):
	# 		words[word] = 0
	# 	words[word] = words[word] + 1
	str_offset='\t\t'
	matches = mr.Rule.match(file_name, str_offset)
	print(str_offset + str(matches))
	print('')
	
print([r.name for r in mr.rules])

	
for dirName, subdirList, fileList in os.walk(rootDir):
	print('%s' % dirName)
	for fname in fileList:
		file_path = dirName + '/' + fname
		
		process_file_name(file_path, fname)
	# for subdir in subdirList:
	# 	print('sub: %s' % subdir)


word_frequencies = dict()
for k, v in words.items():
	if(word_frequencies.get(v) is None):
		word_frequencies[v] = []
	word_frequencies[v].append(k)

words_values = list(words.values())
freqs_of_interest = [freq for freq in words_values if freq > 20]
freqs_of_interest.sort()

for freq in freqs_of_interest:
	print('{0} - x{1}'.format(word_frequencies.get(freq), freq))
