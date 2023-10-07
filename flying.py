import os
import time
import sys

plane_frames_default = [
    r"       __ __",
    r"         |",
    r"--o--o--( _ )",
    r"        -|-"
]

def clear_screen():
    os_name = sys.platform.lower()
    if os_name.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def flying(plane_picture=''):
    if plane_picture:
        plane_frames = plane_picture.split('\n')
    else:
        plane_frames = plane_frames_default
    width, height = os.get_terminal_size()
    plane_length = max(map(len, plane_frames))
    animation_speed = 0.01

    for frame in range(0, width - plane_length + 1, 2):
        clear_screen()
        for line in plane_frames:
            print(" " * frame + line)
        time.sleep(animation_speed)
    clear_screen()


def main():
    flying()

if __name__ == "__main__":
    main()
