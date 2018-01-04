# Deployment Guide for Pubcrawler

This tutorial will guide you to install Pubcrawler on Amazon EC2. The setup environment contains Ubuntu 16.04 LTS, Anaconda Python 3.x, Nginx softwares.



## Contents

1. Setup EC2 instance
2. Setup RDS instance
3. Deploy Pubcrawler
4. Manage spiders
5. Manage Scrapy server
6. References





## 1. Setup EC2 instance

### 1. 1 Create security group

Create a security group for EC2 instance with the following configuration

1. Add following Inbound rules with `source` field containing **my IP address**. These rules define who can access the EC2 server.
   1. SSH
   2. Custom TCP at port **8080**


2. Following Outbound rules by default allow all traffic (and this should be fine). We need at least the following in case you want to be specific. These rules define whom your EC2 server can access.
   1. HTTP, HTTPS with destination **anywhere**
   2. Custom TCP at 8080 with destination **anywhere**


### 1.2 Create EC2 instance

Read through the following before setting up AW EC2 instance

1. Launch an EC2 instance using Ubuntu 16.04 LTS 64-bit image
2. Use the above created security group while configuring
3. Download the private key if you don't have and when asked at the end of configuration
4. You can use default values for remaining configuration settings

### 1.3 Install dependencies

Log into your EC2 instance and the following commands will help you to do that.

1. SSH into EC2 instance

   ```txt
   $ ssh -i "<path-to-private-key>" <username>@<ec2-public-dns>

   <path-to-private-key> := Absolute or relative path to the file you just downloaded
   <username> := Amazon assigns "ubuntu" by default
   <ec2-public-dns> := This is available in your EC2 instances list
   ```

2. Copy `install.sh`, `requirements.txt` and `pubcrawler.nginx.conf` files to EC2 instance. These files can be downloaded from Pubcrawler repository.

3. Execute the following commands on your remote bash shell.

   ```bash
   chmod +x install.sh
   sudo ./install.sh
   ```


### 1.4 Run Scrapy server

1. Start Nginx `$ sudo nginx`
2. Start Scrapy server `$ scrapyd`. Use `$ nohup scrapyd &` to run asynchronously.
3. Scrapy server should be available at `http://<public dns ip>:8080`




## 2. Setup RDS instance

This section will help you start a MySQL server on AWS RDS

### 2.1 Create security group

Create a security group for RDS instance with the following configuration

1. Add the following Inbound rules
   1. MySQL/Aurora with `source` field containing **my IP address** or **anywhere** depending on from where you want to access the database.
   2. MySQL/Aurora with `source` field containing **EC2 security group** ID you created previously.

### 2.2 Create MySQL instance

1. From RDS dashboard select MySQL as your database
2. Use the security group created above
3. Optionally, enable your instance to use AWS IAM for authentication




##  3. Deploy Pubcrawler

This part of deployment is done from your local system where Pubcrawler source code is available.

### 3.1 Install dependencies

1. Using your Python 3.x environment, install `scrapy` package

   ```txt
   pip install scrapy
   ```

2. Install the latest development version of  `scrapyd-client` package. This package's version available on `pip` does not seem to provide all features.

   ```txt
   pip install git+https://github.com/scrapy/scrapyd-client.git
   ```



### 3.2 Update production database configuration

Pubcrawler does not yet have a neat way to switch between test and production database. As such, these settings have to be hardcoded in the source code now.

1. First, create a database schema in the above database. We will refer it as `<database-schema>` in the following contents.
2. Obtain AWS's MySQL public DNS address, port, username and password
3. Update these values in `repository/fintime50/fintime50/model.py` file. The update string would look like `mysql+pymysql://<user>:<password>@<ec2-dns>:<port>/<database-schema>`
4. Update `repository/fintime50/fintime50/pipelines.py` file to use `MySQL` database instead of `SQLite` database. i.e, replace `sdb_connect` string with `mdb_connect` string at appropriate places.


### 3.3 Update Scrapy configuration

The configuration file is available at `repository/fintime50/scrapy.cfg`

Ensure the following lines exist in the configuration file. **Note: Its probably not a good add these details to the repository.**

**Before the change**:

```text
[deploy]
#url = http://localhost:6800/
project = fintime50
```

**After the change**:

```text
[deploy:production]
url = http://<AWS-EC2-Public-DNS>:8080/
project = fintime50
```

Pay attention to `[deploy]` and `#` in `#url = http://localhost:6800/`.

### 3.4 Finally, deploy

1. cd to the `fintime50` directory in your local pubcrawler repository
2. Execute `$ scrapyd-deploy production`
3. Open `http://<AWS-EC2-Public-DNS>:8080/` to notice the project ID


## 4. Manage spiders

This section will help you to quickly get started with using Pubcrawler's spiders. Please find the links in references section for comprehensive information. *You need to `cd` into `repository/fintime50`* before executing these commands.

**Start the server**

`$ scrapyd`

Then stop it, and use `nohup scrapyd &` to run it in background process.

**List all available targets**

`$ scrapyd-deploy -l`

**Deploy the project to production**

```txt
# visit the production URL (target) after deploying
$ scrapyd-deploy production
```

**List all projects available in production**

`$ scrapyd-deploy -L production` or

`$ scrapyd-client -t <target url> projects`

**Get list of all spiders**

`$ scrapyd-client -t <target url> spiders -p fintime50`

or simply:

`$ scrapyd-client spiders -p fintime50`

**Schedule spider(s)**

`$ scrapyd-client -t <target url> schedule -p fintime50 <spider-name>`

`$ scrapyd-client -t <target url> schedule -p fintime50` to schedule all spiders

or simply:

`$ scrapyd-client schedule -p fintime50 <spider-name>`

`$ scrapyd-client schedule -p fintime50`

**Cancel a job**

`$ curl <target url>/cancel.json -d project=fintime50 -d job=<job-id>`

**Remove the project from scrapy server**

`$ curl <target url>/delproject.json -d project=fintime50`



## 5. Manage Scrapy server

Scrapy on EC2 is configured to run Nginx server as a reverse proxy to Scrapy's default server. Please find in the references the comprehensive documentation to manage Nginx and Scrapy servers.

### 5.1 Nignx

1. Start server: `$ sudo nginx`
2. Restart server: `$ sudo nginx -s reload`
3. Stop server: `$ sudo nginx -s stop`

### 5.2 Scrapyd

1. Earlier it is shown to asynchronoysly start `scrapyd`, the daemon to start Scrapy's server
2. To stop this server process, first find the process ID using the command `$ ps aux | grep scrapyd`
3. Followed by, stop the server by killing the process `$ kill -9 <process ID>`
4. Scrapy server's configuration can be managed using `scrapy.cfg` file located in the directory from which the server is started. Refer to the documentatin for more details.





## 6. References

1. https://scrapyd.readthedocs.io/en/stable/ (How to run Scrapy)
2. https://doc.scrapy.org/en/latest/intro/install.html (How to install Scrapy)
3. https://github.com/scrapy/scrapyd-client (How to manage Scrapy)
4. http://nginx.org/en/docs/beginners_guide.html#control (Nignx begineers guide)
