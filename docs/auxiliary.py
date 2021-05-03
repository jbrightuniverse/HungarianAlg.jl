import os
os.system("pip install numpy")
os.system("pip install Pillow")

import numpy as np

from base64 import b64encode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def baserender(matrix, rpotentials, cpotentials, equality = False, paths = [], terminus = [], matching = [], highlight = [], hpath = None):
    # Keep OpenSansEmoji.ttf in the same folder as the notebook; 
    #      this is available in the algorithm's repo alongside this notebook

    frames = []

    for path in paths:
        path.reverse()

    matrix = np.array(matrix)
    msize = matrix.shape[0]
    font = ImageFont.truetype("OpenSansEmoji.ttf", 40)
    font3 = ImageFont.truetype("OpenSansEmoji.ttf", 20)

    img = Image.new("RGBA", (400, 300), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)

    singular = d.textsize("000", font = font)
    del img
    singular_width = singular[0] + 2
    singular_height = singular[1] + 2
    matrix_width = msize * singular_width
    matrix_height = msize * singular_height
    wide = singular[0]
    theotherone = [1]
    kmidpoint_x = None
    kmidpoint_y = None
    kmidpoint_x2 = None

    if len(terminus) != 0:
        pathpair = terminus
        for match in matching:
            if match[0] == pathpair[0] and match[1] != pathpair[1]:
                break
        else:
            match = [0, -0.5]

        kmidpoint_x = int(wide + (match[1] + 0.5) * singular_width)
        kmidpoint_x2 = int(wide + (pathpair[1] + 0.5) * singular_width)
        kmidpoint_y = int((pathpair[0] + 1.5) * singular_height)
        
        if kmidpoint_x2 > kmidpoint_x:
            step = 5
        else:
            step = -5

        theotherone = [(a, 0) for a in list(range(kmidpoint_x, kmidpoint_x2, step))] + [(a, 1) for a in list(range(kmidpoint_y, singular_height, -5))]
    for iteration in theotherone:
        img = Image.new("RGBA", (400, 300), (255, 255, 255, 255))
        d = ImageDraw.Draw(img)

        if equality:
            # render full equality graph
            for i in range(msize):
                for j in range(msize):
                    if rpotentials[i] + cpotentials[j] == matrix[i, j]:
                        up = (i + 1) * singular_height
                        left = wide + (j) * singular_width
                        d.rectangle((left, up, left + singular_width, up + singular_height), fill = (42, 222, 216, 255), outline = (42, 222, 216, 255))

        if len(matching) != 0:
            for entry in matching:
                up = (entry[0] + 1) * singular_height
                left = wide + (entry[1]) * singular_width
                d.rectangle((left, up, left + singular_width, up + singular_height), fill = (136, 255, 136, 255), outline = (136, 255, 136, 255))

        if len(highlight) != 0:
            up = (hpath[0] + 1) * singular_height
            left = wide + (hpath[1]) * singular_width
            d.rectangle((left, up, left + singular_width, up + singular_height), fill = (207, 123, 237, 255), outline = (207, 123, 237, 255))

        for i in range(msize + 1):
            d.line((wide, (i+1) * singular_height, matrix_width + wide, (i+1) * singular_height), fill = (0, 0, 0, 255))
            d.line((wide + i * singular_width, singular_height, wide + i * singular_width, singular_height + matrix_height), fill = (0, 0, 0, 255))

        if paths != None:
            # render all alternating paths

            redcircles = []
            circles = []
            for path in paths:
                midpoint_y = (path[0] + 1.5) * singular_height
                midpoint_x = wide
                redcircles.append((midpoint_x, midpoint_y))
                last_coord = wide

                first_is_row = 1
                for i in range(len(path) - 1):
                    if first_is_row:

                        midpoint_x = last_coord
                        midpoint_x2 = wide + (path[i+1] + 0.5) * singular_width
                        midpoint_y = (path[i] + 1.5) * singular_height
                        d.line((midpoint_x, midpoint_y, midpoint_x2, midpoint_y), fill = (245, 161, 66, 255), width = 3)
                        circles.append((midpoint_x2, midpoint_y))

                        last_coord = midpoint_y

                    else:

                        midpoint_y = last_coord
                        midpoint_y2 = (path[i+1] + 1.5) * singular_height
                        midpoint_x = wide + (path[i] + 0.5) * singular_width

                        d.line((midpoint_x, midpoint_y, midpoint_x, midpoint_y2), fill = (245, 161, 66, 255), width = 3)
                        circles.append((midpoint_x, midpoint_y2))

                        last_coord = midpoint_x

                    first_is_row = 1 - first_is_row

            if len(terminus) != 0:
                if iteration[1] == 0:
                    first = iteration[0]
                    second = kmidpoint_y
                else:
                    circles.append((kmidpoint_x2, kmidpoint_y))
                    first = kmidpoint_x2
                    second = iteration[0]
                d.line((kmidpoint_x, kmidpoint_y, first, kmidpoint_y), fill = (245, 161, 66, 255), width = 3)
                d.line((kmidpoint_x2, kmidpoint_y, kmidpoint_x2, second), fill = (245, 161, 66, 255), width = 3)
                redcircles.append((kmidpoint_x2, singular_height))

            scl = 5
            for circle in circles:
                midpoint_x, midpoint_y = circle
                col = (0, 0, 255, 255)
                d.ellipse([(midpoint_x - scl, midpoint_y - scl), (midpoint_x + scl, midpoint_y + scl)], fill=col, outline=col)

            for circle in redcircles:
                midpoint_x, midpoint_y = circle
                col = (255, 0, 0, 255)
                d.ellipse([(midpoint_x - scl, midpoint_y - scl), (midpoint_x + scl, midpoint_y + scl)], fill=col, outline=col)

        for i in range(msize):
            d.text((20, (i+1) * singular_height + 10), str(rpotentials[i]), fill = [(0, 0, 0, 255), (35, 217, 74, 255)][int(len(highlight) != 0 and i in highlight[0])], font = font3)
            d.text((wide + i * singular_width + 20, 10), str(cpotentials[i]), fill = [(0, 0, 0, 255), (35, 217, 74, 255)][int(len(highlight) != 0 and i in highlight[1])], font = font3)

            for j in range(msize):
                d.text((wide + j * singular_width, (i+1) * singular_height), str(matrix[i, j]), fill = (0, 0, 0, 255), font = font3)

        if len(terminus) != 0:
            frames.append(img)
        
    filex = BytesIO()
    if len(terminus) == 0:
        img.save(filex, "PNG")
    else:
        copy = frames[-1]
        for i in range(20):
            frames.append(copy)
        frames[0].save(fp=filex, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
    
    return "<img style='width: 300px;' src='data:image/{1};base64,{0}'/>".format(b64encode(filex.getvalue()).decode('utf-8'), ['png', 'gif'][len(terminus) != 0])