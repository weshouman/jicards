#!/usr/bin/python

import os, glob, sys, time
from gimpfu import *

def process(infile, outdir, outfile):
  start = time.time()
  print "-- %s: Processing" % infile

  # ADD YOUR CODE HERE

  end = time.time()
  print "-- %s: Processed in %.2f seconds" %(infile, end-start)

def run(indir, outdir):
  start = time.time()
  print "- Input from: \"%s\"." % indir
  print "- Output  to: \"%s\"." % outdir

  for infile in get_images(indir):
    outfile = os.path.splitext(os.path.basename(infile))[0]
    process(infile, outdir, outfile)

  end = time.time()
  print "- DB Based Plugin processed in: %.2f seconds" % (end-start)

if __name__ == "__main__":
  print "- DB Based Plugin is triggered with args: %s" % sys.argv
