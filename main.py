#importing functions
from GUI import browse_files

#uploading textbook excerpt and slides
textbook, slides = browse_files()
print("Textbook Path:", textbook)
print("Slides Path:", slides)
