# iso-builder

## Description
iso-builder Python script for building self installing customized GNU/Linux ISO files.

The point of this script is to enable the creation of a very simple custom self-installing ISO in the most simple way.

## Usage
Default values are set for all variables, so the most simple way to run the script is just by:
~~~~
  iso-builder
~~~~

There are many options that can be provided from command line. Check `iso-builder -h` for a list of them. For example, in order to build an ISO file that installs Ubuntu 14.04.4, creates the user called "Julen" with password "MY_PASSWORD" and sets the root password to "MY_PASSWORD", just run:
~~~~
  iso-builder --root_password MY_PASSWORD --user_password Julen:MY_PASSWORD --get_os ubuntu-14.04.4
~~~~

You can also specify your own ISO file, with the `--iso_name` option.

## Building a .deb package
To build a .deb package:
~~~~
  cd deb-pkg/
  sudo chown -R root:root iso-builder-1.0-1
  dpkg --build iso-builder-1.0-1
~~~~

And install with:
~~~~
  dpkg -i iso-builder-1.0-1.deb
~~~~

