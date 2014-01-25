###Clone Repo
go to https://github.storm.gatech.edu/settings/ssh

we need to generate ssh key before using git

Let's go to your local machine

open up a terminal and type ssh-keygen

i.e.

Enter file in which to save the key (/home/user/.ssh/id_rsa): /home/user/.ssh/id_rsa_senior_design_git

cat id_rsa_senior_design_git.pub

copy that content to https://github.storm.gatech.edu/settings/ssh
#### edit .ssh/config
now edit the ~/.ssh/config

Add the following lines to it

```
Host 4911
    HostName github.storm.gatech.edu
    User git
    IdentityFile ~/.ssh/id_rsa_senior_design_git
```
Connect to the Gatech VPN (if off campus)

After that we can actually git clone the repository
either using
* ```git clone git@github.storm.gatech.edu:jlee850/HumorGenomeWebApp.git```
* ```git clone 4911:jlee850/HumorGenomeWebApp.git```

Now you should have your git repository in your local
###Add new file
Okay, let's change our directory to HumorGenomeWebApp

You should only see one master branch right now.

Let's make dev branch out of master branch for this repo

git checkout -b dev

Before we do anything let's put our names in this repo

`git config --local user.email "lindong@gatech.edu"`

`git config --local user.name "Lin Dong"`

Ignore this if you dont use vim

`git config --global core.editor "vim"`

And let's add git_tutorial.md to this directory
i.e.
touch git_tutorial.md
And let git keep track of it

`git add git_tutorial.md`

Now let's commit it to our repo
`git commit -a`

Type the comments in the poped window.

If you ever run into problem like asking
```
warning: push.default is unset; its implicit value is changing in
Git 2.0 from 'matching' to 'simple'. To squelch this message
and maintain the current behavior after the default changes, use:

  git config --global push.default matching

To squelch this message and adopt the new behavior now, use:

  git config --global push.default simple

See 'git help config' and search for 'push.default' for further information.
(the 'simple' mode was introduced in Git 1.7.11. Use the similar mode
'current' instead of 'simple' if you sometimes use older versions of Git)
```
just pick one you like  

`git config --global push.default matching`

`git config --global push.default simple`

###Push to repo
using 
`git push`
to add it the remote repo

if this is the first time push a new branch to remote branch, in this case, there's no dev at the github. We have to use

* `git push --set-upstream origin/dev dev &amp;&amp; git push`

* `git push origin dev`

####If you have any question, just let me know.

