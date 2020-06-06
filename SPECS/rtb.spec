# rtb.spec
# vim:tw=0:ts=2:sw=2:et:
#
# rtb is rsync-time-backup and the rtb-wrapper extension all 
# rsync-time-backup is a neat project created by Laurent Cozic.
# rtb-wrapper is an extension to that projected created by Thomas McWork
# https://github.com/laurent22/rsync-time-backup
# https://github.com/thomas-mc-work/rtb-wrapper
#
# Specfile author: Todd Warner <t0dd_at_protonmail.com>
#
# Licensing:
#   - This rtb RPM and specfile: Mozilla Public License 2.0 (MPL 2.0)
#     Explained: https://choosealicense.com/licenses/mpl-2.0/
#   - rsync-time-backup: The MIT License (MIT)
#     Explained: https://choosealicense.com/licenses/mit/
#   - rtb-wrapper: Apache License 2.0
#     Explained: https://choosealicense.com/licenses/apache-2.0/
#
# ---
#
#
# Package (RPM) name-version-release.
#
# <name>-<version>-<release>
# ...version is (can be many decimals):
# <vermajor>.<verminor>
# ...where release is:
# <pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]
# ...all together now:
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]
#
# Note about the pattern for release iterations (ie. the release value of
# name-version-release):
#     If you are still in development, but the production package is expected
#     to have a release value of 8 (previous release was 7) for example, you
#     always work one step back (in the 7's) and add another significant digit.
#     I.e., release value of 7.1, 7.2, 7.3, etc... are all pre-production
#     release nomenclatures for an eventual release numbered at 8. When we go
#     into production, we "round up" and drop the decimal and probably all the
#     snapinfo as well.  specpattern-1.0.1-7.3.beta2 --> specpattern-1.0.1-8
#
# Source tarballs that I am using to create this...
# - specpattern-1.0.1.tar.gz
# - specpattern-1.0-contrib.tar.gz
#

Name: rtb
Summary: a time-machine-like incremental backup utility
#BuildArch: noarch

%define targetIsProduction 1

# VERSION - can edit
# eg. 1.0.1
%define vermajor 0.0
%define verminor 20191105
Version: %{vermajor}.%{verminor}

%define s0name rsync-time-backup
%define s0version 0.0.20191105
%define s1name rtb-wrapper
%define s1version 0.0.20190228

# RELEASE - can edit
%if %{targetIsProduction}
  %define _pkgrel 1
%else
  %define _pkgrel 0.1
%endif

# MINORBUMP - can edit
%undefine minorbump
%define minorbump taw

#
# Build the release string - don't edit this
#

# eg. 1 (prod) or 0.6.testing (pre-prod)
%define _snapinfo testing
%if %{targetIsProduction}
  %undefine _snapinfo
%endif
%if 0%{?_snapinfo:1}
  %define snapinfo %{_snapinfo}
%else
  %undefine snapinfo
%endif

# _pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# Extracted source tree example structure (extracted in {_builddir})
#   BUILD/sourceroot         BUILD/{name}-0.0
#         \_sourcetree0             \_{s0name}-0.0.20191105
#         \_sourcetree1             \_{s1name}-0.0.20190228
#         \_source_contrib          \_{name}-0.0-contrib (not in this RPM)
#   BUILDROOT/installtree    BUILDROOT/usr/share/{name}
%define sourceroot %{name}-%{vermajor}
%define sourcetree0 %{s0name}-%{s0version}
%define sourcetree1 %{s1name}-%{s1version}
%define source_contrib %{name}-%{vermajor}-contrib
%define installtree %{_datadir}/%{name}

Source0: https://github.com/taw00/rtb-rpm/raw/master/SOURCES/%{sourcetree0}.tar.gz
Source1: https://github.com/taw00/rtb-rpm/raw/master/SOURCES/%{sourcetree1}.tar.gz
#Source2: https://github.com/taw00/rtb-rpm/raw/master/SOURCES/%%{source_contrib}.tar.gz
BuildArch: noarch

Requires: rsync
BuildRequires: sed grep

# https://en.opensuse.org/openSUSE:Build_Service_cross_distribution_howto
# mock builds of suse don't include cacerts for some reason
%if 0%{?suse_version:1}
BuildRequires: ca-certificates-cacert ca-certificates-mozilla ca-certificates
%endif

#t0dd: for build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils dnf
%endif

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# https://spdx.org/licenses/ (these differ!?!)
License: MPL-2.0
URL: https://github.com/taw00/rtb-rpm

# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# ...flip-flop next two lines in order to disable (nil) or enable (1) debuginfo package build
%define debug_package 1
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_pie
%define _hardened_build 1


%description
rtb (leveraging rsync-time-backup and its rtb-wrapper extension) is a
time-machine-like backup utility. It leverages rsync to create incremental
backups managed using hardlinks between backup trees.  It has many similarities
in concept to backintime, but is focused on simplicity.  Profiles can be
defined for different backup scenarios.


%prep
# Prep section starts us in directory .../BUILD -or- {_builddir}

