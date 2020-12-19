# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 

Site URL: http://54.176.241.134/

# Below is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.

1. Server URL: ec2-54-176-241-134.us-west-1.compute.amazonaws.com
2. SSH username: ubuntu
3. SSH password or key: uploaded to folder
    <br> If a ssh key is used please upload the key to the credentials folder.
4. Database URL or IP and port used: 
    <br>DB URL: trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com
    <br>Port: 3306
    <br><strong> NOTE THIS DOES NOT MEAN YOUR DATABASE NEEDS A PUBLIC FACING PORT.</strong> But knowing the IP and port number will help with SSH tunneling into the database. The default port is more than sufficient for this class.
5. Database username: root
6. Database password: trademartadmin
7. Database name (basically the name that contains all your tables): Trademart
8. Instructions on how to use the above information.
    <br><strong>To connect to the Server:</strong>
    <br>1. Open up the terminal
    <br>2. Go into same directory that contains the ssh key file
    <br>3. Use this command to ssh into the server (as root user): ssh -i "team7server.pem" ubuntu@ec2-54-176-241-134.us-west-1.compute.amazonaws.com

    <br><strong>To connect to the database:</strong>
    <br>1. Open up MySQL Workbench
    <br>2. Click the + symbol next to MySQL Connections to add a new database
    <br>3. Enter these credentials:
           <blockquote>Connection Name: Trademart DB
           <br>Connection Method: Standard (TCP/IP)
           <br>Hostname: trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com
           <br>Port: 3306
           <br>Username: root
           <br>Password: > click "Store in Vault..." and enter trademartadmin
           <br>Click "OK"
	   <blockquote>

# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.
