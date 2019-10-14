# A Satoshi Piggy Bank Tutorial 🐷

I tweeted [this](https://twitter.com/kiltonred/status/1180359423727783936) sometime ago:

>Bitcoin hardware wallet that’s WiFi connected and shows the dollar value of the bitcoin within it would be useful as a piggy bank for kids.
>
>Watching their savings grow over the long haul would help kids develop low time preference

A few days later, I built it (kind of...). I didn't build a hardware wallet, but a little device that can monitor how many satoshis a given bitcoin address has and the current US dollar value of those satoshis.

![Side view](./images/side.png)

![Top view](./images/top.png)

The rest of this document is a tutorial on how to build one of these.

## Assumptions about you

Before we get too deep into this tutorial, let's set some expectations. I'm expecting that you:

* Already have bitcoin address that you want to monitor (it can be a segwit or a legacy address)
* You are comfortable with using the terminal app (or willing to learn)

Let's get started.

## Parts & tools 🛠

### Required

#### [Raspberry Pi Zero starter kit](https://www.amazon.com/gp/product/B0748MBFTS) ($27)

You won't need all the items that come with this kit, but it's still a good deal.

#### [32GB microSD card](https://www.amazon.com/gp/product/B079GTYCW4) ($6)

This You'll need a microSD card with at least 8GB of storage. If you have one handy, you don't need to buy a new one.

#### [Tiny screen](https://www.amazon.com/gp/product/B07T4LGTWT) ($14)

This is the tiny screen where the satoshi balance and dollar value will be displayed.

It's a Chinese knock-off of the out-of-stock [Adafruit PiOLED - 128x32 Monochrome OLED Add-on for Raspberry Pi](https://www.adafruit.com/product/3527)

#### [Soldering iron kit](https://www.amazon.com/gp/product/B07PDK3MX1) ($10)

You see the little pins that are sticking out of the Pi? These come as part of the Pi kit. You'll need to solder them onto the Pi before you can plug-in the display.

This soldering kit comes with soldering wire.

### Other tools you might need, if you don't already have

#### SD card reader

You'll need a way to plug-in this microSD card to your desktop computer to put the Pi software on it. This microSD comes with an adapter, so if you have a standard SD card reader on your desktop, you're good. Otherwise, you might need an SD card reader [like this](https://www.amazon.com/SmartQ-C307-Portable-MicroSDHC-MicroSDXC/dp/B06ZYXR7DL).

#### USB keyboard and mouse

You'll need a USB keyboard and mouse to control the Pi once you start it up.

(Alternatively, if you're advanced user, you can control the Pi using SSH from your desktop. Search YouTube for tutorials on that.)

## Soldering the pins onto the Pi 🔥

Once you have your Pi and soldering kits. You can get started by soldering the pins onto the Pi. [This YouTube video tutorial](https://www.youtube.com/watch?v=UDdbaMk39tM) shows how:

[![Raspberry Pi soldering](https://img.youtube.com/vi/UDdbaMk39tM/0.jpg)](https://www.youtube.com/watch?v=UDdbaMk39tM)

## Installing Operating System on the Pi 💻

When you receive your Pi, it'll be a brick without any operating system. The first thing you'll need to do is install the operating system. [This YouTube video tutorial](https://www.youtube.com/watch?v=GJDIgS8nres) shows how:

[![Raspberry Pi soldering](https://img.youtube.com/vi/GJDIgS8nres/0.jpg)](https://www.youtube.com/watch?v=GJDIgS8nres)

## Put the Pi in the case 🥧

Now that you're done with soldering and you have the microSD card inserted in the Pi, you can put the Pi inside the clear case.

The case should have windows to the pins from both sides.

## Plug-in the tiny screen

The tiny screen goes over the case. Plug it in the correct location, as shown in this picture (but over the case)

![](./images/pluggedin-screen.jpeg)

## Install the software for the tiny screen

This part of the tutorial may feel a little uncertain. Follow the steps below and hopefully you'll get through it!

For this step, you'll need some knowledge of the Raspberry Pi terminal app. This [YouTube video tutorial](https://www.youtube.com/watch?v=UW3UxK4Tiqg) may be a good introduction.

Launch the terminal app in your Pi and start following the below sections

### Update Pi and Python libraries

Enter the commands that you see in the ["Update Your Pi and Python" in this page](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi#update-your-pi-and-python-3-4).

### Enable the I2C thingamajig

For the tiny screen and Pi to be able to talk to each other, you need this I2C thing enabled. To enable it follow [this guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).

After going through the guide above, you can enter the command below to see if things are working

```bash
sudo i2cdetect -y 0
```

If you see a number show up in the grid that means your Pi can now see your connected screen!

### Keep installing stuff

As [these instructions](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage) show, you'll next need to run the following commands:

```bash
sudo apt-get install python3-pip
```

Then

```bash
sudo apt-get install python3-pil
```

If the above two commands complete without errors, you're good! 👍

## Run the Python script 🐍

Now you're ready to start running Python code that can display things on the screen!

Download the code using `git clone`

```bash
git clone https://github.com/kiltonred/satoshi-piggy-bank.git
```

Run the code

```bash
sudo python3 ./satoshi-piggy-bank/piggy-bank.py --address 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp --fontsize 11 --lineheight 20 --refreshrate 3600
```

Hopefully you're now seeing the satoshis and dollar value on the screen?

### Options for the Python script

In the above command, you can see values such as ` 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp`. You can replace this address with your own. And you can replace any of the other options, too.

The options are:

Name|Default|Description
-|-|-
`--address`|`1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp`<br>(Some address I found online)|The Bitcoin<br>address to track
`--fontsize`|14|How big the font<br>on the screen is
`--lineheight`|20|How far away the<br>lines are from each other
`--refreshrate`|3600|How often the<br>screen updates

You can re-run the command above with different options to see which configurations you like.

## Run the `piggy-bank.py` script on Pi start-up

You don't want to run this command manually every time you plug-in your Pi. You want it to run automatically.

To make that happen, you'll need to edit the file called `/etc/rc.local`. If you're new to editing files using the terminal, [watch this tutorial](https://www.youtube.com/watch?v=boD-opv0fMs).

To get started, enter

```bash
sudo nano /etc/rc.local
```

That will open `/etc/rc.local` in the `nano` editor.

Before the the line that says `exit 0`, paste your `piggy-bank.py` script command.

After you finish, your `/etc/rc.local` file should look something like this

```bash
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo python3 /home/pi/satoshi-piggy-bank/piggy-bank.py --address 1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp --fontsize 14 --lineheight 20 --refreshrate 3600

exit 0
```

Now to save and exit `nano`, press `Ctrl`+`x`. It will ask you want to save the changes, press `y` for `Yes`. It will ask you if you want to save using the same file name, just press `Enter`.

## Test the start-up script

Unplug your Pi and plug it back in. Within a minute or so, the `piggy-bank.py` script should run and it should update the screen.

## You're done!

This is the end of the tutorial. If you've got it working, hooray! Congratulations! 🎉

## Questions or comments

I know these instructions were vague and unclear in many areas. If you're stuck some where, need clarifications, or help, [post an issue](https://github.com/kiltonred/satoshi-piggy-bank/issues/new).
