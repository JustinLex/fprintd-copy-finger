# fprintd-copy-finger
Small python script for copying a registered finger from one user to another on Linux.

`fprintd`, the daemon for fingerpint authentication on Linux, doesn't allow using the same fingerprint to authenticate two users on the same computer. This is a pain if you have multiple accounts on the same laptop and want to use fingerprint authentication for both accounts. This tool allows you to override that by making a copy of the fingerprint record and installing it onto another user.

## Some notes
This script was written for and tested on a Lenovo Thinkpad P14s Gen 2 (AMD), which uses a "Synaptics, Inc. Prometheus MIS Touch Fingerprint Reader", with the USB id `06cb:00bd`. I was running Fedora 35 with `fprintd 1.94.1-1.fc35`. 

This method of copying the fingerprint may not work on other fingerprint sensors, especially if libfprint stores the fingerprint data differently with that sensor. 

Please let me know how it goes if you try this on any other fingerprint sensor!

This script is completely unsupported by libfprint. The fact that duplicate fingerprint records are not allowed was 
[a conscious decision by the libfprint developers](https://gitlab.freedesktop.org/libfprint/fprintd/-/blob/master/src/device.c#L2226). 
This tool is just convenient if you happen to use your fingerprint sensor in a way that benefits from duplicate fingerprints. 
This code comes with no warranty, and I take no responsibility for you bricking your fingerprint sensor or your authentication configuration getting borked.

## How to use
1. Clone the repo on your machine

```
git clone https://github.com/JustinLex/fprintd-copy-finger.git
cd fprintd-copy-finger/
```

2. Install the system package and python dependencies, preferably in a venv.

This script uses the `PyGOgject` library to interface with fprintd, and `PyGObject` has a number of build dependencies that 
you will have to install on with your system package manager. The command example below shows the packages that you will need if you are using Fedora.
If you are running another distro, try googling these packages to find the names of the build dependencies for your distro.

```
sudo dnf install python-devel glib2-devel cairo-devel cairo-gobject-devel gobject-introspection-devel
python -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

3. Find the fingerprint file that you want to copy.

By default, fingerprint files are stored under `/var/lib/fprint/{user}/{vendor name}/{sensor id}/{finger id}`, and can only be read by root.

4. Run the script as root, pointing it at the fingerprint file that you want to clone, and the user you want to copy the fingerprint to.

e.g. `sudo python copy-finger.py /var/lib/fprint/jlh/synaptics/7c3928dbc3a2/7 justin`
