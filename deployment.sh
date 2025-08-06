# run docker container instance in the same network
docker run --network=my_rasp_network -v m:/var/lib/mysql -p 3306:3306 -h 127.0.0.1 --name mysql -e MYSQL_ROOT_PASSWORD=Nirvikalpa#123 --restart unless-stopped mysql

docker cp /home/pi/docker_vol_backup/dump.sql mysql:/dump.sql

docker exec -it mysql bash -c "mysql -u root -p -e 'CREATE DATABASE ContainerDatabase; USE ContainerDatabase; SOURCE /dump.sql;'"

docker run --network=my_rasp_network -p 5001:5001 richie31/notify