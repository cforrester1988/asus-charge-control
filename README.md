# asus-charge-control

> Set your recent ASUS notebook's maximum charge level on Linux.

Recent ASUS notebooks come with a Windows application to set the maximum battery
charge level, in order to reduce stress on the battery and prolong its lifespan. On
Linux kernels >= version 5.4, the ```asus_nb_wmi``` kernel module exposes a sysfs object to manage this setting.

Getting or setting the charge end threshold is rather verbose:

```console
$ cat /sys/class/power_supply/BAT0/charge_control_end_threshold
100

$ echo 80 | sudo tee /sys/class/power_supply/BAT0/charge_control_end_threshold
80
```

asus-charge-control offers a quicker way.

## Installation

asus-charge-control should work with any device running a recent kernel (>= 5.4) with the ```asus_nb_wmi``` module loaded. Use ```lsmod | grep asus_nb_wmi``` to check; if you see a line like ```asus_nb_wmi            32768  0```, then the module is running.

It has been tested with the following ASUS notebooks:

- ASUS VivoBook 15 **X512DA**

A Python version >= 3.7 is necessary to run this script. Most Linux distributions come with the right version. To verify that Python is installed on **Debian**/**Ubuntu**-based distributions, use apt:

```console
sudo apt install python3
```

As root privileges are necessary to set the charge end threshold, asus-charge-control should be installed as a global package:

```console
sudo pip install --system asus-charge-control
```

**DANGER:** Normally, Python packages should not be installed with ```sudo```, as they may execute arbitrary code. I encourage you to read ```setup.py``` before installation.

## Usage

You can get the current charge end threshold by calling ```asuscharge``` from  the command line:

```console
$ asuscharge
Current charge end threshold: 100%
```

Setting the charge end threshold requires root privileges:

```console
$ sudo asuscharge 80
Successfully set charge end threshold to 80%
```

**Note:** The charge end threshold resets back to 100% when the system is rebooted.

You can use a cron job to set the charge end threshold automatically on boot. To do so, find the path of the asuscharge command like so:

```console
$ which asuscharge
/usr/local/bin/asuscharge
```

Modify the root user's crontab file:

```console
sudo crontab -e
```

Add the following line to the end of the file:

```console
@reboot /usr/local/bin/asuscharge MAX
```

Replace ```MAX``` with the charge end threshold you would like, then save and close the file.

## Development

You can use the ```asuscharge``` package in your own applications. The package offers a ```ChargeThresholdController``` object, with a settable ```end_threshold``` property. It also offers three methods to check if the user's platform supports the charge end threshold feature: ```supported_platform(), supported_kernel(), and module_loaded()```.

## Version history

- 1.0.1
  - (fix) supported_kernel() returned an incorrect value for Linux kernel versions > 5.9

- 1.0.0
  - Initial release.
