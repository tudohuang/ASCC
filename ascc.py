import os
import time
import threading
import curses
from PIL import Image, ImageSequence
from moviepy.editor import VideoFileClip
import numpy as np
import argparse

def display_ascii_animation(stdscr, path, width=100, sec=0.1):
    try:
        if width <= 300:
            # Initialize curses
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            stdscr.attron(curses.color_pair(1))

            def image_to_ascii(image):
                img_width, img_height = image.size
                ratio = img_height / img_width / 1.65
                height = int(width * ratio)
                image = image.resize((width, height))
                pixels = image.getdata()
                grayscale_characters = "@%#*+=-:. "
                ascii_art = ""

                for pixel_value in pixels:
                    ascii_art += grayscale_characters[(pixel_value // 25) % len(grayscale_characters)]

                ascii_art_len = len(ascii_art)
                ascii_img = ""

                for i in range(0, ascii_art_len, width):
                    ascii_img += ascii_art[i:i+width] + "\n"

                return ascii_img

            # Determine if it's a GIF or MP4
            file_extension = os.path.splitext(path)[-1].lower()
            last_ascii_art = None

            if file_extension == '.gif':
                try:
                    gif = Image.open(path)
                except Exception as e:
                    raise ValueError(f"Failed to open image at {path}: {e}")

                # Loop through GIF frames
                for ii in range(20):  # Loop 20 times to simulate a longer animation
                    for index, frame in enumerate(ImageSequence.Iterator(gif)):
                        if (index + 1) % 2 != 0:
                            gray_frame = frame.convert("L")
                            ascii_art = image_to_ascii(gray_frame)

                            if ascii_art != last_ascii_art:
                                stdscr.clear()
                                stdscr.addstr(0, 0, ascii_art)
                                stdscr.refresh()
                                last_ascii_art = ascii_art

                            time.sleep(sec)

            elif file_extension == '.mp4':
                clip = VideoFileClip(path)
                duration = clip.duration

                if duration < 300:  # Less than 5 minutes
                    for frame in clip.iter_frames(fps=24, dtype='uint8'):
                        frame_image = Image.fromarray(frame, 'RGB').convert("L")
                        ascii_art = image_to_ascii(frame_image)

                        if ascii_art != last_ascii_art:
                            stdscr.clear()
                            stdscr.addstr(0, 0, ascii_art)
                            stdscr.refresh()
                            last_ascii_art = ascii_art

                        time.sleep(sec)
                else:
                    raise ValueError("Video is too long to convert to ASCII animation.")
            else:
                raise ValueError("Unsupported file format. Only GIF and MP4 are supported.")
        #else:
            #print(Fore.RED + "ERROR: Width is too large." + Fore.RESET)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # This ensures that curses mode is properly shut down
        curses.endwin()

# To run the function in a terminal that supports curses
def ascii_display(path, width, sec):
   curses.wrapper(display_ascii_animation, path, width, sec)

#ascii_display("C:\\Users\\tudo\\Downloads\\006yt1Omgy1h6gxpxly28g30hs0a0qv6.gif", 100,0.01)

def main():
    parser = argparse.ArgumentParser(description='ASCII Art Display')
    parser.add_argument('-p', '--path', type=str, required=True, help='Path to the image or video file')
    parser.add_argument('-w', '--width', type=int, default=100, help='Width of the ASCII art')
    parser.add_argument('-s', '--sec', type=float, default=0.1, help='Seconds between frames')

    args = parser.parse_args()

    ascii_display(args.path, args.width, args.sec)

if __name__ == "__main__":
    main()




