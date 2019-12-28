#!/usr/bin/python
import csv, sys, argparse, os

def dateIsYear(date):
	if len(date) == 4:
		try:
			int(date)
			return True
		except ValueError:
			return False
	else:
		return False

def processQuestionableDate(date):
	if len(date) == 5 and date[4] == "?":
		if dateIsYear(date[:4]):
			return [date[:4]+"-01-01", date[:4]+"-12-31"]
		elif date[2:4] == "--": #eg: date is 19--
			return [date[:2]+"00-01-01", date[:2]+"09-12-31"]
		elif date[3:4] == "-": #eg date is 192-
			return [date[:3]+"0-01-01", date[:3]+"9-12-31"]
		else:
			return ["", ""]
	else:
		return ["", ""]


def processBetweenDate(date):
	dates = ["", ""]
	if date.startswith("between "): #hack it off  and only continue processing if it was present in the first place
		date = date[8:]
		if date.endswith("?"): #hack that off as well
			date = date[:-1]
		if " and " in date: #split the string on that
			dates = date.split(" and ")
		if dateIsYear(dates[0].strip()) and dateIsYear(dates[1].strip()):
			dates[0] = dates[0].strip()+"-01-01"
			dates[1] = dates[1].strip()+"-12-31"
	return dates

def stripDateBrackets(date):
	if date.startswith('[') and date.endswith(']'):
		return date[1:-1]
	else:
		return date

def standarizeCirca(date):
	if date.startswith("c") or date.startswith("ca") or date.startswith("circa"):
		try:
			return "circa " + "".join(date[date.index(" ")+1:].split())
		except ValueError: #likely there is no space between c or ca. before date
			if date.startswith("ca.") and not date.startswith("ca. "):
				return "circa " + "".join(date[3:].split())
			elif date.startswith("c") and not date.startswith("c "):
				return "circa " + "".join(date[1:].split())
			else:
				return date
	else:
		return date

def processCircaDate(date):
	dates = ["",""]
	if date.startswith("circa "):
		date = date[6:].strip()
		print(date)
	if "?" in date:
		print(date)
		dates = processQuestionableDate(date)
	elif dateIsYear(date):
		dates[0] = date + "-01-01"
		dates[1] = date + "-12-31"
	return dates


def processDates(entries):
	cr_date = ""
	try:
		#get the index of the Date:creation field and set insert points for begin and end dates
		cr_date_ind = entries[0].index("Date:creation")
		begin_date_ind = cr_date_ind + 1
		end_date_ind = cr_date_ind + 2
		for row in entries:
			print(row[0])
			dates = ["", ""]
			#add header values for Begin date and End date
			if "Date:creation" in row:
				row.insert(begin_date_ind, "Begin date")
				row.insert(end_date_ind, "End date")

			else:
				cr_date = row[cr_date_ind].strip()
				cr_date = stripDateBrackets(cr_date)
				cr_date = standarizeCirca(cr_date)
				if len(cr_date) < 7:
					cr_date = "".join(cr_date.split()) #get rid of extraneous whitespace on questionable dates like 192 -? or 192- ?
				row[cr_date_ind] = cr_date
				if dateIsYear(cr_date):
					dates[0] = cr_date + "-01-01"
					dates[1] = cr_date + "-12-31"
				elif "?" in cr_date and "between" not in cr_date and "circa" not in cr_date:
					dates = processQuestionableDate(cr_date)
				elif cr_date.startswith("between"):
					dates = processBetweenDate(cr_date)
				elif cr_date.startswith("circa"):
					dates = processCircaDate(cr_date)
				row.insert(begin_date_ind, dates[0])
				row.insert(end_date_ind, dates[1])


	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise

def processGeoSubjects(entries):
	geo_indexes = []
	geo_subjects = []
	#pull subject translations from csv file
	with open("geo.csv", 'rt') as g:
		reader = csv.reader(g, dialect='excel')
		for row in reader:
			geo_subjects.append(row)
	#get the indexes of the geo subject columns
	for i, col in enumerate(entries[0]):
		if col == "Subject:geographic FAST":
			geo_indexes.append(i)
	#go through each row and reconcile the values in each geo column against geo_subjects list
	for row in entries:
		for i in geo_indexes:
			if row[i] != "":
				for geo in geo_subjects:
					if row[i] == geo[0]:
						row[i] = geo[1]

def addLocalIdentifier(entries, identifier):
	header = 'Identifier:local'
	insertIndex = getHeaderIndex(entries[0], "Identifier:roger record") + 1
	addColumn(entries, insertIndex, header)
	columnIndex = getHeaderIndex(entries[0], header) # this should be the same as insertIndex but better safe than sorry
	iter_entries = iter(entries)
	next(iter_entries)
	for row in iter_entries:
		row[columnIndex] = identifier

def addRelatedResource(entries):
	roger_index = getHeaderIndex(entries[0], "Identifier:roger record")
	insert_index = roger_index + 2
	header = 'Related resource:related'
	addColumn(entries, insert_index, header)
	columnIndex = getHeaderIndex(entries[0], header)
	iter_entries = iter(entries)
	next(iter_entries)
	for row in iter_entries:
		row[columnIndex] = "Roger record @ http://roger.ucsd.edu/record=" + row[roger_index] + "~S9"

