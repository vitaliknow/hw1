import argparse
import sys


def output(line):
    print(line)


def grep(lines, params):
	if params.invert: 
		for line in lines:
			line = line.rstrip()
			if not(params.pattern in line):
				output(line)
				
	elif params.ignore_case:
		for line in lines:
			line = line.rstrip()
			if params.pattern.lower() in line.lower():
				output(line)
				
	elif params.count:
		count = 0
		for line in lines:
			line = line.rstrip()
			if params.pattern in line:
				count += 1
		print (count)
		
	elif params.line_number:
		num = 0
		for line in lines:
			line = line.strip()
			num += 1
			if params.pattern in line:
				print(num, line, sep = ':')
	
	else:
		for line in lines:
			line = line.rstrip()
			if params.pattern in line:
				output(line)
	
	if params.before_context:
		list_lines = []
		count = 0
		for line in lines:
			line = line.rstrip()
		
			if count == params.before_context:
				list_lines.pop(-(count))
				count -= 1
			
			
			
			list_lines.append(line)
			
			if params.pattern in line:
				count = 0
			else: 
				count += 1
		print (list_lines)
	
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
	print(params)
	
	
if __name__ == '__main__':
    main()