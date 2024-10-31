sudo nano /boot/config.txt
gpu_mem=256

sudo apt update && sudo apt upgrade -y && sudo apt install mc python3 python3-pygame python3-vlc python3-mysqldb -y

#get GPU memmory
vcgencmd get_mem gpu


sudo nano /etc/systemd/system/rpitv.service

[Unit]
Description=RPiTV Signage Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/rpitv-viewer/main.py
WorkingDirectory=/home/pi/rpitv-viewer/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload

sudo systemctl enable rpitv.service

sudo systemctl start rpitv.service

sudo systemctl status rpitv.service || pkill -f main.py



Hiding Boot Text
sudo nano /boot/cmdline.txt
change: "console=tty1" to "console=tty3"
If not present add: "quiet loglevel=3 plymouth.enable=0 logo.nologo" at the end. Control+X, Y
