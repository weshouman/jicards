#!/bin/bash

# Sanity check
MIN_ARG_COUNT=3
if [ $# -lt "${MIN_ARG_COUNT}" ]; then
  echo "- Number of supplied arguments($#) less than expected(${MIN_ARG_COUNT})"
  echo USAGE: demo_generator.bat DEMOS_DIR ID NAME
  echo example: demo_generator.bat "./demos/" 02 "Image merger"
  exit 1
fi

DEMOS_DIR=$1
DEMO_ID=$2
DEMO_NAME=$3

demo_dir=${DEMOS_DIR}/${DEMO_ID}
echo Creating ${demo_dir}

# Sanity check
if [ -d ${demo_dir} ]; then
  echo Directory exists, please specify an unused directory name
  exit 2
fi

mkdir ${demo_dir}
mkdir ${demo_dir}/src
cat <<EOF > ${demo_dir}/src/core.py
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
  print "- ${DEMO_NAME} processed in: %.2f seconds" % (end-start)

if __name__ == "__main__":
  print "- ${DEMO_NAME} is triggered with args: %s" % sys.argv
EOF

mkdir -p ${demo_dir}/tests/01
cat <<EOF > ${demo_dir}/tests/01/README.md
# Basic Test
input:
- INPUT 1
- INPUT 2
output:
- OUTPUT
EOF

mkdir ${demo_dir}/tests/01/in
mkdir ${demo_dir}/tests/01/out
touch ${demo_dir}/tests/01/out/.keep
