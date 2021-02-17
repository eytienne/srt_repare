import argparse
import math
import re
from typing import Match

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("duration", help="duration of the video (in seconds)", type=float)
parser.add_argument("begin", help="begin delay", type=float)
parser.add_argument("end", help="end delay", type=float)
parser.add_argument("-df", "--debug-frames", nargs="*", help="Debug frame", type=int)
parser.add_argument("-e", "--encoding", default="cp1252", type=str)
parser.add_argument("-o", "--output", help="Output filenae", type=str)
args = parser.parse_args()
print(args)

def lerp(a: float, b: float, t: float):
    '''
    Linearly interpolates between a and b
    Returns a when t = 1
    Returns b when t = 0
    '''
    return (t * a) + ((1-t) * b)

def replace_time(match: Match):
    matched: str = match.group()
    h, m, s = map(lambda s: float(s.replace(",", ".")), matched.split(':'))
    # print(h, m, s)
    ts = h * 3600 + m * 60 + s

    add = lerp(args.begin, args.end, 1 - ts / args.duration)
    # print(add)
    ts += add

    # hours
    hours = ts // 3600
    # remaining seconds
    ts = ts - (hours * 3600)
    # minutes
    minutes = ts // 60
    # remaining seconds
    seconds = ts - (minutes * 60)
    # total time
    return '{:02}:{:02}:{:02},{:03}'.format(int(hours), int(minutes), int(seconds), math.floor((ts-math.floor(ts))*1000))

with open(args.file, mode="r", encoding=args.encoding) as src:
    dest_file: str = None
    if args.output:
        dest_file = args.output
    else:
        dest_file = args.file
        dest_file = re.sub(r"(\.\w+)$", r"_repared\1", dest_file)

    with open(dest_file, mode="w+") as dest:
        ii = 0
        for line in src:
            iimatch = re.match('^\d+$',line)
            if iimatch != None:
                ii = int(iimatch.group())
            rline = re.sub(
               r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', replace_time, line)
            if ii in args.debug_frames or []:
                print(rline)
                pass
            dest.write(rline)
