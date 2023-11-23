% pacman-mirrors(8) Pacman-Mirrors 4.x User Manual
%
% April, 2019

# NAME

pacman-mirrors - generate pacman mirrorlist for Manjaro Linux

# SYNOPSIS
```
 pacman-mirrors [-h] [-f [NUMBER]] [-i [-d]] [-m METHOD] [--status]
                [-c COUNTRY [COUNTRY...] | [--geoip] | [--continent]]
                [-l] [-lc] [-q] [-t SECONDS] [-v] [-n]
                [--api] [-S/-B BRANCH] [-p PREFIX]
                        [-P PROTO [PROTO...]] [-R] [-U URL]
```

# DESCRIPTION

Generates mirrorlist with up-to-date mirrors for Manjaro Linux.
Default is to rank all mirrors by reponse time.
If no arguments are given pacman-mirrors lists available options.
Pacman-mirrors requires access to files which are read-only
so it must be run with *su* or *sudo*.

To create a mirrorlist using all default use

    pacman-mirrors -f

The mirrorlist generation process can be refined through arguments
and arguments with options, for example

    pacman-mirrors --country Denmark --timeout 5

# IMPORTANT
After all operations *ALWAYS* syncronize and update your system with

    sudo pacman -Syyu

# OPERATION
Pacman-mirrors tries to provide **ONLY** up-to-date mirrors **if** they
are available in your chosen mirror pool. This means - at any given time -
the number of available mirrors will vary depending on when the mirror
last syncronized with the master repo server. If no up-to-date mirrors
is available in your chosen mirror pool, your mirror list will not be changed.
This behavior can be overridden if so desired by using the *-s/--no-status* switch.

# NETWORK CONNECTION
To be able to download the latest status file from repo.manjaro.org
pacman-mirrors verifies network connection by opening up to
three different websites. These sites are

1. repo.manjaro.org
2. github.com
2. bitbucket.org

The sites are chosen due to their generic nature and general availability.

# MIRROR RANKING
The mirrors are ranked by means of downloading a file from the systems core repo.
The file defaults to *core.db.tar.gz* but can be customized using the corresponding
entry in the configuration file.

## MODES

1. The number of mirrors
   * pacman-mirrors -f [number]
2. More control (custom mirror pool)
   * -c COUNTRY[[,COUNTRY]...]
   * --continent
3. Full control (custom mirror pool)
   * -i [-d/--default]

## FILES OVERVIEW

* **The configuration**: *`/etc/pacman-mirrors.conf`*
   * The file holds configuration for pacman-mirrors.
* **The mirrorlist**: *`/etc/pacman.d/mirrorlist`*
   * The file contains a number of servers which `pacman` uses to update your system.
* **Manjaro mirror pool with status**: *`/var/lib/pacman-mirrors/status.json`*
   * The mirrorpool status file.
   * It is the data you see displayed at mirror-manager.manjaro.org.
   * The file is downloaded and saved on every run of pacman-mirrors.
* **Custom mirror pool**: *`/var/lib/pacman-mirrors/custom-mirrors.json`*
   * The file is your custom mirror pool
   * It is created using **`-i/--interactive`** or **`-c/--country`** argument.

If you are stunned by this message

    .: WARNING No mirrors in selection
    .: INFO The mirrors has not changed

This is not an error, it is a feature.
The reason: You have limited your mirror pool too much and none of your selected mirrors are up-to-date.

**Suggested solutions**:

* Remove limitations on countries and/or protocols
* Do a complete reset of your list with *`pacman-mirrors -c all -aP all`*

## GENERAL INFO ABOUT ARGUMENTS
Some options are mutual exclusive and will throw an arguments error:

* **--country**, **--fasttrack**, **--geoip**, **--continent**

Some arguments require another argument present to have effect.
If such conditions rise pacman-mirrors will throw an argument error.

The arguments can appear in any order except for arguments which takes additional options
in which case the options must follow immediately after the argument with or without space,
for example

    pacman-mirrors -f
    pacman-mirrors -f 5
    pacman-mirrors -f5

