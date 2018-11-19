import sys
import time
import webbrowser
from jinja2 import Environment, PackageLoader

def parse(FTP,fn):
    dataSection = False
    headerSection = False
    lastTime = 0    #if first, set to current
    currentTime = 0
    deltaUpCount = 0
    ergList = []
    secPerMin = 60
    #secPerMin = 1

    with open(fn) as f:
        for i in f:
            if "[COURSE HEADER]" in i:
                headerSection = True
            elif "[END COURSE HEADER]" in i:
                headerSection = False
            elif "[COURSE DATA]" in i:
                dataSection = True
            elif "[END COURSE DATA]" in i:
                dataSection = False
            else:
                if headerSection:
                    pass
                if dataSection:
                    currentTime,y = i.split()
                    deltaTime = int(currentTime)-int(lastTime)
                    ergList.append([int(currentTime)*secPerMin,int((float(y)/100.0*FTP))])
                    lastTime = currentTime

    env = Environment(autoescape=False, optimized=False)
    with open("flot.template", "r") as f:
      template = env.from_string(f.read())
    with open("flot.html", "w") as f:
      template.stream(
        ergList = ergList,
        power=FTP
      ).dump(f)

#cmdline or OS open with parse file input

if __name__ == '__main__':
    FTP = 200       #get FTP from user/cmdline
    filename = "1 hour with 5 min intervals.erg"
    if len(sys.argv[1]):
        filename = sys.argv[1]

    parse(FTP,filename)

    webbrowser.open_new_tab('flot.html')
