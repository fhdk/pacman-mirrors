# Change Log
All notable changes to this project will be documented in this file.

## [4.23.2] 2021-12-30
* [178](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/178)

## [4.23.1] 2021-12-02
* [#165](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/165)
* [#168](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/168)
* [#170](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/170)
* [#172](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/172)
* [#173](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/173)
* [#174](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/174)
* [#175](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/175)
* [#176](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/176)
* [#177](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/177)

## [4.21.1] 2021-04-19
* testing suggestion from issue [#163]((https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/163))

## [4.21.1] 2021-04-19
* add missing cleanup after ftp test
  (regression from issue [#160](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/160))

## [4.21.0] 2021-04-05
* issue [#160](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/160)

## [4.20.2] 2021-04-04
* issue [#158](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/158)
* issue [#159](https://gitlab.manjaro.org/applications/pacman-mirrors/-/issues/159)

## [4.20.0] 2021-03-20
* issue #157 - rechecked the timeout for urls - refactored to use only requests lib

## [4.19.3] 2021-03-14
* added `timeout=config["timeout"] to functions which did implement timeout

## [4.19.2] 2021-03-14
* Added check to validate the path supplied by argument `-a -p` e.g. -p mistaken for `-P https`

## [4.19.1]
* workaround for gtk initialization error on pinephone

## [4.19] 2020-12-02
* enhanced `-c/--country` argument
  - countries can be specified using country code or country name
  - further enhanced argument to accept lower case (any casing is accepted)
  - country specifications can be a mix of country code and country name
  - duplicate countries are removed

## [4.18.x]
* fix missed reference to i686

## [4.18] 2020-11-09
* remove 32-bit
* remove async
* prevent attempt to download data files if url in config is missing

## [4.17.1] 2020-09-29
* fix --interactive on arm - sway edition

## [4.16.3] 2020-03-03
* Fix typo

## [4.16.3] 2020-03-02
* Added **stable-staging** to the end of the branch list.

## [4.16.2] 2019-12-12
* Fixed missing reset of custom mirror pool when using `--continent` and `--geoip`

## [4.16] 2019-12-10
* Added `--continent` argument [#149](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/149)
* Added `--status` argument [#151](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/151)

## [4.15.1] 2019-10-22
* Fix bug in return value for `--geoip` argument
* Removed debug messages

## [4.15] 2019-10-19
* Refactor internal mirrorpool building - excluding mirros which are unresponsive or not up-to-date
* Experimental argument `--use-async`
  - @ZenTauro code added for [#144](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/144)
  - Overall functionality works - needs field testing.
  - Disclaimer before run.

## [4.14.99.dev] 2019-04-25
* Implemented [#146](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/146)
  - Added `--interval`. Works only with `--no-status` filtering mirrors based on last sync time.
* Fixed [#145](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/145)

## [4.14.2] 2019-04-22
* pulled transifex translation
* updated documentation (man page)

## [4.14.1] 2019-01-03
* new geo location service

## [4.14.0] 2018-10-29
* refactor geo location query to use geoip.kde.org

## [4.13.0] 2018-10-28
* Implemented [#143](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/143)
  - Added `--no-color` argument for Pamac v7.2 logging.
  - Pulled translations
  - Fixed doubled messages when using `-f` argument

## [4.12.5] 2018-08-06
* fix issue with console ui

## [4.12.4] 2018-08-06
* rebuild - removed debug code

## [4.12.3] 2018-08-06
* changed test file to `core.db.tar.gz` - added option to `pacman-mirrors.conf`

## [4.12.2] 2018-08-02
* fix sorting based on resp_time (lexicographic -> numbers)

## [4.12.1] 2018-08-01
* refactor mirror probe to get more realistic response times.
* setting http User-Agent to Pacman-Mirrors/{version}

## [4.11.5] 2018-07-24
* Fix for [#140](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/140)
* Fix issue for when user had configured protocol limitations - servers with invalid certificates was still written to the mirrorlist.

## [4.11.4] 2018-07-23
* Fix for [#139](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/139)
* Fixed interactive mirrorlist still containing https on invalid certificate

## [4.11.3] 2018-07-22
* Fix for [#138](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/138)
* Mirrors offering both https and http - with expired/invalid certifcate was written to mirrorlist with https protocol instead of http.
* Pulled translation from Transifex

## [4.11.2]
* Final build with fix for [#136](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/136)
* The change of call to gettext in the i18n module to return unicode messages fixed the issue.

## [4.11.1dev]
* Attempt to fix [#136](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/136)
* The issue manifests when the translation makes use of unicode chars (Hungarian) maybe others
* The call to gettext in the i18n module has been changed to return unicode messages.

## [4.11.0] 2018-06-22
* Added       : Implemented issue [#135](https://gitlab.manjaro.org/applications/pacman-mirrors/issues/135)
* Description : A non-reponsive mirror is eliminated from the mirrorlist
*             : If a mirror is blacklisted in the systems hosts file the mirror becomes unresponsive

## [4.10.1] 2018-04-01
* Added       : Implemented issue [#128](https://github.com/manjaro/pacman-mirrors/issues/128)
* Description : `-s/--no-status` Allow mirror list with not up-to-date mirrors

## [4.9.1] 2018-03-23
* Fixed  : [#130](https://github.com/manjaro/pacman-mirrors/issues/130) Mirror list generation could result in weird destinations if user selected multiple protocols from same mirror.

## [4.9.0] 2018-03-23
* Added  : `-lc/--country-config` (Pamac [#366](https://github.com/manjaro/pamac/issues/366))

## [4.8.2] 2018-03-19
* Fix: Github [#123](https://github.com/manjaro/pacman-mirrors/issues/123).

## [4.8.1] 2018-03-19
* Trying to squash a bug with help from community. Github [#123](https://github.com/manjaro/pacman-mirrors/issues/123).
* The issue was hard to pin down, but with the help of a fantastiq community it has been done.

## [4.8.0] 2018-03-19
* Remove : `--branch` - temporary branch change removed [System Maintenance](https://wiki.manjaro.org/System_Maintenance) [Forum Post](https://forum.manjaro.org/t/wiki-pacman-mirrors-pacman-4-7-6-recommendations-for-maintenance-and-installation/41991/16)
* Change : `--get-branch` not dependent on api [#124](https://github.com/manjaro/pacman-mirrors/issues/124) and [#125](https://github.com/pacman-mirrors/issues/125)
* Check  : `--api` is present with api args -> args error -> exit(1)
* Check  : `--interactive` is present with `--default` -> args error -> exit(1)
* Added  : translation texts for args error
* Updated: changelog, translations, documentation and tests

## [4.7.6] 2018-03-08
* Updated docs
* Updated translations

## [4.7.5] 2018-02-14
* Refactor to handle x32 correct so pool is not empty

## [4.7.4] 2018-02-13
* Fix for uncaught IndexError when mirror pool is empty [Forum post](https://forum.manjaro.org/t/pacman-mirrors-4-7-3-1-problems/40319/4)

## [4.7.3] 2018-02-11
* Added the missed the x32-branches [Forum post](https://forum.manjaro.org/t/pacman-mirrors-4-7-2-config-file-sanity-check-and-fix-of-my-staring-blind/40171/9)

## [4.7.2] 2018-02-10
* Added sanity check to config entries [Forum post](https://forum.manjaro.org/t/solved-struggling-to-change-permanently-from-stable-to-testing/40128)

## [4.7.1] 2018-01-28
* Wayland check - disable gtk on wayland compositor [#115](https://github.com/manjaro/pacman-mirrors/issues/115)
* Added catch for generic network errors not otherwise caught [#119](https://github.com/manjaro/pacman-mirrors/issues/119)
* Pulled translations

## [4.7.0] 2017-12-08
* Support for x32 branches - transparent change to x32
  - Check if architecture is i686 and change branch to x32-$branch
  - b/--branch and -a/--api -S/--set-branch
    - no need to prepend when calling branch changing functions

## [4.6.9] 2017-12-06
* **Improvement**: support for x32 branches [#114](https://github.com/manjaro/pacman-mirrors/issues/114)

## [4.6] 2017-11-19
* **Release bump to 4.6** Error with version display 4.5b1

## [4.5.0] 2017-11-16
* **Fix**: Custom mirror pool was not reset when supplying new countries on CLI.
* **Documentation**: Added file overview to documentation and man page.
* Discussion on a pamac incompatibility [pamac issue 366](https://github.com/manjaro/pamac/issues/366) and how to solve it properly.

## [4.5b1] 2017-11-09
After releasing 4.4 a couple of small trivial issues surfaced.
* **Fix**: Network check was handled poorly in corner cases.
* **Fix**: Reset of a custom mirror pool failed in corner cases.
* **Fix**: Country list was not complete.
* **Change**: OnlyCountry removed from configuration to avoid confusion.
* **Added**: Check for custom mirror pool by checking and validating custom-mirrors.json.

## [4.4] 2017-11-07
* **Improvement**: `-f/--fasttrack` honor `-c COUNTRY,COUNTRY,COUNTRY`
* **Change**: `-c/--country` countries supplied will be written to `custom-mirrors.json`, overwriting exiting file.

## [4.3.1] 2017-11-07
* **Fix**: typo in documentation

## [4.3.0] 2017-10-28
- **Fix**: `-h/--help` added deprecation messages
- **Improvement**: Api `--get-branch` removed root requirement
- **Deprecation**: `-y` and `-g` is deprecated and use is discouraged
- **Improvement**: General mirrorlist uses only up-to-date mirrors on users branch
- **Improvement**: Fasttrack mirrorlist uses only up-to-date mirrors on users branch
- **Improvement**: Filter generated mirrorlist based on branch and sync status
- Update translations.

## [4.2.2]
- **Fix**: Missing txt 'OPT_COUNTRY'

## [4.2.1] 2017-08-16
- Ensure correct exit code (0) on `api --get-branch`

## [4.2.0] 2017-06-14
- **Improvement**: Added `-U` / `--url` [#105](https://github.com/manjaro/pacman-mirrors/issues/105).
- **Improvement**: Added `-R`/`--re-branch` [#105](https://github.com/manjaro/pacman-mirrors/issues/105).
- **Improvement**: Added man page.

**Breaking changes**
- `-S`/`--set-branch $BRANCH` requires branch as argument.
- `-u`/`--update` renamed to `-y`/`--sync`.
- `NoUpdate` configuration removed from pacman-mirrors.conf.
- `--no-update` argument removed.
- `MirrorlistsDir = /etc/pacman.d/mirrors` removed from pacman-mirrors.conf.
- `-o`/`--output` argument removed.
- `OutputMirrorlist = /etc/pacman.d/mirrorlist` removed from pacman-mirrors.conf
- `-d`/`--mirror_dir` argument removed.

**Other improvements and fixes:**
- **Improvement**: Do not write bad servers to the end of the mirrorlist.
- **Improvement**: created argument groups for logic division of arguments usage.
- **Improvement**: `-G`/`--get-branch` and `-S`/`--set-branch` mutually exclusive.
- **Improvement**: `-n`/`--no-mirrorlist` and `-y --sync` mutually exclusive.
- **Improvement**: added choices to `-P`/`--proto` [all, http, https, ftp, ftps].
- **Improvement**: sorting mirrorlist by country during load of data file.
- **Fix**: Bug where ssl-certificate errors would break execution.
- **Fix**: Issue where values from configuration was not parsed correct.
- **Fix**: Issue where location in config was not determined correct.

## [4.1.4] 2017-05-16
- Improvement: Removed `--no-mirrorlist` dependency on API.
- Fix: Behavior of `--no-mirrorlist`. Download updated mirror files before exit.

## [4.1.3] 2017-05-15
- Fix: comparison of mirrorfiles fixed

## [4.1.2] 2017-05-15
- Fix: ranking breaks when `--interactive` is used with `--default` [#98](https://github.com/manjaro/pacman-mirrors/issues/98)

## [4.1.1] 2017-05-01
- Added `-u` / `--update` option
  * Run `pacman -Syy` after mirrorlist generation
- Modified network check so a single site failure is not considered network failure.

## [4.1.0] 2017-05-01
- Added protocol option to api.
  * Possible to control protocols from CLI
- `/var/lib/pacman-mirrors/mirrors.json` is causing confusion so it has been removed.
  * Only one fallback is needed `/usr/share/pacman-mirrors/mirrors.json`.
  * If a new `mirrors.json` is available - existing will be updated by pacman-mirrors.
- Improvement on default mirrorlist.
  * mirror protocols are reverse sorted (https,http,ftps,ftp).
  * if several protocols exist only the first is written to mirrorlist. Thus ssl enabled protocols get priority.
- Improvement on mirror protocol selection [#90](https://github.com/manjaro/pacman-mirrors/issues/90).
  * If a mirror offers more than one protocol - only the first is written to the mirrorlist.
  * Added `# Protocols = ` to pacman-mirrors.conf.
  * Defined protocols are honored in the order in which they appear.
- Improvement on `--interactive`: select mirrors by protocol.
- Added a simple API [#81](https://github.com/manjaro/pacman-mirrors/issues/81).
- Update translations.
- Code optimizing.
- Added to config `# SSLVerify = True`.
- Refactored mirrorcheck to ignore a mirrors certificate error if `SSLVerify = False`.
- Refactored mirrorcheck for https-mirrors timing out during ssl-handshake.
- Update docs.

## [4.0.4] - 2017-04-15
- Fix issue with UnicodeEncodeError in interactive mode

## [4.0.3] - 2017-03-28
- Fix issue with `--fasttrack` and `OnlyCountry = Custom`.
- Update translations.
- Update docs.

## [4.0.2] - 2017-03-21
- Fix issue with chroot mirrorlist generation

## [4.0.1] - 2017-03-21
- GUI: Add sorting functionality.
- Add: --default argument
- Fix issue with OnlyCountry unexpected reset
- Fix issue with not only displaying selected mirrors.
- Fix connectivity check.
- Update translations.

## [4.0.0] - 2017-03-19
- Add: -l/--list Print available mirror countries
- Add: Network check; do not run rank if no internet.
- Add: -f/--fasttrack [n] argument.
- Modified GUI and TUI to reflect rank/random method.
- Colorized console output by message type.
- Internal rewrite to use json files from repo.manjaro.org.
- The `/etc/pacman.d/mirrors` dir has been removed.
  - All data files now exist in `/var/lib/pacman-mirrors`.
  - If the `Custom` mirrorfile exist it will convert to `custom-mirrors.json`
- A lot of inevitable small fixes.

## [3.2.2] - 2017-02-12
- Fix issue with multiple country select.
- Bug fixes.

## [3.2.1] - 2017-02-10
- Fix save of config file.
- Update translations.

## [3.2.0] - 2017-02-06
- Add TUI interface.
- Bug fixes.
- Update translations.

## [3.1.0] - 2017-01-18
- Replace --verbose option by --quiet.
- New documentation.
- Translation review.
- Check DISPLAY when using interactive mode.
- Better structure for the GUI.

## [3.0.0] - 2017-01-12
- Refactoring.
- New GUI.
- Code improvements.
- --verbose option.

## [2.0.0] - 2016-03-01
- Add translation support.
- Better error messages.
- --no-update option, to prevent updates when upgrading the package.
- Big refractor of code.
- Configuration file /etc/pacman-mirrors.conf is optional.
- Pep8 all the code in pacman_mirrors.py
- Reestructure the project.
- The Custom country created with interactive mode is now stored in /var/lib/pacman-mirrors/
- If a Custom country is found in /etc/pacman.d/mirrors/ its moved automatically to the new directory.
