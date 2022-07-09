import cgi
import cx_Oracle

def main():
    form=cgi.FieldStorage()
    theStr = form.getfirst('theList', '')
    contents = processInput(theStr)
    print(contents)

def processInput(theFile):
    #g) connect to oracle database system
    con = cx_Oracle.connect('arushi/[redacted]')
    cur = con.cursor()

    #a) Read in the contents of the data file.
    infile = open(theFile, 'r')
    myStr = ""
    finalStr = ""

    #b) insert string where each nucleotide starts
    #myStr contains the file line by line
    for aline in infile:
        hold = aline
        if'mRNA' in hold or 'cds' in hold or 'mitochondrial' in hold:
            #find index of that string
            hold = hold + "_**gene_seq_starts_here**_"        
        myStr = myStr + hold

    
    splitGene = myStr.split('>')
    splitGene = splitGene[1:]

    #arrays that store all the stats for comparison
    ref_nums = []
    gene_codes = []
    a_freqs = []
    c_freqs = []
    g_freqs = []
    t_freqs = []
    gc_freqs = []
    
    #h) create a table to store facts
    cur.execute('drop table beeGenes')
    cur.execute('''create table beeGenes (
        ref_num varchar2(10), 
        sequence clob,
        freq_A number, 
        freq_C number,
        freq_G number,
        freq_T number,
        freq_GC number
        )''')

    
    #input sizes come from the max gene length python script, also attached
    cur.bindarraysize = 50
    cur.setinputsizes(10, 14648, float, float,  float,  float,  float)


    for gene in splitGene:
        start = 3 #'gi|ref number|...'
        ref_end = gene.index('|', 3) 
        ref_num = gene[start:ref_end]
        
        g_start = gene.find('**_') + 3
        gene_code = gene[g_start:]

        gene_code = gene_code.replace('\n', '')

        #e) calc freq of nucl in every gene
        g_len = len(gene_code)
        freq_A = gene_code.count('A')/float(g_len)
        freq_C = gene_code.count('C')/float(g_len)
        freq_G = gene_code.count('G')/float(g_len)
        freq_T = gene_code.count('T')/float(g_len)
        freq_GC = freq_C + freq_G

        a_freqs.append(freq_A)
        c_freqs.append(freq_C)
        g_freqs.append(freq_G)
        t_freqs.append(freq_T)
        ref_nums.append(ref_num)
        gene_codes.append(gene_code)

        #f) calc freq_GC
        gc_freqs.append(freq_GC)

        #insert stats into the beeGenes table
        cur.execute('''insert into beeGenes (ref_num, sequence, freq_A, freq_C, freq_G, freq_T, freq_GC) 
        values(:v1, :v2, :v3, :v4, :v5, :v6, :v7) ''', (ref_num, gene_code, freq_A, freq_C, freq_G, freq_T, freq_GC))

        con.commit()

    cur.close()
    con.close()

    return makePage("donesub.html", ("Thank you for uploading."))

def fileToStr(fileName):
    """Return a string containing the contents of the named file."""
    fin = open(fileName) 
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, subs):
    #make the page given a template (kompozer), blanks for substitutions
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate %subs

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()
