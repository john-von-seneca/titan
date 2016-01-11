import re
import time

class Rule:
	@staticmethod
	def match(file_name, str_offset='\t\t'):
		in_matched_rules = 0
		matches = []
		for rule1 in rules:
			# print('\t\t' + str(rule1.name) + ' -> ' + str(rule1.is_valid(file_name)))
			b_result, data = rule1.process(file_name, str_offset)
			if b_result:
				in_matched_rules += 1
				#print(str_offset + str(data))
				#matches.append(data)
				matches = data
				break
			
		if(in_matched_rules==0):
			raise NameError('No Rules Matched')
		return matches
		
	def __init__(self):
		print('yo')

	def process(self, file_name, str_offset='\t\t'):
		pmtrs = None
		b_found = self.is_valid(file_name)
		if b_found:
			print(str_offset + self.name + '')
			pmtrs = self.extract_parameters(file_name)
		
		return [b_found, pmtrs]

	def is_valid(self, file_name):
		return file_name.find(self.pattern_in_file)!=-1

	def trim_extension(self, file_name):
		return re.match('(.*)\..*$',file_name).group(1)

	def trim_non_title(self, file_name):
		for pattern in ['BRRip','x264',
						b'By Baggins\xc2\xa9'.decode(),
						b'shared by nightmare\xe2\x84\xa2'.decode(),
						b'by nightmare\xe2\x84\xa2'.decode(),
						b'by \xc6\x92antom\xe2\x84\xa2'.decode(),
						'-by ClintEastwood',
						'SHARED BY JOKER',
						'XviD','NvadR',
						'1080p','BluRay','720p','480p',
						'Shared by Cockfighter','\\[Knight_collection\]',
						'by bitter',
						'BKP_CSNO',
						'by Zangetsu',
						'BDRip','KORUB','HDRiP','m-HD','Blu Ray Rip']:
			# match = re.search(pattern, file_name, flags=re.IGNORECASE)
			# if match is None:
			# 	continue
			# file_name = file_name[:max(0,match.span()[0])] + file_name[match.span()[1]:]
			file_name = re.sub(pattern, '', file_name, flags=re.IGNORECASE)
		for pattern in ['\.', '_', '-', '\(\)', '\[\]' ,'\s+']:
			file_name = re.sub(pattern,' ',file_name)
			
		return file_name
	
	def format_title(self, str_title):
		title = str_title
		for pattern in ['.','-']:
			title = title.replace(pattern,' ')
		return title

class Yify(Rule):
	def __init__(self):
		self.name = 'yify'
		self.pattern_in_file = 'YIFY'

	def extract_parameters(self, file_name):
		match_obj = re.match('(.*)\.([0-9]{4})\.(.*)\.(.*)\.(.*)\.YIFY',file_name)
		if match_obj is None:
			raise NameError(self.name + ' not matching ' + file_name)
		
		pmtrs = dict()
		pmtrs['rule'] = self.name
		pmtrs['title'] = match_obj.group(1).replace('.', ' ')
		pmtrs['year'] = int(match_obj.group(2))
		pmtrs['quality'] = match_obj.group(3)
		pmtrs['source'] = match_obj.group(4)
		pmtrs['codec'] = match_obj.group(5)
		return pmtrs

class Fxg(Rule):
	def __init__(self):
		self.name = 'fxg'
		self.pattern_in_file = 'FXG'

	def extract_parameters(self, file_name):
		
		match_obj = re.match('(.*)\[([0-9][0-9][0-9][0-9])\]DvDrip.*\[(.*)\]-FXG.avi',file_name)
		if match_obj is None:
			raise NameError(self.name + ' not matching ' + file_name)
		
		pmtrs = dict()
		pmtrs['rule'] = self.name
		pmtrs['title'] = match_obj.group(1).replace('.', ' ')
		pmtrs['year'] = int(match_obj.group(2))
		pmtrs['source'] = 'dvd'
		pmtrs['lang'] = match_obj.group(3)
		return pmtrs

class AnoXmous(Rule):
	def __init__(self):
		self.name = 'anoXmous'
		self.pattern_in_file = 'anoXmous'

	def extract_parameters(self, file_name):
		
		match_obj = re.match('(.*)\.([0-9][0-9][0-9][0-9])\.(.*)\.(.*)\.(.*)\.anoXmous',file_name)
		if match_obj is None:
			raise NameError(self.name + ' not matching ' + file_name)
		
		pmtrs = dict()
		pmtrs['rule'] = self.name
		pmtrs['title'] = match_obj.group(1).replace('.', ' ')
		pmtrs['year'] = int(match_obj.group(2))
		pmtrs['quality'] = match_obj.group(3)
		pmtrs['source'] = match_obj.group(4)
		pmtrs['codec'] = match_obj.group(5)
		return pmtrs

class Rbg(Rule):
	def __init__(self):
		self.name = 'rbg'
		self.pattern_in_file = 'RBG'

	def extract_parameters(self, file_name):
		match_obj = re.match('(.*)\s([0-9]{4})\s(.*)\s(.*)\s(.*)\s(.*)-RBG',file_name)
		if match_obj is None:
			raise NameError(self.name + ' not matching ' + file_name)
		
		pmtrs = dict()
		pmtrs['rule'] = self.name
		pmtrs['title'] = match_obj.group(1).replace('.', ' ')
		pmtrs['year'] = int(match_obj.group(2))
		pmtrs['quality'] = match_obj.group(3) + ' ' + match_obj.group(5)
		pmtrs['source'] = match_obj.group(4)
		pmtrs['codec'] = match_obj.group(6)
		return pmtrs

class Generic(Rule):
	def __init__(self):
		self.name = 'Generic'
		trash = time.localtime()
		self.year = trash.tm_year

	def process(self, file_name, str_offset):
		pmtrs = dict()
		pmtrs['rule'] = 'Generic'
		pmtrs['year'] = self.get_year(file_name)
		file_name = self.trim_year(file_name, pmtrs['year'])
		file_name = self.trim_extension(file_name)
		file_name = self.trim_non_title(file_name)
		pmtrs['title'] = self.format_title(file_name)
		return [True, pmtrs]

	# return the last valid year
	def get_year(self, file_name):
		years = re.findall('[0-9][0-9][0-9][0-9]', file_name)
		years = [int(year) for year in years]
		years_valid = [year for year in years if year<=self.year and year>=1930]
		return years_valid[-1] if len(years_valid)>=1 else None
	
	def trim_year(self, file_name, year):
		if year is None:
			return file_name
		
		match = re.search(str(year), file_name)
		return file_name[:max(0,match.span()[0]-1)] + file_name[match.span()[1]:]
	
rules = [Yify(), AnoXmous(), Fxg(), Rbg(), Generic()]

