# GIMP-Plugins
This project is for any GIMP Python Fu Plugins that might be created. 

## MatrixPortal_filtered_view

This plugin simulates the display of the image on the Martix Portal. The pixels in the image are truncated supposing the references to RGB565 in the code means the lower order bit are just dropped. There is a selection for the bits per pixel setting in the MatrixPortal() object creation.
Additionally, there is a brightness and contrast filter added to more closely match the perceptual quality of the image. The defaults were selected based on some samples viewed.

The plugin registation signature will add a Menu item **Python-Fu**, under that is **RGB LED simulated view** item.

Always undo (CTRL+Z) after viewing the results.

To install, you need to copy the Python script to the correct folder as per the GIMP configuration. Look for the path in GIMP using  Edit-Preferences-Folders-Plugins

It might have an entry like for Windows:

`C:\Users\{your username}\AppData\Roaming\GIMP\2.10\plug-ins`

# Acknowledgements
This is mostly based on information from [https://gimpbook.com](https://gimpbook.com) and [Gimp Scripting Python Fu by Jackson Bates](https://www.youtube.com/c/JacksonBates). There is also good info at [https://www.gimp.org/docs/python/index.html](https://www.gimp.org/docs/python/index.html).
