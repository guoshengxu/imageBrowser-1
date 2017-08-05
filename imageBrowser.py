#!/usr/bin/python3

import os, errno, re, subprocess

for dir in["thumbs", "pages"]:
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

regex = re.compile("^.+\.(jpg|png|gif)$")
images = list(filter(regex.match, sorted(os.listdir("."))))

with open("templates/pageTemplate.html", "r") as file:
    pageTemplate = file.read()
with open("templates/indexTemplate.html", "r") as file:
    indexTemplate = file.read()

thumbs = ""

for i in range(0, len(images)):
    with open("pages/image{}.html".format(i), "w+") as file:
        if i == 0:
            prev = 0
            next = i + 1
        elif i == len(images) - 1:
            prev = i - 1
            next = i
        else:
            prev = i - 1
            next = i + 1

        file.write(pageTemplate
                .format(0, prev, next, len(images) - 1, images[i]))

    subprocess.call("convert {} -resize '100' thumbs/thumb{}.gif"
            .format(images[i], i), shell=True)

    thumbs += ("<a href=pages/image{0}.html>\n"
               "<img src=thumbs/thumb{0}.gif>\n"
               "</a>").format(i)

with open("index.html", "w+") as file:
    file.write(indexTemplate.format(thumbs))

