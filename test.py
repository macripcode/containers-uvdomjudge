import json
import MySQLdb
from time import sleep

host = '127.0.0.1'
usuario_bd = 'macripco'
pass_usuario_db = '12345'
port = 32768
data = {}


try:
    conn = MySQLdb.connect(host=host, port=port, user=usuario_bd, passwd=pass_usuario_db, db='domjudge')
    # Details
    data['contests'] = []
    # -------Adding all contest---->
    cur = conn.cursor()
    cur.execute("select cid, name, endtime_string from contest;")
    row = cur.fetchone()
    while row is not None:
        cur1 = conn.cursor()
        cur1.execute(
            "select contestproblem.probid , problem.name from contestproblem, problem where problem.probid = contestproblem.probid and contestproblem.cid = " + str(
                row[0]) + ";")
        problems = []
        row1 = cur1.fetchone()
        while row1 is not None:
            problems.append(row1)
            row1 = cur1.fetchone()
        data['contests'].append((row[0], row[1], row[2], problems))
        row = cur.fetchone()
    # ------- End Adding all contest---->

    # Statistics
    data['number_of_attempts'] = []
    # --------get total number of students-------------------------------->
    #
    cur3 = conn.cursor()
    cur3.execute("select count(teamid) from team where categoryid=3;")
    row3 = cur3.fetchone()
    number_of_students = int(row3[0])
    cur3.close()


    # -------Adding all number of attemps by problems in each contest---->
    cur.execute("select cid from contest;")
    row = cur.fetchone()
    # por cada contest
    while row is not None:
        cur1 = conn.cursor()
        cur1.execute(
            "select contestproblem.probid, problem.name from contestproblem, problem where contestproblem.cid =" + str(
                row[0]) + " and contestproblem.probid = problem.probid;")
        row1 = cur1.fetchone()
        # por cada problema
        while row1 is not None:
            cur2 = conn.cursor()
            cur2.execute(
                "select count(teamid), submissions from scorecache_jury where scorecache_jury.probid = " + str(
                    row1[0]) + " group by submissions;")
            row2 = cur2.fetchone()
            attemps = []

            cur4 = conn.cursor()
            cur4.execute("select count(distinct teamid) from scorecache_jury where probid = " + str(row1[0]) + ";")
            row4 = cur4.fetchone()
            number_of_submissions = int(row4[0])
            cur4.close()


            while row2 is not None:
                attemps.append(row2)
                row2 = cur2.fetchone()

            data['number_of_attempts'].append(
                (row[0], row1[0], row1[1], attemps, (number_of_submissions, number_of_students)))
            cur2.close()
            row1 = cur1.fetchone()
        cur1.close()
        row = cur.fetchone()
    cur.close()

    # --------Getting list of student---------------->
    # list
    data['list'] = []
    cur = conn.cursor()
    cur.execute("select teamid, name from team where categoryid = 3 order by name;")
    row = cur.fetchone()
    while row is not None:
        data['list'].append((row[0], row[1]))
        row = cur.fetchone()
    cur.close()
    # --------Getting list of students---------------->

    # --------Getting evaluations---------------->
    data['evaluation'] = []
    for contest in data['contests']:
        for problem in contest[3]:
            eval = []
            cur1 = conn.cursor()
            for student in data['list']:
                print(student)

                res = cur1.execute("select scorecache_jury.cid, \
                                           scorecache_jury.probid,\
                                           team.id, \
                                           scorecache_jury.is_correct \
                                    from   scorecache_jury, \
                                           team \
                                     where scorecache_jury.cid = " + str(contest[0]) + " and \
                                           scorecache_jury.probid = " + str(problem[0]) + " and \
                                           scorecache_jury.teamid = 201740801 and \
                                           scorecache_jury.teamid = team.teamid")

                print(res)

            #     if res == 0:
            #         eval.append((0))
            #     else:
            #         row1 = cur1.fetchone()
            #         if row1[4] == 0:
            #             eval.append((0))
            #         elif row1[4] == 1:
            #             eval.append((5))
            #
            # data['evaluation'].append((contest[0], problem[0], eval))

    # -----Adding evaluations
    conn.commit()
    conn.close()

    #print (data)


except MySQLdb.Error as e:
    data['error'] = e