def addFile2Columns(entries):
	if getHeaderIndex(entries[0], 'File name 2') is None:
		insert_index = getHeaderIndex(entries[0], 'File use') + 1
		addColumn(entries, insert_index, 'File name 2')
	if getHeaderIndex(entries[0], 'File use 2') is None:
		insert_index = getHeaderIndex(entries[0], 'File name 2') + 1
		addColumn(entries, insert_index, 'File use 2')

#add code to clean straggling punctuation at beginning/end of field entries
def cleanFields(entries):
	for row in entries:
		for entry in row:
			entry = entry.strip()
			if entry.startswith(',') or entry.startswith(';') or entry.startswith(':') or entry.startswith('.'):
				entry = entry[1:]
			if entry.endswith(',') or entry.endswith(';') or entry.endswith(':'):
				entry = entry[0:-1]

def getHeaderIndex(header_row, header_name):
	for i, header in enumerate(header_row):
		if header == header_name:
			return i
	return None

def getFileList(dir):
	file_list = []
	zip_list = []
	if os.path.exists(dir) and os.path.isdir(dir):
		for dirName, subdirList, fileList in os.walk(dir):
			for fname in fileList:
				if file_is_zip(fname):
					zip_list.append(fname)
				else:
					file_list.append(fname)

	return file_list, zip_list

def addColumn(data, insert_index, header):
	for i, row in enumerate(data):
		if i == 0:
			row.insert(insert_index, header)
		else:
			row.insert(insert_index, '')

def file_is_pdf(filename):
	if filename[filename.rfind('.') + 1:].lower() == 'pdf':
		return True
	else:
		return False

def file_is_zip(filename):
	if filename[filename.rfind('.') + 1:].lower() == 'zip':
		return True
	else:
		return False

def add_files(entries, dir):
	files, zips = getFileList(dir)
	bib_ind = getHeaderIndex(entries[0], 'Identifier:roger record')
	file1_ind = getHeaderIndex(entries[0], 'File name')
	file1_use_ind = getHeaderIndex(entries[0], 'File use')
	file2_ind = getHeaderIndex(entries[0], 'File name 2')
	file2_use_ind = getHeaderIndex(entries[0], 'File use 2')
	level_ind = getHeaderIndex(entries[0], 'Level')
	with_file_entries = []
	for row in entries:
		bib_num = row[bib_ind]
		entry_files = []
		for f in files:
			if f.startswith(bib_num):
				entry_files.append(f)
		if len(entry_files) == 0:
			with_file_entries.append(row)	# catch things like the header
		elif len(entry_files) == 1:			# single file objects and pdf+zip objects
			f = entry_files[0]
			file_ext = f[f.rfind('.')+1:]
			row[file1_ind] = f
			if file_ext == 'pdf':
				row[file1_use_ind] = "document-service"
			elif file_ext == 'tif':
				row[file1_use_ind] = "image-source"
			f_no_ext = f[:f.rfind('.')]
			#check for matching zip file
			for z in zips:
				if z.startswith(f_no_ext):
					row[file2_ind] = z
					row[file2_use_ind] = "document-source"
			with_file_entries.append(row)
		elif len(entry_files) > 1:
			with_file_entries.append(row)
			for f in entry_files:
				file_ext = f[f.rfind('.')+1:]
				f_no_ext = f[:f.rfind('.')]
				new_row = []
				# create cells for each header value in entries
				for cell in entries[0]:
					new_row.append('')
				new_row[level_ind] = 'Component'
				new_row[file1_ind] = f
				if file_ext == 'pdf':
					new_row[file1_use_ind] = "document-service"
				elif file_ext == 'tif':
					new_row[file1_use_ind] = "image-source"
				for z in zips:
					if z.startswith(f_no_ext):
						new_row[file2_ind] = z
						new_row[file2_use_ind] = "document-source"
				with_file_entries.append(new_row)
	return with_file_entries

def main():
	entries = []
	inputfile = ''
	outputfile = ''
	argsparser = argparse.ArgumentParser()
	argsparser.add_argument('csv', help='csv filename')
	argsparser.add_argument('-d', '--dir', help='Directory path containing files', action='store')
	args = argsparser.parse_args()

	inputfile = args.csv
	outputfile = args.csv[:-4] + '_processed.csv'

	#import container data from csv file, csv should be encoded UTF-8
	with open(inputfile, 'rt', newline='', encoding='utf8') as f:
		reader = csv.reader(f, dialect='excel')
		for row in reader:
			entries.append(row)
	cleanFields(entries)
	processDates(entries)
	addFile2Columns(entries)
	addLocalIdentifier(entries, "scarare")
	addRelatedResource(entries)
	processGeoSubjects(entries)
	if args.dir is not None:
		entries = add_files(entries, args.dir)
	with open(outputfile, 'w+', newline='', encoding='utf8') as w:
		writer = csv.writer(w)
		writer.writerows(entries)

if __name__ == "__main__":
	main()
