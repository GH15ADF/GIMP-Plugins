#!/usr/bin/env python

# MatrixPortal_filtered_view.py Rel 1
# Simulate display on a Matrix Portal RGB LED Display
# Created by Charles Foster
# Comments directed to https://gimplearn.net
#
# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
#
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release

from gimpfu import *
from array import array

# Needed if you want to print() for debugging
# import sys
# sys.stderr = open('c:/temp/er.txt', 'a')
# sys.stdout = open('c:/temp/log.txt', 'a')


def mp_filtered_view(image, brightness, contrast, bitspp) : #FUNCTION DEFINITION
	# create the mask to discard the selected number of low order bits
	BIT_DEPTH = int(bitspp)
	mask = 0xFF >> BIT_DEPTH
	bit_mask = 0b11111111
	mask = mask ^ bit_mask

	# start an undo group
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	pdb.gimp_image_convert_rgb(image)
	my_flattened_layer = pdb.gimp_image_flatten(image)

	bytes_pp = my_flattened_layer.bpp
	# print "Bytes_pp" + str(bytes_pp)

	# All of the pixel region logic is from:
	# https://github.com/akkana/gimp-plugins/blob/master/arclayer.py

	# create a new destination layer
	layername = "mpf flattened"
	destDrawable = gimp.Layer(image, layername, image.width, image.height, \
							my_flattened_layer.type, my_flattened_layer.opacity, my_flattened_layer.mode)

	# add destination layer to image
	image.add_layer(destDrawable, 0)

	# create a source pixel region on the origional layer(drawable), False-False
	# Need to set the last two parameters to False for the Source Pixel Region (https://www.gimp.org/docs/python/#PREGION-OBJECT)
	# 	dirty - Non zero if changes to the pixel region will be reflected in the drawable.
	#   shadow - Non zero if the pixel region acts on the shadow tiles of the drawable.
	srcRgn = my_flattened_layer.get_pixel_rgn(0, 0, image.width, image.height, False, False)

	# create an array from the source pixel region
	# create an array of unsigned integer of size 1 byte as big as the image
	src_pixels = array("B", srcRgn[0:image.width, 0:image.height])

	# create a destination pixel region on destination layer, True-True
	dstRgn = destDrawable.get_pixel_rgn(0, 0, image.width, image.height, True, True)

	# create and initialize to x00 destination array for destination pixels
	p_size = len(srcRgn[0,0])               
	dest_pixels = array("B", "\x00" * (image.width * image.height * p_size))

	# loop over the source pixel region to
	for i in range(0, len(dest_pixels) - 1):
		# use that mask to drop the low order bits
		dest_pixels[i] = src_pixels[i] & mask
		# print i, src_pixels[i], dest_pixels[i]

	# Set the destination pixel region to the destionation array
	dstRgn[0:image.width, 0:image.height] = dest_pixels.tostring() 

	# Flush and merge the destination layer
	destDrawable.flush()
	destDrawable.merge_shadow(True)

	# Set the source layer to invisible
	my_flattened_layer.visible = False

	# change brightness and contrast
	pdb.gimp_brightness_contrast(destDrawable, int(brightness), int(contrast))

	# update the layer
	destDrawable.update(0, 0, image.width, image.height)
	
	# wrap up and end undo group
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
"""
https://gitlab.gnome.org/GNOME/gimp/-/blob/gimp-2-10/plug-ins/pygimp/gimpfu.py
def register(proc_name, blurb, help, author, copyright, date, label,
             imagetypes, params, results, function,
             menu=None, domain=None, on_query=None, on_run=None):

"""
register(
	"python_fu_mp_filtered_view", 
	"Matrix Portal filtered view", 
	"Simulate the image display on an RGB LED Display via a Matrix Portal", 
	"CHF", 
	"CHF", 
	"Dec 2020", 
	"RGB LED simulated view",
	"*",      # Create a new image, don't work on an existing one
	[ 
	#INPUT BEGINS
	(PF_IMAGE, "image", "takes current image", None),
	#(PF_DRAWABLE, "drawable", "Input layer", None),
	(PF_SPINNER, "brightness", "Brightness:", 120, (-127, 127, 1)),
	(PF_SPINNER, "contrast", "Contrast:", 114, (-127, 127, 1)),
	# (PF_SPINNER, "bpp", "Bits per Pixel", 6, (2, 6, 1))
	(PF_RADIO, "bpp", "Bits per Pixel", "6",
		(
			("6", "6"),
			("5", "5"),
			("4", "4"),
			("3", "3"),
			("2", "2")
		)
	)
	#INPUT ENDS
	],
	[],
	mp_filtered_view, menu="<Image>/Python-Fu")

main()
