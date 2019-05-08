#!/usr/bin/env python3
import cgi
import cgitb
from os.path import join as pathjoin, basename, dirname, expanduser
cgitb.enable(display=0, logdir=expanduser("~/.cgi-pdf2html/logs/"))

import subprocess
from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile
import hashlib
import os

def pdf2html(url, htmlroot="tmp", filename="temp.pdf",
             requestheaders={
                 "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0",
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                 "Accept-Language": "en-US,en;q=0.5",
                 "Content-Type": "application/x-www-form-urlencoded"
             }):
    htmldir = pathjoin(htmlroot,
                       hashlib.md5(url.encode()).hexdigest()[:3])
    subprocess.run(["rm", "-rf", htmldir])
    os.makedirs(htmldir)
    with urlopen(Request(url, headers=requestheaders)) as urlfile:
        tmpfile = pathjoin(htmldir, filename)
        with open(tmpfile, "wb") as tf:
            tf.write(urlfile.read())

        subprocess.run(["pdftohtml", basename(tmpfile)],
                        cwd=dirname(tmpfile))
        return tmpfile.replace(".pdf", ".html")

def cgimain(currpath="cgi-bin/pdf2html.py"):
    form = cgi.FieldStorage()
    if "url" not in form:
        print("Content-Type: text/html")
        print()
        print("""<html><body>
        <H1>Error</H1>
        <p>Please fill in the url field</p>.
        <form>
        <input name=url type=text" label="URL"/>
        </form>
        """)

    url = form.getvalue("url")
    htmlfile = pdf2html(url)
    print("Content-Type: text/html")
    print()
    print("""<html>
    <body>
    <a href="/{htmlfile}">Converted HTML for '{pdffile}'</a>
    <script>
    var currurl = window.location.href;
    var newurl = currurl.replace('{currpath}', '{htmlfile}');
    window.location.assign(newurl);
    </script>
    </body>
    </html>""".format(htmlfile=htmlfile, pdffile=url, currpath=currpath))



if __name__ == '__main__':
    import sys
    cgimain()

