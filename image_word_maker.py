#!/usr/bin/env python

# Hello World on image in GIMP Python

from gimpfu import *
import os.path #file utilities

def image_word_maker(initstr, font, size, color, file) :

#    # Use in case we want to work directly on the given file
#    if os.path.isfile(file) is True:
#        img_loaded = pdb.gimp_file_load(file, file)

#        WIDTH = img_loaded.width
#        HEIGHT = img_loaded.height

#        layer0 = gimp.Layer(img_loaded, "loaded image", WIDTH, HEIGHT,
#                            RGB_IMAGE, 100, NORMAL_MODE)
#        img_loaded.add_layer(layer0, 1)
#        gimp.Display(img_loaded)

    # Make a new image. Size 10x10 for now -- we'll resize later.
    img = gimp.Image(1, 1, RGB)

    # Save current foreground color
    pdb.gimp_context_push()

    # Set text color
    gimp.set_foreground(color)

    # Create a new text layer (-1 for the layer means create a new layer)
    layer = pdb.gimp_text_fontname(img, None, 0, 0, initstr, 10,
                                   True, size, PIXELS, font)

    WIDTH = layer.width
    HEIGHT = layer.height

    # Resize the image to the size of the layer
    img.resize(WIDTH, HEIGHT, 0, 0)

    # Background layer
    background = gimp.Layer(img, "Background", WIDTH, HEIGHT,
                            RGB_IMAGE, 100, NORMAL_MODE)
    background.fill(BACKGROUND_FILL)
    img.add_layer(background, 1)

    # Sanity check for file existance
    if os.path.isfile(file) is True:
        layer2 = pdb.gimp_file_load_layer(img, file)
        pdb.gimp_image_insert_layer(img, layer2, None, 0)

        ## saving into a file
        # Duplicate into a new tmp image and 
        new_image = pdb.gimp_image_duplicate(img)

        # Merge layers
        layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)

        split_file = os.path.splitext(file)
        file_new = split_file[0] + '2' + split_file[1]
	# a debugging print
        #pdb.gimp_message(file_new)

        # Save into a file
        pdb.gimp_file_save(new_image, layer, file_new, file_new)

        # Delete new image
        pdb.gimp_image_delete(new_image)

    # Create a new image window
    gimp.Display(img)

    # Show the new image window
    gimp.displays_flush()

    # Restore the old foreground color:
    pdb.gimp_context_pop()

register(
    "python_image_word_maker",
    "text with image",
    "Create & save a new image with text string and an image file from desk",
    "Walid Shouman",
    "Walid Shouman",
    "2015",
    "text with image (pyfu)",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "string", "Text string", 'Hello, worlds!'),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "size", "Font size", 50, (1, 3000, 1)),
        (PF_COLOR, "color", "Text color", (1.0, 0.0, 0.0)),
        (PF_STRING, "file", "GlobPattern", '/tmp/star.png')
    ],
    [],
    image_word_maker, menu="<Image>/File/Create")

main()
