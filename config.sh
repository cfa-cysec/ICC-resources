#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y

#gives access to ifconfig
sudo apt-get install net-tools -y

#install remmina
sudo add-apt-repository -y ppa:remmina-ppa-team/remmina-next
sudo apt-get update
sudo apt-get install remmina* -y

echo "Remmina installation complete!"

#enable rdp
grdctl rdp enable
grdctl rdp disable-view-only

echo "RDP Enabled"

#background setup
IMAGE_URL="https://kds-tools.com/work/cfa_background.png"
IMAGE_PATH="$HOME/Pictures/cfa_background.jpg"
wget -O "$IMAGE_PATH" "$IMAGE_URL"

gsettings set org.gnome.desktop.background picture-uri "file://$IMAGE_PATH"
gsettings set org.gnome.desktop.background picture-options 'stretched'

echo "Background set"

#enable ssh
sudo apt-get install ssh -y
sudo systemctl enable ssh
sudo systemctl start ssh

echo "SSH enabled"

#install python
sudo apt install python3 python3-pip -y 

echo "python installed"

# power settings

#screen blank -> turn screen off after a period of inactivity
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver ubuntu-lock-on-suspend false

echo "power settings fixed"

#automatic login

current_username=$(whoami)

gdm_config="/etc/gdm3/custom.conf"

sudo sed -i "s/^#\s*AutomaticLoginEnable\s*=\s*.*/AutomaticLoginEnable=true/" "$gdm_config"
sudo sed -i "s/^#\s*AutomaticLogin\s*=\s*.*/AutomaticLogin=$current_username/" "$gdm_config"

echo "enabled auto login"

#install visual studio code
sudo apt install software-properties-common apt-transport-https wget -y
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository -y "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install code

echo "visual studio installed"