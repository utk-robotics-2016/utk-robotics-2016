[![Circle CI](https://circleci.com/gh/utk-robotics-2016/utk-robotics-2016.svg?circle-token=54928279bf95f8682260893ee69e4ad5cc5ea3a3)](https://circleci.com/gh/utk-robotics-2016/utk-robotics-2016)

# utk-robotics-2016

Here are the steps that will get you coding as fast as possible:

### Reading

Before jumping in, skim through the [Robot overview](../../wiki/Robot-overview), [Beaglebone](../../wiki/Beaglebone), and [Contributing to Software](../../wiki/Contributing-to-Software) sections of the wiki. They will give you all the basic info, as well as information on getting set up with accounts on the Beaglebone.

### Setting up the git repo

Once you have connected to the Beaglebone through the instructions provided in [Beaglebone](../../wiki/Beaglebone), you first need to set up your private/public keypairs, which are not created automatically when your account is set up. In the BBB's shell,

    ssh-keygen -t rsa -b 4096 -C "YOUR_GITHUB_EMAIL"

Follow the prompts. The password does not need to be your Github password, and you can choose not to have one. You will now have key files located in `~/.ssh`. Now run

    cat ~/.ssh/id_rsa.pub

And copy the output to your clipboard. Next, follow the steps at https://help.github.com/articles/generating-ssh-keys/#step-4-add-your-ssh-key-to-your-account to add the SSH key to your Github account. You can now

    git clone git@github.com:utk-robotics-2016/utk-robotics-2016.git

To get this repository in your home directory. You will be on the `master` branch by default. As explained in [Contributing to Software](../../wiki/Contributing-to-Software), feel free to look around in master, but do not commit any changes directly to it. You will make changes in your own branch. Please consult [Contributing to Software](../../wiki/Contributing-to-Software) for instructions on how to do that.