Pacman-mirrors always attempt to download the lastest available data
from [http://repo.manjaro.org](http://repo.manjaro.org).
These data is always used during mirrorlist generation to ensure
that you connect to a mirror which is up-to-date for your systems branch.

# ARGUMENTS, METHODS AND OPTIONS

## METHODS
-g
:   Generic default run command. Will use custom mirror pool if defined.

-c, \--country *COUNTRY* [[*COUNTRY*]...]
:   Creates a custom mirror pool with supplied countries.

--continent
:   Creates a custom mirror pool from geolocation

-f, \--fasttrack [*NUMBER*]
:   Generates a random mirrorlist for the users current selected branch,
mirrors are randomly selected from the users current mirror pool,
either a custom pool or the default pool,
the randomly selected mirrors are ranked by their current access time.
The higher number the higher possibility of a fast mirror.
If a number is given the resulting mirrorlist contains that number of servers.

\--geoip
:   Use geolocation. If not possible use defined mirror pool. Custom pool if defined

-i, \--interactive [--default]
:   This is a function designed to leave full control over countries,
mirrors and protocols to the user. This function **DOES NOT**
take into consideration up-to-date mirrors.
The optional **--default** forces pacman-mirrors to load the default
mirror file and ignore any preset custom pool,
thus allowing for reselecting mirrors for a new custom pool.

## API

-a, \--api
:   Mandatory to process API options.

-B, -S, \--set-branch *BRANCH*
:   Permanent change branch, using *stable*, *testing* or *unstable*.

-p, \--prefix *PREFIX*
:   Add a path prefix to pacman-mirrors file-handling eg. */mnt/install* or *$mnt*.

-P, \--proto, \--protocols *PROTO* [*PROTO*] ...
:   Write protocols to configuration,  using *all* or *http*, *https*, *ftp* and *ftps*.

-R, \--re-branch
:   Replace branch in mirrorlist.

-U, \--url *URL*
:   Replace mirrorlist with supplied url.

## MISC

-G, \--get-branch
:   Return branch from configuration.

-h, \--help
:   Show the help message.

-l, \--list, \--country-list
:   Lists available mirror countries.

-lc, \--country-config
:   Lists custom selected countries.

-m, \--method *METHOD*
:   Default method is *rank* but *random* can be selected.

-n, \--no-mirrorlist
:   Use to skip generation of mirrorlist.

\--no-color
:   Suppress colorized messages.

-q, \--quiet
:   Make pacman-mirrors silent.

\--status
:   Print status for mirrors in system mirror list

\--interval
:   Apply a filter based on elapsed hours since last sync.

-t, \--timeout *SECONDS*
:   Change the number of seconds waiting for a server response,
SSL enabled mirrors has this value doubled to compensate for
the time spent on exchanging encryption keys.

-v, \--version
:   Show the version of pacman-mirrors.

## Exit status:

    0     : OK
    1     : Problem with argument
    2     : Problem accessing systemfiles
    3     : Missing mirror file
    4     : Primary mirror not up-to-date
    5     : Invalid mirrors found
    BRANCH: Value from config

## Configuration flow of pacman-mirrors

At launch an internal default configuration is setup,
file configuration is applied then the commandline is parsed and applied.

## API arguments

The arguments modifies key elements of pacman-mirrors configuration according to the users needs.

The actions performed by the API are in strict order and performed *before any* other actions.
This also means that ordinary arguments supplied in conjunction with api might be ignored.
Eg. **-U** argument terminates pacman-mirrors when branch and mirrorlist has been written.

1. If *p*  *PREFIX*
   *  add *PREFIX* to internal file configuration
2. If *-S/-B* *BRANCH*
   * apply *BRANCH* to internal configuration
   * replace branch in pacman-mirrors.conf with *BRANCH*
3. If *-U* *URL*
   * apply internal configuration to a mirrorlist with *URL*
   * *sys.exit(0)*
4. If *-P* *PROTO* [*PROTO*] ...
   * replace protocols in pacman-mirrors.conf with *PROTO*
5. If *-R*
   * replace branch in mirrorlist with *-S/-B* *BRANCH*

When done pacman-mirrors checks the internet connection and
if possible download the latest datafiles for creating the mirrorlist.
At this point it is possible to interrupt further processing.

If the *-n/--no-mirrorlist* argument is present pacman-mirrors will now exit.

# EXAMPLES

Most optional arguments are self explaining others require explanation.
The API functions is mainly designed to help packagers and iso-builders.
However it can be of use for everyone because it takes the hazzle out of
editing your pacman-mirrors configuration.

## Commands

* Which countries has mirrors?

    *pacman-mirrors --country-list*

* Which countries in my custom mirror pool

    *pacman-mirrors --country-config

* What branch am I on

    *pacman-mirrors --get-branch*

## Commands requiring sudo

* I want to permanently change branch to unstable,
* I want to use mirrors from Germany and France,
* I want only https and http protocol in that order

    *sudo pacman-mirrors --country Germany,France --api --set-branch unstable --procotol https http*

* Create a mirrorlist with German mirrors

    *sudo pacman-mirrors --country Germany*

* If you want more countries in your mirrorlist add them they will be written to your custom mirror pool

    *sudo pacman-mirrors --country Germany France Denmark*

* Create a mirrorlist with 5 mirrors up-to-date on your branch

    *sudo pacman-mirrors --fastrack 5*

* I want to choose my mirrors

    *sudo pacman-mirrors --interactive*

* I have a custom mirror list and I want to create a new custom mirror list?

    *sudo pacman-mirrors --interactive --default*

* I have a custom mirror list - can I reset it?

    *sudo pacman-mirrors --country all*

## Advanced use samples - BEWARE OF THE DRAGONS
* Change system branch and do not change the mirrorlist

    *sudo pacman-mirrors -naS unstable*

* Change system branch and replace branch in mirrorlist and quit

    *sudo pacman-mirrors -naRS unstable*

* Change protocols you will accept but do not change the mirrorlist

    *sudo pacman-mirrors -naP https http*

* A packager can write directly to a mounted systems datafiles using either a path or an environment variable replacing the branch in both configuration and mirrorlist leaving the mirrors as is

    *sudo pacman-mirrors -anR -p $prefix -S $branch -P https*

* It is also possible to specify a mirror in which case the mirrorlist is created and pacman-mirrors terminate

    *sudo pacman-mirrors -ap $prefix -S $branch -U $url*

# DEFAULT CONFIGURATION

    ##
    ## /etc/pacman-mirrors.conf
    ##

    ## Branch Pacman should use (stable, testing, unstable)
    # Branch = stable

    ## Generation method
    ## 1) rank   - rank mirrors depending on their access time
    ## 2) random - randomly generate the output mirrorlist
    # Method = rank

    ## Filename to use when ranking mirrors
    ## The file must be present in core repo
    # TestFile = core.db.tar.gz

    ## Define protocols and priority
    ##   separated by comma 'https,http' or 'http,https'
    ## ATM available protocols are: http, https, ftp
    ## Not specifying a protocol will ban the protocol from being used
    ## If a mirror has more than one protocol defined only the first is written to the mirrorlist
    ## Empty means all in reversed alphabetic order
    # Protocols =

    ## When set to False - all certificates are accepted.
    ## Use only if you fully trust all ssl-enabled mirrors.
    # SSLVerify = True

    ## Set a static mirror to be used instead of the official mirror pool
    ## e.g. Static = https://domain.tld/manjaro/
    # Static =


# MORE INFO
* [https://wiki.manjaro.org/index.php?title=Pacman-mirrors](https://wiki.manjaro.org/index.php?title=Pacman-mirrors)
* [https://wiki.manjaro.org/index.php?title=Create_your_own_Custom_Mirrorlist](https://wiki.manjaro.org/index.php?title=Create_your_own_Custom_Mirrorlist)

# REPORTING BUGS
   [https://gitlab.manjaro.org/applications/pacman-mirrors/issues](https://gitlab.manjaro.org/applications/pacman-mirrors/issues)

# SEE ALSO

The pacman-mirrors source code and all documentation may be downloaded from [https://gitlab.manjaro.org/applications/pacman-mirrors/](https://gitlab.manjaro.org/applications/pacman-mirrors/)

# AUTHORS

    Esclapion <esclapion@manjaro.org>
    philm <philm@manjaro.org>
    Ramon Buldó <rbuldo@gmail.com>
    Hugo Posnic <huluti@manjaro.org>
    Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>
