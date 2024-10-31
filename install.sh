#!/bin/bash

# Update and upgrade the system
echo "Updating and upgrading the system..."
sudo apt update
sudo apt -y upgrade

# Update gpu_mem parameter
echo "Updating /boot/firmware/config.txt..."
sudo sed -i '/^max_framebuffers/c\max_framebuffers=2\ngpu_mem=256' /boot/firmware/config.txt

# Install necessary packages
echo "Installing necessary packages..."
sudo apt install -y python3 python3-vlc python3-pygame mc

# Create media directory
echo "Creating media directory..."
mkdir -p ./media

# Create systemd service file
echo "Creating systemd service..."
sudo bash -c 'cat > /etc/systemd/system/rpitv.service <<EOF
[Unit]
Description=RPiTV Service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/rpitv-viewer/main.py
WorkingDirectory=/home/pi/rpitv-viewer/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd to apply the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service..."
sudo systemctl enable rpitv.service

# Wait for key press and then reboot
read -p "Installation complete. Press any key to reboot..."
read -p "Don't forget to update config.json file in app folder to set rpi_id and token."
sudo reboot