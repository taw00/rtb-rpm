# rtb-rpm
**Rsync Time Backup** — a time-machine-style backup utility — packaged for Fedora, EL (RHEL/CentOS), and OpenSUSE

`rtb` is a command line driven backup utility leveraging the popular project,
_[rsync-time-backup](https://github.com/laurent22/rsync-time-backup)_ and its
extension _[rtb-wrapper](https://github.com/thomas-mc-work/rtb-wrapper)_. Under
the covers, _rsync_ does all the heavy-lifting. Backups are incremental where
same-files are maintained with hardlinks between backup trees. _rtb_ has many
similarities in concept to _backintime_, but is focused on simplicity.
Profiles can be defined for different backup scenarios.


### Installation:

```sh
# Initial installation of the COPR repository
sudo dnf copr enable taw/rtb
```

```sh
# Installation of rtb
sudo dnf install rtb
```

All `*.src.rpm` packages provided in rtb-rpm GitHub repository should be signed with [my GPG key](https://keybase.io/toddwarner/key.asc)<br />Binary packages are delivered by the COPR build system as enabled above. Those packages are signed with the [Fedora Project's](https://fedoraproject.org/) [COPR GPG signing key](https://download.copr.fedorainfracloud.org/results/taw/rtb/pubkey.gpg)

### The upstream projects

The underlying projects (upstream):
- https://github.com/laurent22/rsync-time-backup
- https://github.com/thomas-mc-work/rtb-wrapper

### My changes
`rtb` is essentially a symlink to `rtb-wrapper.sh` with two changes:
- The default configuration directory is `$HOME/.config/rtb` (instead of `$HOME/.rsync_tmbackup/`)
- The log directory is set to `$HOME/.local/log/rtb/` (instead of `$HOME/.rsync_tmbackup/`)

### How-To

1. First create the configuration directory:
```sh
mkdir -p $HOME/.config/rtb
```
2. Decide where you are backing things up to. Personally, I use the keybase
   filesystem, but for our example, we are using a folder in the
   `/tmp/mybackups` directory.
3. Create an initial backup profile: `$HOME/.config/rtb/home-documents.inc`
```text
SOURCE="$HOME/Documents"
TARGET="/tmp/mybackups/Documents"
EXCLUDE_FILE="$HOME/.config/rtb/home-documents.excludes.lst"
WIPE_SOURCE_ON_RESTORE=false
```
If that target was via ssh, it may look something like `TARGET="todd@myserver:some/backup/directory"`
4. Edit your master home directory excludes list:  
   `$HOME/.config/rtb/home.excludes.lst`  
   It might look something like this.
```diff
# home.excludes.lst — my home directory master list of excludes
# Assumption: SOURCE="$HOME"
#
# Documents -- We are backing up Documents separately in this example, see below
- /Documents/
#+ /Documents/*.pdf
#+ /Documents/*.txt
#+ /Documents/*.md
#+ /Documents/*.docx
#+ /Documents/*.odt
#- /Documents/*
#- /Documents/.*

# Never backed up
- /Downloads/
# /Applications that can be restored via passphrase and the cloud
- /.mozilla/
- /.config/google-chrome/
- /.local/share/keybase/

# Music -- back up all of it 
+ /Music/

# Atom -- keep the configuration and toss the rest
+ /.atom/*.cson
+ /.atom/*.coffee
+ /.atom/*.less
+ /.atom/*.package.list
- /.atom/*
- /.atom/.*

# SSH (critical)
+ /.ssh/
```

5. Create your documents excludes list 
   (`$HOME/.config/rtb/home-documents.excludes.lst`):
```diff
# home-documents.excludes.lst
# Assumption: SOURCE="$HOME/Documents"
# Certain things are explicitely permitted in this example and everything else
# is filtered from the backup. This will ignore directories and other
# structures.
+ *.pdf
+ *.txt
+ *.md
+ *.docx
+ *.odt
- *
- .*
```

6. Run it!
```sh
rtb backup home-documents
```

Note, run the first time, it will likely yell that you need to touch a
`backup.marker` file in the target directory. Do what the script does and run
it again. This is essentially an "are you sure?" step.

7. Restore it!
rtb restore home-documents

### More Information

For more information about rtb-wrapper, please visit <https://github.com/thomas-mc-work/rtb-wrapper>

For more information about rsync-time-backup, which this is all based off of,
please visit: <https://github.com/laurent22/rsync-time-backup>. That project's
README has more information about the **expiration logic** of the backups, more
about **how that exclusion file works**, etc. The hardest part of all this is
that darn exclusion file.  It's tricky to get just right.

Finally, the raw utilities live in `/usr/share/rtb/`, but for nearly all use
cases, you only need to use `/usr/bin/rtb`

### Enjoy

Contact information:
* My usernames in various social places: taw, taw00, and t0dd
* Email: Todd Warner <t0dd_at_protonmail.com>

