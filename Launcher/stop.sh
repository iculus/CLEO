#!/bin/sh
sudo killall crystalz-launch && echo "launcher down"
sudo killall crystalz-sense && echo "fingers down"
sudo killall crystalz-ard && echo "sensors down"
sudo killall crystalz-lights && echo "lights down"
sudo killall ngrok && echo "ngrok down"

exit 0

