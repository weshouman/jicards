#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os,glob,sys,time
from gimpfu import *


def process(infile, outdir):
        print "Processing file %s " % infile
        image = pdb.file_jpeg_load(infile,infile)
        drawable = pdb.gimp_image_get_active_layer(image)

        print "File %s loaded OK" % infile
        pdb.plug_in_photocopy(image, drawable,8.,0.8,0.2,0.2)
        pdb.plug_in_cartoon(image, drawable, 7.,0.2)
        outfile=os.path.join(outdir, os.path.basename(infile))
        outfile=os.path.join(os.path.dirname(infile),outfile)
        print "Saving to %s" % outfile
        pdb.file_jpeg_save(image, drawable, outfile, outfile, "0.5",0,1,0,"",0,1,0,0)
        print "Saved to %s" % outfile
        pdb.gimp_image_delete(image)


def run(indir, outdir):
        start=time.time()
        print "Running on directory \"%s\"" % indir
#   os.mkdir(os.path.join(directory,'processed'))
        for infile in glob.glob(os.path.join(indir, '*.jpg')):
                process(infile, outdir)
        end=time.time()
        print "Finished, total processing time: %.2f seconds" % (end-start)


if __name__ == "__main__":
        print "Running as __main__ with args: %s" % sys.argv
