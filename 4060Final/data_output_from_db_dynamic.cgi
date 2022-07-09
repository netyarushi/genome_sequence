import cgi
import cx_Oracle

def main():
    contents = processInput()
    print(contents)

def processInput():
    con = cx_Oracle.connect('arushi/harkersoftball')
    cur=con.cursor()
    aaList = ['A', 'C', 'G', 'T']
    gis = []
    fList = []

    #selects the max frequency from the array, also retrieves corresponding gene id
    for i in range(4):
        myDict = {'aa':aaList[i]}
        obj = cur.execute('''select ref_num, freq_%(aa)s from beeGenes, (select max(freq_%(aa)s) as max%(aa)s from beeGenes) where freq_%(aa)s=max%(aa)s''' % myDict)

        #since could be more than one gene with highest freq, grab all of them 
        for x in obj:
            #append the gene identifier
            gis.append(x[0])

            #append the max frequency
            fList.append(x[1])
        
    #found that there are 5 genes with the max freq for thymine, so have 5 blanks on the template and replace them here
    fList = fList[:4] 
    myTuple = (gis[0], fList[0],gis[1], fList[1],gis[2], fList[2], gis[3], gis[4], gis[5], gis[6], gis[7], fList[3])


    cur.close()
    con.close()

    return makePage('bee_res.html', myTuple)
    
'''fileToStr and makePage are the same functions as the other'''

def fileToStr(fileName):
    fin = open(fileName);
    contents = fin.read();
    fin.close()
    return contents


def makePage(templateFileName, subs):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % subs

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()