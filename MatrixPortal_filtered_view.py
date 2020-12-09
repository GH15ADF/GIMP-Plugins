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
import sys
sys.stderr = open('c:/temp/er.txt', 'a')
sys.stdout = open('c:/temp/log.txt', 'a')
print("testing 123")

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
	
#def mp_filtered_view(image, drawable, brightness, contrast, bpp) : #FUNCTION DEFINITION
def mp_filtered_view(image, brightness, contrast, bitspp) : #FUNCTION DEFINITION
	BIT_DEPTH = int(bitspp)
	mask = 0xFF >> BIT_DEPTH
	bit_mask = 0b11111111
	mask = mask ^ bit_mask

	# start an undo group
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	pdb.gimp_image_convert_rgb(image)
	my_flattened_layer = pdb.gimp_image_flatten(image)

#	pix_region = drawable.get_pixel_rgn(0, 0, image.width, image.height, True, True)
#	px = pix_region[10,10]
	bpp, px = pdb.gimp_drawable_get_pixel(my_flattened_layer,0,0)
	print "BPP: " + str(bpp) + " Pixel value: " + str(px)
	#pdb.gimp_drawable_set_pixel(my_flattened_layer, 0, 0, bpp, (0,255,0))
	for x in range(0, my_flattened_layer.width - 1):
		for y in range(0, my_flattened_layer.height - 1):
			# get the next pixel
			bpp, px = pdb.gimp_drawable_get_pixel(my_flattened_layer,x,y)
			# do the bit per pixel bitspp trim
			r_mod = px[0] & mask
			g_mod = px[1] & mask
			b_mod = px[2] & mask
			#print "BPP: " + str(bpp) + " Old Pixel value: " + str(px) + " New Pixel value: " + str((r_mod,g_mod,b_mod))
			pdb.gimp_drawable_set_pixel(my_flattened_layer, x, y, bpp, (r_mod,g_mod,b_mod))
			
	pdb.gimp_drawable_update(my_flattened_layer, 0, 0, my_flattened_layer.width, my_flattened_layer.height)

	# adjust brightness and constrast
	# TODO: I cannot get the gimp_drawable_brightness_contrast to work so I
	# am using the depracated version
	# brightness_val = brightness/256.0
	# contrast_val = contrast/256.0
	# print "brightness_val: " + str(brightness_val) + " contrast_val: " + str(contrast_val)
	# pdb.gimp_drawable_brightness_contrast(my_flattened_layer, brightness_val, contrast_val)

	print "brightness: " + str(brightness) + " contrast: " + str(contrast)
	pdb.gimp_brightness_contrast(my_flattened_layer, int(brightness), int(contrast))
	
	pdb.gimp_drawable_update(my_flattened_layer, 0, 0, my_flattened_layer.width, my_flattened_layer.height)
	
	# end undo group
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
	(PF_SPINNER, "bpp", "Bits per Pixel", 6, (2, 6, 1))
	#INPUT ENDS
	],
	[],
	mp_filtered_view, menu="<Image>/Python-Fu")

main()
