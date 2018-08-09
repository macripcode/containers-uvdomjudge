from django.shortcuts import render
import os
import json
import MySQLdb
import pdb
from subprocess import Popen, PIPE
import shlex
import docker
from docker.types import Mount

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

#Cheeck de current port 80 from a running container
def get_port_80(name_container):
    response = os.popen(
        'docker inspect --format=\'{{(index (index .NetworkSettings.Ports "80/tcp") 0).HostPort}}\' ' + name_container).read().replace(
        '\n', '')

    return response

#Cheeck de current port 3306 from a running container
def get_port_3306(name_container):
    response = os.popen(
        'docker inspect --format=\'{{(index (index .NetworkSettings.Ports "3306/tcp") 0).HostPort}}\' ' + name_container).read().replace(
        '\n', '')

    return response


#Stop container with name_container
def stop_container(name_container):
    try:
        container= client.containers.get(name_container)
        container.stop()
    except 	docker.errors.APIError:
        return '500'

    return '200'


#Start container with name_container
def start_container(name_container):
    try:
        container= client.containers.get(name_container)
        container.start()
    except 	docker.errors.APIError:
        return '500'

    return '200'

#Remove container with name_container
def remove_container(name_container):
    try:
        container= client.containers.get(name_container)
        container.remove()
    except 	docker.errors.APIError:
        return '500'

    return '200'

#Return logs from container with name_container
def logs_container(name_container):
    response =""
    try:
        container= client.containers.get(name_container)
        response = container.logs().decode('utf8')
    except 	docker.errors.APIError:
        return '500'

    return response

#Check if the container with name_container is actually up
def is_running_container(name_container):
    state_container = os.popen('docker inspect --format=\'{{.State.Running}}\' ' + name_container).read().replace(
        '\n', '')
    return state_container

#this create a container and execute
def run_container_course(container):

    id_course = container['id_course']
    image =  container['image']
    name_vol_container = container['name_vol_container']

    command1 = "sed -i '/bind/s/^/#/g' /etc/mysql/my.cnf"
    command2 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'172.17.0.1' IDENTIFIED BY '12345';\""
    command3 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'localhost' IDENTIFIED BY '12345';\""
    command4 = "sudo /etc/init.d/mysql restart"

    try:
        container = client.containers.run(image,command=(command1,command2,command3,command4),detach=True,name=id_course,ports={'3306/tcp': None, '80/tcp': None},mounts=[Mount("/var/lib/mysql",name_vol_container,type='volume')])
        return '200'

    except docker.errors.ImageNotFound:
        return '500'
    except docker.errors.ContainerError:
        return '500'
    except docker.errors.APIError:
        return '500'


#get the data of container
def data_container(name_container):


    id_container = os.popen('docker inspect --format=\'{{.Id}}\' ' + name_container).read().replace(
        '\n', '')
    port_number_3306_container = os.popen(
        'docker inspect --format=\'{{(index (index .NetworkSettings.Ports "3306/tcp") 0).HostPort}}\' ' + name_container).read().replace(
        '\n', '')
    port_number_80_container = os.popen(
        'docker inspect --format=\'{{(index (index .NetworkSettings.Ports "80/tcp") 0).HostPort}}\' ' + name_container).read().replace(
        '\n', '')
    ip_address_container = os.popen(
        'docker inspect --format=\'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}\' ' + name_container).read().replace(
        '\n', '')
    mountpoint_vol_container = os.popen(
        'docker inspect --format=\'{{range  .Mounts}}{{.Source}}{{end}}\' ' + name_container).read().replace(
        '\n', '')
    state_container = os.popen('docker inspect --format=\'{{.State.Running}}\' ' + name_container).read().replace(
        '\n', '')
    image= os.popen('docker inspect --format=\'{{.Config.Image}}\' ' + name_container).read().replace(
        '\n', '')

    # ---Saving the container---
    data = {
        "id_container": id_container,
        "name_container": name_container,
        "port_number_80_container": port_number_80_container,
        "port_number_3306_container": port_number_3306_container,
        "base_image_container": image,
        "address_volume_db_host_container": mountpoint_vol_container,
        "ip_address_container": ip_address_container,
        "running_container": state_container,
        "associated_course": name_container
    }

    data_container_reg_str = json.dumps(data)
    data_container_reg_enc = data_container_reg_str.encode('utf-8')

    return data_container_reg_enc



#Insert a new student in the bd of domjudge inside of container, if this container is up
def enroll_course(data):

    # datos para poner generales

    host = '127.0.0.1'
    usuario_bd = 'macripco'
    pass_usuario_db = '12345'
    port = int(data['port_number_3306_container'])

    # student's data
    code_student = data['code_student']
    lastname_student = data['lastname_student']
    name_student = data['name_student']
    email_student = data['email_student']


    # conect domjudge's database

    try:

        conn = MySQLdb.connect(host=host, port=port, user=usuario_bd, passwd=pass_usuario_db, db='domjudge')
        cur = conn.cursor()
        cur.execute("INSERT INTO team(teamid,categoryid,name,enabled) VALUES(" + code_student+",3,'" + lastname_student+ " " + name_student + "' ,1)")
        cur.execute("INSERT INTO user(userid,username,name,email,password,teamid) VALUES(" + code_student + "," + code_student + ",'"+ lastname_student+ " " + name_student + "','" + email_student + "',md5('" +  code_student+ "#" + code_student + "')," + code_student + ");")
        cur.execute("INSERT INTO userrole(userid,roleid) VALUES(" + code_student + ",3)")
        cur.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error as e:
        return '500'
    return '201'

