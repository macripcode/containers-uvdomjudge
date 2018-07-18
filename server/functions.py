from django.shortcuts import render
import os
import json
import MySQLdb

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
    response = os.popen(
        'docker stop ' + name_container).read().replace(
        '\n', '')
    if response == name_container:
        return '200'
    return '500'
#hasta aqui ya hice el server

#Start container with name_container
def start_container(name_container):
    response = os.popen(
        'docker start ' + name_container).read().replace(
        '\n', '')
    if response == name_container:
        return '200'
    return '500'

#Remove container with name_container
def remove_container(name_container):
    response = os.popen(
        'docker rm ' + name_container).read().replace(
        '\n', '')
    if response == name_container:
        return '200'
    return '500'

#Return logs from container with name_container
def logs_container(name_container):
    response = os.popen(
        'docker logs ' + name_container).read()
    return response

#Check if the container with name_container is actually up
def is_running_container(name_container):
    state_container = os.popen('docker inspect --format=\'{{.State.Running}}\' ' + name_container).read().replace(
        '\n', '')
    return state_container

#this create a container and execute
def run_container_course(container):
    print("dato de container")
    print(type(container))
    print(container)

    id_course = container['id_course']
    image =  container['image']
    name_vol_container = container['name_vol_container']


    #probar try catch para ver si cuando el contenedor y existe lo captura
    instruction = "docker run -d -v " + name_vol_container + ":/var/lib/mysql -p :80 -p :3306 --name " + id_course + " " + image
    response = os.system(instruction)

    return response

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
    print("data_container_reg_str")
    print(data_container_reg_str)
    print("data_container_reg_enc")
    print(data_container_reg_enc)


    #data_container_reg_enc = data_container_reg_str.encode('utf-8')
    #response = create_container(data_container_reg_enc)

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
        file = open('testfile.txt', 'w')
        file.write(e)
        file.close()
        return '500'
    
    return '201'

#insert the data of profesor an set up like admin of domjudge
def set_pass_admin_container(data):
    print("el lazo 6")


    host = '127.0.0.1'
    usuario_bd = 'macripco'
    pass_usuario_db = '12345'

    # get port number 3306
    name_container = data['id_course']
    port_number_3306_container = os.popen(
        'docker inspect --format=\'{{(index (index .NetworkSettings.Ports "3306/tcp") 0).HostPort}}\' ' + name_container).read().replace(
        '\n', '')
    port = int(port_number_3306_container)

    # user's data
    id_professor = data['id_professor']
    name_professor = data['name_professor']
    lastname_professor = data['lastname_professor']
    email_professor = data['email_professor']

    # conect domjudge's database

    try:

        conn = MySQLdb.connect(host=host, port=port, user=usuario_bd, passwd=pass_usuario_db,
                               db='domjudge')
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
    user='root'
    password='temprootpass'
    host='localhost'
    db='domjudge'

    command1 = "docker exec -d "+name_container+" sh -c \"sed -i '/bind/s/^/#/g' /etc/mysql/my.cnf\""
    command2 = "docker exec -d "+name_container+" sh -c \"mysql --user=\\\"root\\\" --password=\\\"temprootpass\\\" --execute=\\\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'172.17.0.1' IDENTIFIED BY '12345';\\\"\""
    command3= "docker exec -d "+name_container+" sh -c \"sudo /etc/init.d/mysql restart \""
    res1=os.system(command1)
    res2=os.system(command2)
    res3=os.system(command3)


    if res1==0 and res2==0 and res3==0:
        return '200'
    return '500'
