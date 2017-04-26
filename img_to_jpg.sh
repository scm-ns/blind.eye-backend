#!/bin/bash

echo "Make sure all the images to be converted to jpg end with .img"
echo "After conversion to jpg the *.img are removed"

echo "Starting rescursive conversion of all images in the folder"
find ./ -name "*.img" -exec mogrify -format jpg {} \;

echo "Finished converting"
echo "Deleting *.img files"
find ./ -name "*.img" -exec rm {} \;

