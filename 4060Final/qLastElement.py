import cx_Oracle
def queryLastElement():
    con = cx_Oracle.connect('arushi/harkersoftball')
    cur=con.cursor()

    obj = cur.execute('''select * from beeGenes where ref_num=147907436''')
    for x in obj:
        print(x)
        print(x[1].read())


    cur.close()
    con.close()

queryLastElement()
