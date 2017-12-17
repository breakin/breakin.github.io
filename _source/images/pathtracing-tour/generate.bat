@echo off
del *.png
post1.exe -output image1-1.png -image_index 0 -width 1600 -height 1200 -samples 4
post1.exe -output image1-2.png -image_index 1 -width 1600 -height 1200 -samples 4
post2.exe -output image2-1.png -image_index 0 -width 1600 -height 1200 -samples 16
post2.exe -output image2-2.png -image_index 0 -width 1600 -height 1200 -samples 256
post3.exe -output image3-1.png -image_index 0 -width 1600 -height 1200 -samples 16
post4.exe -output image4-1.png -image_index 0 -width 1600 -height 1200 -samples 16
post5.exe -output image5-1.png -image_index 0 -width 1600 -height 1200 -samples 16
post5.exe -output image5-2.png -image_index 0 -width 1600 -height 1200 -samples 256