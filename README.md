# study-picamera-examples
A collection of picamera example based on OpenCV

# requirements

* python 2.7, 3.4, 3.5 or 3.6
* OpenCV 2.4 or 3.x

# dependencies

If you use desktop version of Raspbian, you may need to install following packages.

```
sudo apt update
sudo apt -y upgrade
sudo apt update
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libgtk2.0-dev libgtk-3-dev
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y libqtgui4 libqt4-test
sudo apt install -y libilmbase12 libopenexr22 libgstreamer1.0-dev
sudo apt install -y python3-dev python3-pip
sudo pip3 install numpy opencv-python picamera[array] flask imutils pyzbar
```

# getting started

1. Enable PiCamera `sudo raspi-config nonint do_camera 0`
2. Clone this repository on your Raspberry Pi
3. Go to the directory
4. Run `python3 camera/main.py`
5. Open Chrome browser with `localhost:5000` from your local workstation
