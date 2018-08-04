import json
import MySQLdb

host = '127.0.0.1'
usuario_bd = 'macripco'
pass_usuario_db = '12345'
port = 32768

data = {}

try:

    conn = MySQLdb.connect(host=host, port=port, user=usuario_bd, passwd=pass_usuario_db, db='domjudge')

    data = {}

    # Details
    data['contests'] = []
    # -------Adding all contest---->
    cur = conn.cursor()
    cur.execute("select cid, name, endtime_string from contest;")
    row = cur.fetchone()
    while row is not None:
        cur1 = conn.cursor()
        cur1.execute( "select contestproblem.probid , problem.name from contestproblem, problem where problem.probid = contestproblem.probid and contestproblem.cid = "+str(row[0])+";")
        problems = []
        row1 = cur1.fetchone()
        while row1 is not None:
            problems.append(row1)
            row1 = cur1.fetchone()
        data['contests'].append((row[0],row[1],row[2],problems))
        row = cur.fetchone()
    # ------- End Adding all contest---->

    # Statistics
    data['number_of_attempts'] = []
    # -------Adding all number of attemps by problems in each contest---->
    cur.execute("select cid from contest;")
    row = cur.fetchone()
    #por cada contest
    while row is not None:
        cur1 = conn.cursor()
        cur1.execute("select probid from contestproblem where contestproblem.cid ="+str(row[0])+";")
        row1 = cur1.fetchone()
        #por cada problema
        while row1 is not None:
            cur2 = conn.cursor()
            cur2.execute("select count(teamid), submissions from scorecache_jury where scorecache_jury.probid = "+str(row1[0])+" group by submissions;")
            row2 = cur2.fetchone()
            attemps =[]
            while row2 is not None:
                attemps.append(row2)
                row2 = cur2.fetchone()

            data['number_of_attempts'].append((row[0], (row1[0], attemps )))
            cur2.close()
            row1 = cur1.fetchone()
        cur1.close()
        row = cur.fetchone()

    cur.close()
    conn.commit()
    conn.close()

    print (data)


except MySQLdb.Error as e:
    data['error'] = e

#return json.dumps(data)