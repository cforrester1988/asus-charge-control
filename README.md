# asus-charge-control

Set your recent ASUS notebook's maximum charge level on Linux.

Recent ASUS notebooks come with a Windows application to set the maximum battery
charge level, in order to reduce stress on the battery and prolong its lifespan. On
Linux kernels >= 5.4, the ```asus_nb_wmi``` kernel module exposes a sysfs object to manage this setting.

Getting or setting it is rather verbose:

```console
$ cat /sys/class/power_supply/BAT0/charge_control_end_threshold
100

$ echo 80 | sudo tee /sys/class/power_supply/BAT0/charge_control_end_threshold
80
```

**asus-charge-control** offers a quicker way:

```console
$ asuscharge
Current charge end threshold: 100%

$ sudo asuscharge 80
Successfully set charge end threshold to 80%
```

**TODO:** Create a simple GUI interface to do the same.

**asus-charge-control** should work with any device running a recent kernel (>= 5.4) with the ```asus_nb_wmi``` module loaded. Use ```lsmod | grep asus_nb_wmi``` to check; if you see a line like ```asus_nb_wmi            32768  0```, then the module is running.

It has been tested with the following ASUS notebooks:

- ASUS VivoBook 15 **X512DA**
