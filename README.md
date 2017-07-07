This repo includes some useful demos for working with GIMP

# Demos Description
Following are some insights about each of the included demos

## Demo 01: Image Word Maker
A GUI based plugin that creates an image with a given text and background fill.

## Demo 10: Processor
A CLI based plugin to add a filter into an image and save the result.

## Demo 11: Image Merger
A CLI based plugin that uses a directory of foreground images and another of background images to generate every combination of image merges of both the image.

## Demo 12: DB Based Processor
**WIP**: A plugin to generate images based on both input of an image and a database.

# Known Issues
Following is a list of issues that was found, that seems/seemed challenging to fix.

## Operation Returned 'no return values'
Upon receiving the error `file-jpeg-save returned no return values` that means we are trying to save an image that is not save-able, the second parameter of the `file_jpeg_save()` is the culprit in this error.

### Root cause
I was copying a layer into an image
```
oldlayer = oldimage.layers[0]
newlayer = pdb.gimp_layer_new_from_drawable(oldlayer, newimage)
```
but I was not associating the layer to the image, for example by adding this line
```
newimage.add_layer(newlayer)
```
thus the image ended up having no layers, and when saving there was no layers to be saved


### Analysis
when `newimage.flatten()` there was a helpful error saying that there's no layers to be merged.  
by checking the newlayer visibility, one could find that it's True, finally when checking the newimage's layers, one could find that it had no layers, thus `add_layer` was the first resort to think about

