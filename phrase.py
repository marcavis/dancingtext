#!/usr/bin/env python
#usage: call with ./phrase.py line1 line2 line3 line4
#lines can have spaces if they are inside quotes, like:
#./phrase.py this "is a" phrase
import subprocess, sys


def bash(arg):
    return subprocess.check_output(['bash','-c', arg])
    
    
def main(phrase, line):
    for frame in range(14):
        phrase = "".join([x for x in phrase if x.isalpha() or x == " "])
        phrase = phrase.lower()
        
        for letter in phrase:
            let = letter
            #spaces use 9.gif as their spritesheet since <space>.gif is more awkward
            if letter == " ":
                let = "9"
            
            crop = "convert -crop 233x185+" + str(frame * 233) +"+0 " + let + \
                        ".gif +repage bak-" + \
                        let + ("%02d" % frame) + ".png"
            bash(crop)
        inputFiles = " ".join(["bak-" + x + ("%02d" % frame) + ".png" for x in phrase.replace(" ","9")])
        bash("convert -background white +append -flatten " + inputFiles + \
        " line-" + ("%02d" % line) + "-output-" + ("%02d" % frame) + ".png")
   
        #
        #print inputFiles

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        lineNum = 0
        for x in sys.argv[1:]:
            main(x, lineNum)
            lineNum += 1
        for x in range(14):
            bash ("convert -append -background white -gravity center line*output-" + \
             ("%02d" % x) + ".png final-output-" + ("%02d" % x) + ".png")
        bash("convert -delay 12 -resize 560x final-output-*.png phrase-tw.gif")
        bash("convert -delay 12 final-output-*.png phrase-big.gif")
        bash("rm line-*-output-*")
        bash("rm final-output-*")
        bash("rm bak-*")
    else:
        print "To use the script, write the lines you want as arguments."
        print "Lines can have spaces if they're enclosed in quotes, as in:"
        print "./phrase this \"is a\" phrase"