#rm -rf %%{sourceroot} ; mkdir -p %%{sourceroot}
mkdir -p %{sourceroot}
# sourcecode
%setup -q -T -D -a 0 -n %{sourceroot}
%setup -q -T -D -a 1 -n %{sourceroot}

# For debugging purposes...
%if ! %{targetIsProduction}
  cd .. ; /usr/bin/tree -df -L 1 %{sourceroot} ; cd -
%endif

%if 0%{?suse_version:1}
  echo "\
======== OpenSUSE version: %{suse_version} %{sle_version}
-------- Leap 15.1  will report as 1500 150100
-------- Leap 15.2  will report as 1500 150200
-------- Tumbleweed will report as 1550 undefined"
%endif

%if 0%{?fedora:1}
  echo "======== Fedora version: %{fedora}"
%if 0%{?fedora} < 31
  echo "Fedora 30 and older can't be supported. Sorry."
  exit 1
%endif
%endif

%if 0%{?rhel:1}
  echo "======== EL version: %{rhel}"
%if 0%{?rhel} < 7
  echo "EL 6 and older can't be supported. Sorry."
  exit 1
%endif
%if 0%{?rhel} >= 9
  echo "EL 9 and newer is untested thus far. Good luck."
%endif
%endif


##
## Building the RPM: prep --> build --> install --> files
##


%build
# This section starts us in directory {_builddir}/{sourceroot}

cd %{sourcetree0}
echo "\
MIT License

Copyright (c) Laurent Cozic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
" > LICENSE_rsync-time-backup_rsync_tmbackup
mv README.md README_rsync-time-backup_rsync_tmbackup.md
cd ..
cd %{sourcetree1}
mv LICENSE LICENSE-rtb-wrapper
mv README.md README-rtb-wrapper.md
cp -a rtb-wrapper.sh rtb-wrapper.orig.sh
sed -i.previous1 '{s+cmd="rsync_tmbackup.sh+cmd="'%{installtree}'/rsync_tmbackup.sh --log-dir '\''$HOME/.local/log/rtb'\''+}' rtb-wrapper.sh
# ' added here so that syntax highlighting works again. Poor confused vim.
sed -i.previous2 '{s+profile_dir="${config_dir}/conf.d"+profile_dir="${config_dir}"+}' rtb-wrapper.sh
sed -i.previous3 '{s+${HOME}/.rsync_tmbackup+${HOME}/.config/rtb+}' rtb-wrapper.sh
cd ..


%install
# This section starts us in directory {_builddir}/{sourceroot}

# Cheatsheet for built-in RPM macros:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix or _usr = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
# This is used to quiet rpmlint who cannot seem to understand that /usr/lib is
# still used for certain things.
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are already defined in newer versions of RPM, but not in el7
%if 0%{?rhel} && 0%{?rhel} < 8
%define _tmpfilesdir %{_usr_lib}/tmpfiles.d
%define _unitdir %{_usr_lib}/systemd/system
%define _metainfodir %{_datadir}/metainfo
%endif


# Create directories
# /usr/bin/
install -d -m755 -p %{buildroot}%{_bindir}
# /usr/share/rtb
install -d %{buildroot}%{installtree}

install -m755 %{sourcetree0}/rsync*.sh %{buildroot}%{installtree}
install -m755 %{sourcetree1}/rtb*.sh %{buildroot}%{installtree}

# Binaries - a little ugly - symbolic link creation
ln -s %{installtree}/rtb-wrapper.sh %{buildroot}%{_bindir}/%{name}

# Log files
# ...logrotate file rules
#install -D -m644 -p %%{sourcetree_contrib}/logrotate/etc-logrotate.d_%%{name} %%{buildroot}%%{_sysconfdir}/logrotate.d/%%{name}
# ...ghosted log files - need to exist in the installed buildroot
#touch %%{buildroot}%%{_localstatedir}/log/%%{name}/debug.log


%files
# This section starts us in directory {_buildrootdir} (I think)
# (note that macros like %%docs, %%licence, etc may locate in
# {_builddir}/{sourceroot})

%defattr(-,root,root,-)
%license %{sourcetree0}/LICENSE*
%doc %{sourcetree0}/README*
%license %{sourcetree1}/LICENSE*
%doc %{sourcetree1}/README*

# The directories...
# /usr/share/rtb/ and /usr/share/rtb/*
%{installtree}

# Binaries
%{_bindir}/%{name}

# Logs
# log file - does not initially exist, but we still own it
#%%attr(644,root,root) %%{_sysconfdir}/logrotate.d/%%{name}


##
## Installing/Uninstalling the RPM: pre, post, posttrans, preun, postun
##


%pre
# This section starts us in directory {_builddir}/{sourceroot}
# an installation step (runs right prior to installation)
# - system users are added if needed. Any other roadbuilding.



%changelog
* Sat Jun 06 2020 Todd Warner <t0dd_at_protonmail.com> 0.0.20191105-1.taw
* Sat Jun 06 2020 Todd Warner <t0dd_at_protonmail.com> 0.0.20191105-0.1.testing.taw
  - Initial build.
  - Config directory set to default to $HOME/.config/rtb
  - Log directory is set to default to $HOME/.local/log/rtb
