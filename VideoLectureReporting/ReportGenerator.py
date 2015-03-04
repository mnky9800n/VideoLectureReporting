from bottle import route, run, static_file

import glob
import os

@route('/hello')
def hello():
    return "Hello World!"



def  GetGraphNames():
    os.chdir("C:\Users\Administrator\Google Drive\code learning\VideoLectureReporting\VideoLectureReporting\images\\")
    return [file for file in glob.glob("*.svg")]

def GenerateGraphDivs(GraphNames):
    os.chdir("C:\Users\Administrator\Google Drive\code learning\VideoLectureReporting\VideoLectureReporting\images\\")

    divs = ""

    for graph in GraphNames:
        divs += """
        <div>
            <object type="image/svg+xml" data="{0}">Your browser does not support SVG</object>
        </div>
        """.format(graph)

    return divs

@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root="C:\Users\Administrator\Google Drive\code learning\VideoLectureReporting\VideoLectureReporting\images", mimetype="image/svg")

#@route("/static/<filename:path>")
#def send_static(filename):
#    return static_file(filename, root="C:\Users\Administrator\Google Drive\code learning\VideoLectureReporting\VideoLectureReporting\images")

@route('/report')
def generate_report():

    GraphNames = GetGraphNames()

    for g in GraphNames:
        print send_image(g)
    
    
    #d="""<!DOCTYPE html>
    #<html>
    #<head>

    #<title>Report</title>
    #<meta charset="UTF-8">
    #<style>
    #* { color: rgba(0,0,0,1.0); }
    #</style>
    #<script>
    #'use strict';
    #</script>
    #</head>
    #<body>
    #{0}
    #</body>
    #</html>""".format(GenerateGraphDivs(GraphNames))
    #return d

run(host='localhost', port=8080, debug=True) 