#!/bin/sh

echo Installing flight computer service...
cp resources/service/rocket.service /etc/systemd/system/rocket.service
systemctl enable rocket > /dev/null 2>&1
echo Installing flight computer service complete.
