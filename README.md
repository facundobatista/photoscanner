# photoscanner

Script to automate the scanning of "old printed photos"

Just run:

```
   ./scan_photos.py 
```

The script is prepared to be run by `fades`. Otherwise prepare the proper virtualenv or whatever, dependencies are `numpy` and `opencv-python`.

It will ask you to put photos in the scanner, press Enter, and it will scan them, cut them and save them as JPEG images. 

That's all you normally need. But if you see that any photo perimeter was not correctly recognized, before changing the photos press `R` and it will scan again but will save the raw scanned image (then you could manually process it, I recommend to use `gimp`).
