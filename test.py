import docker
from docker.types import Mount
from threading import Thread
import time


client = docker.DockerClient(base_url='unix://var/run/docker.sock')

container= client.containers.run(
    "python_base_image:v02",
    detach=True,
    name='201802750001M03',
    ports={'3306/tcp': None, '80/tcp': None},
    mounts=[Mount("/var/lib/mysql","201802750001M03_backup_db",type='volume')]
)
print ("antes")
time.sleep(8)
print ("despues")

#container = client.containers.get("201802750001M01")

command1 = "sed -i '/bind/s/^/#/g' /etc/mysql/my.cnf"
command2 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'172.17.0.1' IDENTIFIED BY '12345';\""
command3 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'localhost' IDENTIFIED BY '12345';\""
command4 = "sudo /etc/init.d/mysql restart"

a = container.exec_run(command1, detach=False, stream=True, stderr=True, stdout=True)
b = container.exec_run(command2, detach=False, stream=True, stderr=True, stdout=True)
c = container.exec_run(command3, detach=False, stream=True, stderr=True, stdout=True)
d = container.exec_run(command4, detach=False, stream=True, stderr=True, stdout=True)



# def crear_cont():
#
#     client = docker.DockerClient(base_url='unix://var/run/docker.sock')
#
#     container= client.containers.run(
#         "python_base_image:v02",
#         detach=True,
#         name='201802750001M01',
#         ports={'3306/tcp': None, '80/tcp': None},
#         mounts=[Mount("/var/lib/mysql","201802750001M01_backup_db",type='volume')]
#     )
#
#     container = client.containers.get("201802750001M01")
#
#     command1 = "sed -i '/bind/s/^/#/g' /etc/mysql/my.cnf"
#     command2 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'172.17.0.1' IDENTIFIED BY '12345';\""
#     command3 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'localhost' IDENTIFIED BY '12345';\""
#     command4 = "sudo /etc/init.d/mysql restart"
#
#     a = container.exec_run(command1, detach=False, stream=True, stderr=True, stdout=True)
#     b = container.exec_run(command2, detach=False, stream=True, stderr=True, stdout=True)
#     c = container.exec_run(command3, detach=False, stream=True, stderr=True, stdout=True)
#     d = container.exec_run(command4, detach=False, stream=True, stderr=True, stdout=True)
#
#
# def open_cont():
#
#     container = client.containers.get("201802750001M01")
#
#     command1 = "sed -i '/bind/s/^/#/g' /etc/mysql/my.cnf"
#     command2 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'172.17.0.1' IDENTIFIED BY '12345';\""
#     command3 = "mysql --user=\"root\" --password=\"temprootpass\" --execute=\"GRANT ALL PRIVILEGES ON *.* TO 'macripco'@'localhost' IDENTIFIED BY '12345';\""
#     command4 = "sudo /etc/init.d/mysql restart"
#
#     a = container.exec_run(command1,detach=False,stream=True,stderr=True, stdout=True)
#     b = container.exec_run(command2,detach=False,stream=True,stderr=True, stdout=True)
#     c = container.exec_run(command3,detach=False,stream=True,stderr=True, stdout=True)
#     d = container.exec_run(command4,detach=False,stream=True,stderr=True, stdout=True)


# hilo1 = threading.Thread(name='crear_cont', target=crear_cont, daemon=True)
# hilo1.start()
# hilo2 = threading.Thread(name='open_cont', target=open_cont, daemon=True)
# hilo2.start()



#
#
#
#     container= client.containers.get(name_container)
#
#
#
#     print("a")
#     print(a)
#     print("b")
#     print(b)
#     print("c")
#     print(c)
#     print("d")
#     print(d)
#
# def data(name):
#     t = Thread(target=open, args=(name,))
#     t.start()
#     t.join()
#
# data("201802750001M03")


#client = docker.APIClient(base_url='unix://var/run/docker.sock')


#mount = Mount("/var/lib/mysql","201802750001M04_backup_db",type='volume')
#container= client.containers.get("201802750001M01")
#container.start()
#container.stop()
#container.remove()

# res=container.logs().decode('utf8')
# print (type(res))
# print(res)