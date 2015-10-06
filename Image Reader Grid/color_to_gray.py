
# A short Python program to convert an input image, which
# may be in color, to a grayscale PNG image.

import Image
import sys
import os

if len(sys.argv) == 2:
    input_file = sys.argv[1];
    path_without_ext, ext = os.path.splitext(input_file)
    input_filename = os.path.basename(path_without_ext)
    out_file = input_filename + '_BW.png'

    try:
        in_image = Image.open(input_file)
    except IOError, e:
        print e
        sys.exit(1);
    except:
        print "Unexpected error reading file", file
        sys.exit(1);

    out_image = in_image.convert("L");

    try:
        # Write the image
        out_image.save(out_file, "PNG")
    except IOError, e:
        print e
    except:
        print "Unexpected error writing file", file
    
else:
    print "Usage: color_to_gray.py <input_file>"
