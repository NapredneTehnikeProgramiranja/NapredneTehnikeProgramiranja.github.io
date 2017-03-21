#!/usr/bin/python
# coding: utf-8

"""
This script maintains installation for all needed packages at
"Napredne tehnike programiranja" class. It works for Ubuntu >= 14.04 ONLY.

Tested only with:
- ubuntu/trusty64 vagrant box [https://atlas.hashicorp.com/ubuntu/boxes/trusty64/versions/20170220.0.1]
"""

__author__ = "Novak Boškov"
__copyright__ = "Copyright 2017, Novak Boškov"
__credits__ = []
__license__ = "GPL 3"
__version__ = "0.0.1"
__maintainer__ = "Novak Boškov"
__email__ = "gnovak.boskov@gmail.com"

import socket, os, subprocess

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def info(m):
    print(tcolors.OKBLUE + m + tcolors.ENDC)
def success(m):
    print(tcolors.OKGREEN + m + tcolors.ENDC)
def warn(m):
    print(tcolors.WARNING + m + tcolors.ENDC)
def error(m):
    print(tcolors.FAIL + m + tcolors.ENDC)
def bold(m):
    print(tcolors.BOLD + m + tcolors.ENDC)

def call(command, concurrent=False, output=False, sudo=True):
    """
    Execute shell command.
    """
    opts = {'shell': True}

    if sudo:
        command = "sudo " + command

    if not output:
        opts['stdout'] = open(os.devnull, 'w')
        opts['stderr'] =  subprocess.STDOUT

    if concurrent:
        subprocess.call(command, **opts)
    else:
        subprocess.check_call(command, **opts)

def ensure_internet_connection():
    hostname = "www.google.com"
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), timeout=2)
    except:
        error("Unable to connect to " + hostname + "." + os.linesep +
              "Please check your internet connection.")
        exit()

def is_xorg_available():
    try:
        call("Xorg -version")
        return True
    except:
        info("You probably running Ubuntu without X server.")
        return False

if __name__ == "__main__":
    ensure_internet_connection()
    # ensure sudo
    call("/usr/bin/sudo /usr/bin/id", sudo=False)

    info("Napredne tehnike programiranja --- installer starts...")

    call("apt-get update", output=True)

    info("Install GNU/Emacs 25 from PPA.")
    call("add-apt-repository -y ppa:adrozdoff/emacs", output=True)
    call("apt-get update", output=True)
    call("apt-get -y install emacs25", output=True)
    success("Install GNU/Emacs 25 done.")

    info("Install Git")
    call("apt-get -y install git", output=True)
    success("Install Git done")

    info("Install Emacs Prelude distribution")
    call("rm -rf ~/.emacs.d")
    call("git clone git://github.com/bbatsov/prelude.git ~/.emacs.d")
    success("Install Emacs Prelude distribution done")

    info("Install OpenJDK 8 from PPA")
    call("add-apt-repository -y ppa:openjdk-r/ppa", output=True)
    call("apt-get update", output=True)
    call("apt-get -y install openjdk-8-jdk", output=True)
    success("Install OpenJDK 8 done.")

    info("Install Leiningen Clojure build tool.")
    call("wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein", output=True)
    call("chmod +x lein")
    call("mv lein /usr/local/bin")
    success("Install Leiningen Clojure build tool done.")

    info("Install Haskell with Stack")
    call("echo \"export PATH=$PATH:~/.local/bin\" >> ~/.profile")
    call("wget -O stack.sh https://get.haskellstack.org/", output=True)
    call("sh stack.sh --force", output=True)
    call("rm stack.sh")
    success("Install Haskell with Stack done.")

    info("Install Haskell Platform with ghc-prof")
    call("apt-get -y install haskell-platform ghc-prof", output=True)
    success("Install Haskell Platform with ghc-prof done.")

    # Installs Golang 1.8 but do not change GOPATH nor GOROOT if they're set.
    goroot, gopath = os.getenv("GOROOT"), os.getenv("GOPATH")
    goroot_new = gopath_new = ""
    info("Install Golang from official site.")
    warn("This may take few minutes.")
    call("wget https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz", output=True)
    call("tar -xvf go1.8.linux-amd64.tar.gz")
    call("rm -rf /usr/local/go")
    call("mv go /usr/local")
    call("rm go1.8.linux-amd64.tar.gz")

    if not goroot:
        goroot_new = goroot = "/usr/local/go"
        call("echo \"export GOROOT=%s\" >> ~/.profile" % goroot)
    if not gopath:
        gopath_new = gopath = os.getenv("HOME") + "/Go_NTP/test_project"
        call("echo \"export GOPATH=%s\" >> ~/.profile" % gopath)
    if gopath_new or goroot_new:
        call("echo \"export PATH=%s/bin:%s/bin:$PATH\" >> ~/.profile"
             % (gopath_new, goroot_new))

    success("Install Golang done.")

    # Tries to build Chez Scheme from source, pass if fails.
    chez = False
    info("Build Chez Scheme from source on Cisco GitHub.")
    if not is_xorg_available():
        warn("Chez Scheme won't be installed. It requires X server to build.")
    else:
        warn("This may take about 10 minutes due to building from source.")
        call("rm -rf ChezScheme")
        call("git clone git://github.com/cisco/ChezScheme.git", output=True)
        call("apt-get -y install libncurses5-dev libncursesw5-dev")
        os.chdir("ChezScheme")
        call("sh configure", output=True)
        try:
            call("make install", output=True)
            os.chdir("..")
            call("rm -rf ChezScheme")
            success("Install Chez Scheme done.")
            chez = True
        except:
            os.chdir("..")
            call("rm -rf ChezScheme")
            error("Chez Scheme building process failed.")

    info("Install Racket Scheme from PPA.")
    call("add-apt-repository -y ppa:plt/racket", output=True)
    call("apt-get update", output=True)
    call("apt-get -y install racket", output=True)
    success("Install Racket Scheme done.")

    bold(3*os.linesep + "Following software installed:" + os.linesep +
         "==> GNU/Emacs 25 from ppa:adrozdoff/emacs & Emacs Prelude by Bozhidar Batsov" + os.linesep +
         "==> Git" + os.linesep +
         "==> OpenJDK from ppa:openjdk-r/ppa" + os.linesep +
         "==> Leiningen Clojure build tool" + os.linesep +
         "==> Haskell Stack" + os.linesep +
         "==> Golang 1.8 (set GOPATH=%s and GOROOT=%s in ~/.profile)" % (gopath, goroot) + os.linesep +
         ("==> Chez Scheme from Cisco" + os.linesep if chez else "") +
         "==> Racket Scheme")
    success("Napredne tehnike programiranja --- installer done.")
    info("Please logout to complete installation.")
