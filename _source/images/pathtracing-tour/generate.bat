@echo off
del *.png
post1.exe -output image1-1.png -image_index 0 -width 1024 -height 768 -samples 4
post1.exe -output image1-2.png -image_index 1 -width 1024 -height 768 -samples 4
post2.exe -output image2-1.png -image_index 0 -width 1024 -height 768 -samples 16
post3.exe -output image3-1.png -image_index 0 -width 1024 -height 768 -samples 16
post4.exe -output image4-1.png -image_index 0 -width 1024 -height 768 -samples 16