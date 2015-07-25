[![Circle CI](https://circleci.com/gh/utk-robotics-2016/utk-robotics-2016.svg?circle-token=54928279bf95f8682260893ee69e4ad5cc5ea3a3)](https://circleci.com/gh/utk-robotics-2016/utk-robotics-2016)

# utk-robotics-2016

Here are the steps that will get you coding as fast as possible:

### Reading

Before jumping in, skim through:

* [The competition rules](https://docs.google.com/document/d/1ITIsL9fpTk5HKEJW1NENVrkgfCgXqONWpm0sevzeYmo/edit)
* [Robot overview](../../wiki/Robot-overview) (wiki)
* [Beaglebone](../../wiki/Beaglebone) (wiki)
* [Contributing to Software](../../wiki/Contributing-to-Software) (wiki)
* Just the wiki in general

These documents will give you all the basic info, as well as information on getting set up with accounts on the Beaglebone.

### Setting up the git repo

Once you have connected to the Beaglebone through the instructions provided in [Beaglebone](../../wiki/Beaglebone), you first need to set up your private/public keypairs, which are not created automatically when your account is set up. In the BBB's shell,

    ssh-keygen -t rsa -b 4096 -C "YOUR_GITHUB_EMAIL"

Follow the prompts. The password does not need to be your Github password, and you can choose not to have one. You will now have key files located in `~/.ssh`. Now run

    cat ~/.ssh/id_rsa.pub

And copy the output to your clipboard. Next, follow the steps at https://help.github.com/articles/generating-ssh-keys/#step-4-add-your-ssh-key-to-your-account to add the SSH key to your Github account. You can now

    git clone git@github.com:utk-robotics-2016/utk-robotics-2016.git

To get this repository in your home directory. You will be on the `master` branch by default. As explained in [Contributing to Software](../../wiki/Contributing-to-Software), feel free to look around in master, but do not commit any changes directly to it. You will make changes in your own branch. Please consult [Contributing to Software](../../wiki/Contributing-to-Software) for instructions on how to do that.

### Setting up `$PYTHONPATH`

At this point you will want to make sure that the robot is on a SAFE place on the GROUND. Running code can cause the robot to take off when you least expect it. You will not be very popular if you drive the robot off the desk.

Our first step will be to add our code directory to or `$PYTHONPATH`. First get the directory of your code directory. Example:

    corytest@beaglebone:~$ ls
    utk-robotics-2016
    corytest@beaglebone:~$ cd utk-robotics-2016/
    corytest@beaglebone:~/utk-robotics-2016$ ls
    circle.yml  dominate.py  head  README.md  research  test.sh  torso  utils
    corytest@beaglebone:~/utk-robotics-2016$ pwd
    /home/corytest/utk-robotics-2016
    corytest@beaglebone:~/utk-robotics-2016$ vim ~/.bashrc

In this example, `/home/corytest/utk-robotics-2016` is the directory that you will add to your `$PYTHONPATH`. At the end of `~/.bashrc`, add the following line:

    export PYTHONPATH="${PYTHONPATH}:/home/corytest/utk-robotics-2016"
    
Example:

    corytest@beaglebone:~/utk-robotics-2016$ vim ~/.bashrc
    <ADD THE LINE AT THE END>
    corytest@beaglebone:~/utk-robotics-2016$ source ~/.bashrc
    
Note that this entire step only needs to be done once. Next time you log in, you will not need to do this.

### Running the code

As stated before, at this point you will want to make sure that the robot is on a SAFE place on the GROUND. Running code can cause the robot to take off when you least expect it. You will not be very popular if you drive the robot off the desk.

Start by placing the robot in the start square with the front of the robot facing towards the blocks.

To run the current competition code, change to the the `utk-robotics-2016` directory and execute the following:

    python dominate.py
    
### Shelling into `spine`

Sometimes it is nice to have an interactive terminal for controlling the robot rather than having to run a script each time. To get a shell for controlling the robot, follow these instructions:

    corytest@beaglebone:~$ ipython
    Python 2.7.3 (default, Mar 14 2014, 17:55:54)
    Type "copyright", "credits" or "license" for more information.
    
    IPython 3.1.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.
    
    In [1]: import logging
    
    In [2]: from head.spine.core import Spine
    
    In [3]: fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
    
    In [4]: logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
    
    In [5]: s = Spine()
    07:21:46.325 - head.spine.core - INFO - Connecting to /dev/teensy.
    07:21:46.338 - head.spine.core - INFO - Created lock at /var/lock/LCK..teensy.
    07:21:46.345 - head.spine.core - INFO - Connecting to /dev/mega.
    07:21:46.359 - head.spine.core - INFO - Created lock at /var/lock/LCK..mega.
    07:21:46.366 - head.spine.core - INFO - Waiting for connection to stabilize.
    
    In [6]: s.startup() # To check the serial connections
    
    In [7]: # Run any spine command from here
    
    In [8]: s.close() # When you are done, you need to run this to close the serial connections and remove locks
    07:22:46.384 - head.spine.core - INFO - Closed serial connection /dev/teensy.
    07:22:46.390 - head.spine.core - INFO - Removed lock at /var/lock/LCK..teensy.
    07:22:46.400 - head.spine.core - INFO - Closed serial connection /dev/mega.
    07:22:46.408 - head.spine.core - INFO - Removed lock at /var/lock/LCK..mega.
    
    In [9]:
    Do you really want to exit ([y]/n)? y
    corytest@beaglebone:~$
