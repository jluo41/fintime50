#!/bin/sh

root=`pwd`

# install anaconda python
cd /tmp
curl https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh -o anaconda3.sh
bash anaconda3.sh -b

# update stuff
echo "export PATH=\"/home/ubuntu/anaconda3/bin:\$PATH\"" >> ~/.bashrc
export PATH="/home/ubuntu/anaconda3/bin:$PATH"
apt-get update
apt-get install build-essential -y
apt-get install daemon -y
apt-get install nginx -y 

# install dependencies
cd $root
pip install -r requirements.txt

# install latest scrapyd-client from repository
# current production version as on Jul, 2017 does not have all tools
pip install git+https://github.com/scrapy/scrapyd-client.git

# setup nginx conf files
conf_file="pubcrawler.nginx.conf"
cp $root/$conf_file /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/$conf_file /etc/nginx/sites-enabled/$conf_file
rm /etc/nginx/sites-available/default
rm /etc/nginx/sites-enabled/default
