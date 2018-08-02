import PyPDF2
import regex as re
from bs4 import BeautifulSoup
import urllib2

def downdata():
    url = "http://ggsipu.ac.in/ExamResults/ExamResultsmain.htm"
    page = urllib2.urlopen(url)
    sop = BeautifulSoup(page,'lxml')
    print("enter branch(MET/ME/EE/ENE/EEE/PE/MAE/Civil/IT/ICE/ECE/CSE)")
    branch = "("+raw_input()+")"
    print("enter semester(1/2/3/4/5/6/7/8)")
    sem_no = int(raw_input())
    semester_Codes = ["0th","1st","2nd","3rd","4th","5th","6th","7th","8th"]
    sem = semester_Codes[sem_no]+" Sem"
    hh = []
    for i in sop.find_all('td'):                #finding specific result from pool of results
        try:
            content = i.a.contents[0]
            links = "http://ggsipu.ac.in/ExamResults/"+i.a['href']
            if branch in content:
                if sem in content:
                    hh.append([links,content])
                    break
        except:
            continue
    if len(hh) != 0:                  
        filedata = urllib2.urlopen(hh[0][0])        #downloading pdf from ip site
        datatowrite = filedata.read()
        with open('data.pdf', 'wb') as f:
            f.write(datatowrite)
    else:
        print("\n\nRESULT NOT FOUND!\n\n")
    




def beautiy(xdata):
    with open('data.txt', 'wb') as f:
        f.write(xdata)
    #print(xdata)
    bregex = re.compile(r'([0-9]{5,6})\(\d\)\n (\d\d)  (\d\d) \n(\d\d)')      #Reg exp for better readability
    bregex1 = re.compile(r'([0-9]{5,6})\(\d\)\n(-) (\d\d) \n(\d\d)')
    bregex2 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d\d) (-)\n(\d\d)')
    bregex3 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d\d)  (\d\d)\n (\d\d) ')
    bregex4 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d)  (\d\d) \n(\d\d)')
    bregex5 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d\d) (A)\n(A)')
    bregex6 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d\d)  (\d)\n (\d\d)')
    bregex7 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d)  (\d)\n (\d)')
    bregex8 = re.compile(r'([0-9]{5,6})\(\d\)\n (\d) (A)\n(A)')
    allx = bregex.findall(xdata)+bregex1.findall(xdata)+bregex2.findall(xdata)+bregex3.findall(xdata)
    allx = allx+bregex4.findall(xdata)+bregex5.findall(xdata)+bregex6.findall(xdata)+bregex7.findall(xdata)+bregex8.findall(xdata)
    
    nameregex = re.compile(r'[0-9]{11}\n\n([A-Z]{0,})\n')
    nameregex1 = re.compile(r'[0-9]{11}\n\n([A-Za-z]{0,} [A-Za-z]{0,})\n')
    nameregex2 = re.compile(r'[0-9]{11}\n\n([A-Z]{0,} [A-Z]{0,} [A-Z]{0,})\n')
    nameregex3 = re.compile(r'[0-9]{11}\n\n([A-Z]{0,} [A-Z]{0,})\n\nSID')

    name = nameregex.findall(xdata)+nameregex2.findall(xdata)+nameregex2.findall(xdata)+nameregex3.findall(xdata)

    try:
        print "\n\nNAME :",name[0]
    except:
        print " NAME CANNOT BE EXTRACTED"

    print("\nRESULT\n")
    print '{0:10s} {1:10s} {2:10s} {3:10s}'.format("Sub Code","Inter","Extr","Total")
    avg = 0
    for i in allx:
        if i[3]!="A":
            avg += float(i[3])
        print '{0:10s} {1:10s} {2:10s} {3:10s}'.format(i[0],i[1],i[2],i[3])
    print("\n")
    try:
        print "semester % = ", avg/len(allx)
    except:
        print "ERROR!!!"

print("Do You want to download result file again?(y/n)")
ch=raw_input()
if ch == 'y':
    downdata()  

X = 'y'
while(X == 'y'):
    rollNumRegex = re.compile(r'\n([0-9]{11})\n')
    
    pdfFileObj = open('data.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)            #reading pdf
    print("\n\nenter roll no:-")
    rollno = raw_input().encode('utf-8')
    i = 0
    for i in range(pdfReader.numPages):                     #traversing pdf pages
        data = pdfReader.getPage(i).extractText().encode('utf-8')
        allist = rollNumRegex.findall(data)                           #finding all roll nos
    
        if rollno not in allist:
            if i == pdfReader.numPages-1:
                print("\n\n***Sorry Roll no not found!***\n\n")
            continue
        else:
            try:
                spos = data.find(rollno)                          #finding specific roll no.
                fpos = data.find(allist[allist.index(rollno)+1])
                beautiy(data[spos:fpos])
                break
            except:
                spos = data.find(rollno)
                beautiy(data[spos:])
                break
    print("\n\nCheck another roll no :(y/n)")
    X = raw_input()

