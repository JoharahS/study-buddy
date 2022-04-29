import os
from tkinter import PhotoImage

from PIL import Image, ImageEnhance


class Processor():

    # Instantiated in Main constructor

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

    """
    If selected image is a GIF > Properly compose gif > save > obtain frames > write into file
    """

    def processImage(self, img_name, path):
        save_path = "./backgrounds/" + img_name
        self.controller.update_home_background(self.parent, "img", 0, save_path)
        homeBackground_file = open("homeBackground.txt", "w+")
        homeBackground_file.truncate(0)
        homeBackground_file.write("img")
        homeBackground_file.write("\n")
        homeBackground_file.write(save_path)
        homeBackground_file.write("\n")
        homeBackground_file.write(str(0))
        homeBackground_file.close()

    """
    If selected image is a GIF > Properly compose gif > save > obtain frames > write into file
    """

    def processGif(self, img_name, path):
        img = Image.open(os.path.join(path, img_name))
        frames = []
        frames.clear()
        current = img.convert('RGBA')
        enhancer = ImageEnhance.Brightness(current)
        current = enhancer.enhance(0.5)

        # Properly compose the gif so that it will update all pixels every frame, not just the ones that change.
        while True:
            try:
                frames.append(current)
                img.seek(img.tell() + 1)
                current = Image.alpha_composite(current, img.convert('RGBA'))
                enhancer = ImageEnhance.Brightness(current)
                current = enhancer.enhance(0.5)
            except EOFError:
                break

        frame_one = frames[0]
        save_path = "./backgrounds/" + img_name
        if not os.path.exists(save_path):
            frame_one.save(save_path, format="GIF", append_images=frames, save_all=True, duration=100, loop=0)

        # Obtain the correct number of frames within the gif
        num_frames = len(frames)
        while True:
            try:
                frames = [PhotoImage(file=save_path, format='gif -index %i' % (i)) for i in range(num_frames)]
                print("SUCCESS: ", str(num_frames))
                break
            except:
                print("frame count over: ", str(num_frames))
                num_frames -= 1

        # Update home screen to display the gif
        self.controller.update_home_background(self.parent, "gif", num_frames, save_path)

        # Write into file
        # Formatting by line:
        #   Save Path
        #   Number of Frames
        homeBackground_file = open("homeBackground.txt", "w+")
        homeBackground_file.truncate(0)
        homeBackground_file.write("gif")
        homeBackground_file.write("\n")
        homeBackground_file.write(save_path)
        homeBackground_file.write("\n")
        homeBackground_file.write(str(num_frames))
        homeBackground_file.close()