#insert the data of profesor an set up like admin of domjudge
def set_pass_admin_container(data):
    print("el lazo 6")

    host = '127.0.0.1'
    usuario_bd = 'macripco'
    pass_usuario_db = '12345'
    port = int(get_port_3306(data['id_course']))

    # user's data
    id_professor = data['id_professor']
    name_professor = data['name_professor']
    lastname_professor = data['lastname_professor']
    email_professor = data['email_professor']

    # conect domjudge's database

    try:

        conn = MySQLdb.connect(host=host, port=port, user=usuario_bd, passwd=pass_usuario_db,db='domjudge')
        cur = conn.cursor()
        cur.execute("INSERT INTO user(userid,username,name,email,password,enabled) VALUES("+ id_professor + ",'"+id_professor+"','"+ lastname_professor +' '+ name_professor +"','"+ email_professor +"',md5('" + id_professor + "#" +id_professor + "'),1);")
        cur.execute("INSERT INTO userrole(userid,roleid) VALUES(" + id_professor + ",1)")
        #cur.execute("delete from domjudge.user where userid=1;")
        cur.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error as e:
        print(e)
        return '500'

    return '201'

#delete all containers from period
def delete_containers_period(id_period):

    #stop all containers in that period
    os.system("docker stop $(docker ps -f name=" + str(id_period) + " -q)")
    #remove all containers in that period
    os.system("docker rm $(docker ps -a -f name=" + str(id_period) + " -q)")
    #remove volumes that belong to containers
    os.system("docker volume rm $(docker volume ls -f name=" + str(id_period) + " -q)")

    return '200'


def open_database(name_container):

    client1 = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container = client1.containers.get(name_container)

    command1 = "sed -i '/bind/s/^/#/g' /etc/mysql/my.cnf"
    command2 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'172.17.0.1' IDENTIFIED BY '12345';\""
    command3 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'localhost' IDENTIFIED BY '12345';\""
    command4= "sudo /etc/init.d/mysql restart"

    try:

        container.exec_run(command1,detach=False,stream=True,stderr=True, stdout=True)
        container.exec_run(command2,detach=False,stream=True,stderr=True, stdout=True)
        container.exec_run(command3,detach=False,stream=True,stderr=True, stdout=True)
        container.exec_run(command4,detach=False,stream=True,stderr=True, stdout=True)

        return '200'

    except docker.errors.APIError:
        return '500'


def get_data_contest_container(name_container):
    host = '127.0.0.1'
    usuario_bd = 'macripco'
    pass_usuario_db = '12345'
    port = int(get_port_3306(name_container))
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
        #--------get total number of students-------------------------------->
        #
        cur3 = conn.cursor()
        cur3.execute("select count(teamid) from team where categoryid=3;")
        row3 = cur3.fetchone()
        number_of_students=int(row3[0])
        cur3.close()
        print(number_of_students)


        # -------Adding all number of attemps by problems in each contest---->
        cur.execute("select cid from contest;")
        row = cur.fetchone()
        # por cada contest
        while row is not None:
            cur1 = conn.cursor()
            cur1.execute("select contestproblem.probid, problem.name from contestproblem, problem where contestproblem.cid =" + str(row[0]) + " and contestproblem.probid = problem.probid;")
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
                cur4.execute("select count(distinct teamid) from scorecache_jury where probid = " + str(row1[0]) +";")
                row4 = cur4.fetchone()
                number_of_submissions = int(row4[0])
                cur4.close()
                print("number_of_submissions")
                print(number_of_submissions)

                while row2 is not None:
                    attemps.append(row2)
                    row2 = cur2.fetchone()

                data['number_of_attempts'].append((row[0], row1[0], row1[1], attemps,( number_of_submissions, number_of_students)))
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
                cur = conn.cursor()
                cur.execute("select teamid, name from team where categoryid = 3 order by name;")
                row = cur.fetchone()
                eval = []
                while row is not None:
                    cur1 = conn.cursor()
                    res = cur1.execute("select scorecache_jury.cid, \
                                                       scorecache_jury.probid,\
                                                       scorecache_jury.teamid, \
                                                       team.name, \
                                                       scorecache_jury.is_correct \
                                                from scorecache_jury, \
                                                     team \
                                                where scorecache_jury.cid = " + str(contest[0]) + " and \
                                                scorecache_jury.probid = " + str(problem[0]) + " and \
                                                scorecache_jury.teamid = " + str(row[0]) + " and \
                                                scorecache_jury.teamid = team.teamid")
                    if res == 0:
                        eval.append(0)
                    else:
                        row1 = cur1.fetchone()
                        if row1[4] == 0:
                            eval.append(0)
                        elif row1[4] == 1:
                            eval.append(5)
                    row = cur.fetchone()
                data['evaluation'].append((contest[0], problem[0], eval))

        #-----Adding evaluations
        conn.commit()
        conn.close()

        print (data)


    except MySQLdb.Error as e:
        data['error'] = e

    data_str = json.dumps(data)
    data_enc = data_str.encode('utf-8')

    return data_enc


