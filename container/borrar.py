from django.shortcuts import render
import os
import json

import MySQLdb



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



def set_user_admin(data):
    """
    # datos para poner generales
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
    id_user = data['id_professor']
    #print("desde functions id user")
    #print(id_user)

    # conect domjudge's database

    try:

        conn = MySQLdb.connect(host=host, port=port, user=usuario_bd, passwd=pass_usuario_db,
                               db='domjudge')
        cur = conn.cursor()
        cur.execute(
            "UPDATE user SET username = '" + id_user + "', password =md5('" + id_user + "#" + id_user + "') WHERE username='admin'")
        cur.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error as e:
        return '500'
    """

    return 'funcion equivocada'




#from container.views import set_user_admin
#data={"id_course": '201701750017M01',"id_professor": '1144123789'}
#cont=set_user_admin(data)
