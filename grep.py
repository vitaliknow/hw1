import argparse
import sys
import re

def output(line):
    print(line)

def tostr(num, sep, line, line_numerate):
	if line_numerate:
		return (str(num+1) + sep + line)
	else:
		return(line)		
		

def grep(lines, params):
	params.pattern = params.pattern.replace('*', '.*').replace('?','.')
	if params.count:
		counter = 0
		for line in lines:
			if params.pattern in line:
				counter += 1
		output(counter)
		
	else:
		buffer = []
		count = 0
		max_before = params.before_context
		max_after = params.after_context
		if params.context:
			max_before = max_after = params.context
			
		if params.ignore_case:
			params.pattern = params.pattern.lower()	
				
		for num,line in enumerate(lines):
			line = line.rstrip()
			
			if params.ignore_case: 
				temp_line = line.lower()
			else:
				temp_line = line
			
			if ((re.search(params.pattern, temp_line) is not(None)) ^ params.invert):
				for i in buffer:
					output(i)
				output(tostr(num, ':', line, params.line_number))
				buffer = []
				count = 1
				
			elif 0 < count <= max_after:
				output(tostr(num, '-', line, params.line_number))
				count+=1
				
			elif max_before:
					buffer.append(tostr(num, '-', line, params.line_number))
			
			if (len(buffer) == max_before+1):
				buffer.pop(0)	
				
			
def parse_args(args):
	parser = argparse.ArgumentParser(description='This is a simple grep on python')
	parser.add_argument(
		'-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
	parser.add_argument(
		'-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
	parser.add_argument(
		'-c',
		action="store_true",
		dest="count",
		default=False,
		help='Only a count of selected lines is written to standard output.')
	parser.add_argument(
		'-n',
		action="store_true",
		dest="line_number",
		default=False,
		help='Each output line is preceded by its relative line number in the file, starting at line 1.')
	parser.add_argument(
		'-C',
		action="store",
		dest="context",
		type=int,
		default=0,
		help='Print num lines of leading and trailing context surrounding each match.')
	parser.add_argument(
	'-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
	parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
	parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
	return parser.parse_args(args)


def main():
	params = parse_args(sys.argv[1:])
	grep(sys.stdin.readlines(), params)

if __name__ == '__main__':
    main()