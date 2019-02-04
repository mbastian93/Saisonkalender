# @author marcel bastian
# converts calender from csv format to ics file

import sys, getopt, datetime, random

def convertCalendar(inputFile, outputFile):
	readFile = open(inputFile, 'r', encoding='latin_1')
	writeFile = open(outputFile, 'w')
	writeFile.write('BEGIN:VCALENDAR\nPRODID:-//TV Nierstein\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-TIMEZONE:Europe/Berlin\n')
	# skip first 3 lines
	lines = readFile.readlines()[3:]
	for line in lines:
		writeFile.write('BEGIN:VEVENT\n')
		# remove all "
		line = line.replace('"', '')
		event = line.split(';')
		# Time stamp start
		writeFile.write("DTSTART:%s\n" % convertTime(event[2], event[3]))
		# Time stamp end
		hour = str(int(event[3].split(':')[0]) + 2)
		endTime = '%s%s'%(hour, event[3][2:])
		writeFile.write("DTEND:%s\n" % convertTime(event[2], endTime))
		# Time stamp creation
		writeFile.write('DTSTAMP:' + str(datetime.datetime.now().year) + '0730T000000\n')
		# Generate UID
		writeFile.write('UID:%s\n' % generateUID())
		writeFile.write('CREATED:20160808T043800\n')
		# Description
		writeFile.write('DESCRIPTION:%s\n' % convertDescription(event[0], event[1], event[5], event[6], event[7], event[12]))
		writeFile.write('LAST-MODIFIED:%s\n' % generateTimeStamp())
		# Location
		writeFile.write('LOCATION:%s\n' % convertLocation(event[10], event[9], event[8],))
		writeFile.write('SEQUENCE:0\nSTATUS:CONFIRMED\n')
		# Summary
		writeFile.write('SUMMARY:%s\n' % convertSummary(event[1], event[5], event[6]))
		writeFile.write('TRANSP:TRANSPARENT\nEND:VEVENT\n')
	writeFile.write('END:VCALENDAR\n')
	readFile.close()
	writeFile.close()
	return
	
# generate timestamp from date and time string	
def convertTime(date, time):
	splittedDate = date.split('.')
	string = '20' + splittedDate[2] + splittedDate[1] + splittedDate[0] + 'T' + time.replace(':', '') + '00'
	return string

# generate	description
def convertDescription(number, unit, teamA, teamB, venue, desc):
	string = unit + " " + number + '\\n' + teamA + ' - ' + teamB + '\\n' + venue + '\\n' + desc.rstrip()
	return string
	
def convertLocation(street, city, zip):
	string = street + '\, ' + zip + ' ' + city
	return string
	
def convertSummary(unit, teamA, teamB):
	string = unit + ' ' + teamA + ' - ' + teamB
	return string

# generate UID based on timestamp	
def generateUID():
	date = datetime.datetime.now()
	UID =  generateTimeStamp() + str(date.microsecond) + str(random.randint(0,1000)) + '@handball-nierstein.de'
	return UID
	
def generateTimeStamp():
	date = datetime.datetime.now()
	return str(date.year) + str(date.month) + ('0' if date.day < 10 else '') + str(date.day) + 'T' + str(date.hour) + str(date.minute) + str(date.second)
	
def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('test.py -i <inputfile> -o <outputfile>')
		ys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	convertCalendar(inputfile, outputfile)
	
if __name__ == "__main__":
	main(sys.argv[1:])
