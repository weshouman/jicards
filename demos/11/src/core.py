#!/usr/bin/python

import os, glob, sys, time
from gimpfu import *

def get_bgs(dir):
  bg_dir = os.path.join(dir, 'bg')
  return glob.glob(os.path.join(bg_dir, '*.jpg'))

def get_fgs(dir):
  fg_dir = os.path.join(dir, 'fg')
  return glob.glob(os.path.join(fg_dir, '*.jpg'))

# debug methods
# get all the fields of the given object
def get_obj_fields(obj):
  return ', '.join(i for i in dir(obj) if not i.startswith('__'))

# This helper is there only as a future reference
def is_layer_visible(layer, style="PYTHON"):
  if style=="C":
    return pdb.gimp_drawable_get_visible(layer)
  else:
    return layer.visible

# This helper is there only as a future reference
def get_image_layers(image, style="PYTHON"):
  if style=="C":
    return pdb.gimp_image_get_layers(image)
  else:
    return image.layers

def load_multi_images(filenames, fmt="JPEG"):
  if fmt == "JPEG":
    return [pdb.file_jpeg_load(x, x) for x in filenames]
  else:
    print "ERROR: %s is not supported only JPEG format is supported" % fmt
    return []

def transfer_layer_method1(src_layer, dst_img):
  """
  shall return the transfered layer
  Not tested thoroughly
  Usage:
  transfer_layer_method1(src_img.layers[0], dst_img)
  """
  return pdb.gimp_layer_new_from_drawable(src_layer, dst_img)

def transfer_layer_method2(src_layer, dst_img):
  """
  shall return the transfered layer
  Not tested
  Usage:
  transfer_layer_method2(src_img.layers[0], dst_img)
  """
  tmplayer = src_layer.copy()
  return pdb.gimp_image_insert_layer(dst_img, tmplayer, None, 0)

def transfer_layer_method3(src_layer, dst_img):
  """
  shall return the transfered layer
  Not tested, and I don't know how it could be correctly implemented
  Usage:
  transfer_layer_method3(src_img.layers[0], dst_img)
  """
  pdb.gimp_edit_copy(src_layer)
  pdb.gimp_image_insert_layer(dst_img, src_layer, None, 0)
  pdb.gimp_edit_paste(dst_img.layers[0])

def mixer(infile, fg, outdir, outfile):
  start = time.time()

  print "-- %s: processing for %s" % (infile, fg)

  # Store the infile and fg images into images array
  images = load_multi_images([infile, fg], "JPEG")
  # NOTE: adding a single file is achieved by
  # images = []
  # images.append(pdb.file_jpeg_load(infile, infile))
  print "-- %s: loaded" % infile

  width = images[0].width
  height = images[0].height

  new_im = gimp.Image(width, height, RGB)

  # NOTE
  # For a simple image, the len(images[0].layers) would be 1
  # nevertheless we should go through all the layers
  for l in images[0].layers:
    nl = pdb.gimp_layer_new_from_drawable(l, new_im)
    # 0 is the top layer
    new_im.add_layer(nl, 0)
  # print len(new_im.layers)

  for l in images[1].layers:
    nl = pdb.gimp_layer_new_from_drawable(l, new_im)
    # 0 is the top layer
    new_im.add_layer(nl, 0)
  # print len(new_im.layers)

  print "-- %s: saving" % outfile
  # This call may not be needed
  # but it shows good debug info
  new_im.flatten()

  if len(new_im.layers) > 0:
    any_visible_layer = False
    for l in new_im.layers:
      if l.visible == True:
        any_visible_layer = True
        break

    if any_visible_layer == True:
      pdb.file_jpeg_save(new_im, new_im.active_drawable, outfile, outfile, 0.5,0,1,0,"",0,1,0,0)
    else:
      print "Error saving: New image had no visible layers added to it, failed to save the output image"

  else:
    print "Error saving: New image had no layers added to it, failed to save the output image"

  print "-- %s: saved" % outfile
  pdb.gimp_image_delete(new_im)

  end = time.time()
  print "-- %s: processed in %.2f seconds" %(infile, end-start)

def run(indir, outdir):
  start = time.time()

  print "- Processing: \"%s\"" % indir
  print "- Saving  to: \"%s\"" % outdir

  for infile in get_bgs(indir):
    for fg in get_fgs(indir):
      outfile = get_outfile_name(outdir, [infile, fg])
      mixer(infile, fg, outdir, outfile)
      # process(infile, outdir)

  end = time.time()
  print "- Core processed in: %.2f seconds" % (end-start)

def get_outfile_name(outdir, infiles, ext="jpg"):
  newbase = ""
  for i, infile in enumerate(infiles):
    if i > 0:
      # in between
      newbase += "-"
    newbase += os.path.splitext(os.path.basename(infile))[0]

  return os.path.join(outdir, newbase + "." + ext)

if __name__ == "__main__":
  print "Core is triggered with args: %s" % sys.argv
