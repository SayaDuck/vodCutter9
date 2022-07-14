from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import csv

# csv time format in hh:mm:ss
def timeinseconds(timestr):
    h, m, s = timestr.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# optional
inputprefix = ""
outputprefix = ""

# csv row structure:
# header:
# vodfilename, tourneyname, bracketlink, date (yyyy/mm/dd), gamename, commentators (separated by "+"), TO
# rows:
# start (hh:mm:ss), end (hh:mm:ss), round, p1name, p2name, p1chars (separated by "+"), p2chars (separated by "+")


csvnames = []

for i in range(len(csvnames)):
    with open("data/" + csvnames[i], 'r') as file:
        data = csv.reader(file,delimiter=',')
        header = next(data)

        vodfile, tourneyname, bracketlink, date, gamename, commentators, to = [header[i] for i in range(7)]
        commentators = commentators.split("+")
        vodfile = inputprefix + vodfile
        descriptionfilename = "output/" + tourneyname + ".txt"

        with open(descriptionfilename, 'w') as textfile:
            for line in data:
                start, end, round, p1name, p2name, p1chars, p2chars = [line[i] for i in range(7)]
                p1chars = p1chars.split("+")
                p2chars = p2chars.split("+")

                outputname = "output/" + outputprefix + tourneyname + " - " + round + " - " + p1name + " (" + ", ".join(p1chars) + ") vs " + p2name + " (" + ", ".join(p2chars) + ") " + gamename + " Tournament" + ".mp4"
                
                description = tourneyname + " is a " + gamename + " tournament organized by " + to + " held on " + date + ".\nTourney Commentators: " + ", ".join(commentators) + "\nBracket: " + bracketlink

                textfile.write(description)
                textfile.write('\n\n')

                start = timeinseconds(start)
                end = timeinseconds(end)

                ffmpeg_extract_subclip(vodfile, start, end, targetname=outputname)

        textfile.close()