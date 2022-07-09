import cx_Oracle

def find_max_len(gene_seq_list):
    max = 0
    for i in gene_seq_list:
        if len(i) > max:
            max = len(i)
    return max

con = cx_Oracle.connect('arushi/harkersoftball')
cur = con.cursor()

#a) Read in the contents of the data file.
infile = open(r'C:\Users\netyarushi\Documents\honeybee_gene_sequences.txt', 'r')
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

ref_nums = []
gene_codes = []



for gene in splitGene:
    #c) extract the gi number
    start = 3 #'gi|ref number|...'
    ref_end = gene.index('|', 3) 
    ref_num = gene[start:ref_end]
        
    g_start = gene.find('**_') + 3
    gene_code = gene[g_start:]

    ref_nums.append(ref_num)
    gene_codes.append(gene_code)


print("The max length of a gene is ", find_max_len(gene_codes))

cur.close()
con.close()
