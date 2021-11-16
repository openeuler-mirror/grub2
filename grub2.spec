%undefine _hardened_build

%global tarversion 2.04
%define efi_vendor %{_vendor}
%undefine _missing_build_ids_terminate_build
%global _configure_gnuconfig_hack 0

Name:		grub2
Epoch:		1
Version:	2.04
Release:	21
Summary:	Bootloader with support for Linux, Multiboot and more
License:	GPLv3+
URL:		http://www.gnu.org/software/grub/
Source0:	https://ftp.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source1:	grub.macros
Source2:	grub.patches
Source4:	http://unifoundry.com/unifont-5.1.20080820.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore
Source7:        99-grub-mkconfig.install
Source9:	strtoull_test.c
Source10:	20-grub.install
Source11:	installkernel-bls
Source12:       installkernel.in

%include %{SOURCE1}
%include %{SOURCE2}

BuildRequires:  gcc efi-srpm-macros flex bison binutils python3 ncurses-devel xz-devel
BuildRequires:  freetype-devel libusb-devel bzip2-devel rpm-devel rpm-libs
BuildRequires:  autoconf automake autogen device-mapper-devel freetype-devel git
BuildRequires:  texinfo gettext-devel dejavu-sans-fonts help2man systemd fuse-devel

%ifarch %{golang_arches}
BuildRequires:	pesign >= 0.99-8
%endif
%if %{?_with_ccache: 1}%{?!_with_ccache: 0}
BuildRequires:	ccache
%endif

Obsoletes:  grub2 <= %{evr} grub < 1:0.98

%if 0%{with_legacy_arch}
Requires:	%{name}-%{legacy_package_arch} = %{evr}
%else
Requires:	%{name}-%{package_arch} = %{evr}
%endif

%{nil}

%description
GNU GRUB is a Multiboot boot loader. It was derived from GRUB, the GRand
Unified Bootloader, which was originally designed and implemented by
Erich Stefan Boleyn.

Briefly, a boot loader is the first software program that runs when a
computer starts. It is responsible for loading and transferring control
to the operating system kernel software (such as the Hurd or Linux). The
kernel, in turn, initializes the rest of the operating system (e.g. GNU).

%package common
Summary:	common package for grub2
BuildArch:	noarch
Conflicts:	grubby < 8.40-18

%description common
Common package for grub2.

%package        tools
Summary:    tools package for grub2
Requires:   grub2-common = %{epoch}:%{version}-%{release}
Requires:   gettext os-prober which file
Requires(pre):  dracut
Requires(post): dracut

%description    tools
tools package for grub2.

%package     tools-minimal
Summary:     Support tools for GRUB.
Requires:    gettext %{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:   grub2-tools < %{evr}

%description tools-minimal
Support tools for GRUB.

%package     tools-extra
Summary:     Support tools for GRUB.
Requires:    gettext os-prober which file
Requires:    %{name}-tools-minimal = %{epoch}:%{version}-%{release}
Requires:    %{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:   grub2-tools < %{evr}

%description tools-extra
Support tools for GRUB.

%ifarch x86_64
%package        tools-efi
Summary:        efi packages for grub2-tools
Requires:   grub2-common = %{epoch}:%{version}-%{release}
Requires:   gettext os-prober which file
Obsoletes:  grub2-tools < %{evr}

%description    tools-efi
Efi packages for grub2-tools.
%endif

%if 0%{with_efi_arch}
%{expand:%define_efi_variant %%{package_arch} -o}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%define_efi_variant %%{alt_package_arch}}
%endif
%if 0%{with_legacy_arch}
%{expand:%define_legacy_variant %%{legacy_package_arch}}
%endif

%if 0%{with_emu_arch}
%package emu
Summary:	GRUB user-space emulation.
Requires:	%{name}-tools-minimal = %{epoch}:%{version}-%{release}

%description emu
This subpackage provides the GRUB user-space emulation support of all platforms.

%package emu-modules
Summary:	GRUB user-space emulation modules.
Requires:	%{name}-tools-minimal = %{epoch}:%{version}-%{release}

%description emu-modules
This subpackage provides the GRUB user-space emulation modules.
%endif

%package_help

%prep
%do_common_setup
%if 0%{with_efi_arch}
mkdir grub-%{grubefiarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubefiarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubefiarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grubefiarch}-%{tarversion}
%endif
%if 0%{with_alt_efi_arch}
mkdir grub-%{grubaltefiarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubaltefiarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubaltefiarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grubaltefiarch}-%{tarversion}
%endif
%if 0%{with_legacy_arch}
mkdir grub-%{grublegacyarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grublegacyarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grublegacyarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grublegacyarch}-%{tarversion}
%endif
%if 0%{with_emu_arch}
mkdir grub-emu-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-emu-%{tarversion}/.gitignore
cp %{SOURCE4} grub-emu-%{tarversion}/unifont.pcf.gz
git add grub-emu-%{tarversion}
%endif
git commit -m "After making subdirs"

%build
%if 0%{with_efi_arch}
%{expand:%do_primary_efi_build %%{grubefiarch} %%{grubefiname} %%{grubeficdname} %%{_target_platform} %%{efi_target_cflags} %%{efi_host_cflags}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%do_alt_efi_build %%{grubaltefiarch} %%{grubaltefiname} %%{grubalteficdname} %%{_alt_target_platform} %%{alt_efi_target_cflags} %%{alt_efi_host_cflags}}
%endif
%if 0%{with_legacy_arch}
%{expand:%do_legacy_build %%{grublegacyarch}}
%endif
%if 0%{with_emu_arch}
%{expand:%do_emu_build}
%endif
makeinfo --info --no-split -I docs -o docs/grub-dev.info docs/grub-dev.texi
makeinfo --info --no-split -I docs -o docs/grub.info docs/grub.texi
makeinfo --html --no-split -I docs -o docs/grub-dev.html docs/grub-dev.texi
makeinfo --html --no-split -I docs -o docs/grub.html docs/grub.texi

%check
pushd %{_builddir}/%{?buildsubdir}/grub-%{grubefiarch}-%{tarversion}/grub-core
make check
popd

%install
set -e

%do_common_install
%if 0%{with_efi_arch}
%{expand:%do_efi_install %%{grubefiarch} %%{grubefiname} %%{grubeficdname}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%do_alt_efi_install %%{grubaltefiarch} %%{grubaltefiname} %%{grubalteficdname}}
%endif
%if 0%{with_legacy_arch}
%{expand:%do_legacy_install %%{grublegacyarch} %%{alt_grub_target_name} 0%{with_efi_arch}}
%endif
%if 0%{with_emu_arch}
%{expand:%do_emu_install %%{package_arch}}
%endif
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
ln -s %{name}-set-password ${RPM_BUILD_ROOT}/%{_sbindir}/%{name}-setpassword
echo '.so man8/%{name}-set-password.8' > ${RPM_BUILD_ROOT}/%{_datadir}/man/man8/%{name}-setpassword.8

%ifnarch x86_64
rm -vf ${RPM_BUILD_ROOT}/%{_bindir}/%{name}-render-label
rm -vf ${RPM_BUILD_ROOT}/%{_sbindir}/%{name}-bios-setup
rm -vf ${RPM_BUILD_ROOT}/%{_sbindir}/%{name}-macbless
%endif

%find_lang grub

install -d %{buildroot}%{_sysconfdir}/prelink.conf.d/

pushd %{buildroot}%{_sysconfdir}/prelink.conf.d/
cat << EOF > grub2.conf
# these have execstack, and break under selinux
-b /usr/bin/grub2-script-check
-b /usr/bin/grub2-mkrelpath
-b /usr/bin/grub2-mount
-b /usr/bin/grub2-fstest
-b /usr/sbin/grub2-bios-setup
-b /usr/sbin/grub2-probe
-b /usr/sbin/grub2-sparc64-setup
EOF
popd


mkdir -p %{buildroot}%{_datadir}/grub/themes

install -d -m 0755 %{buildroot}%{_prefix}/lib/kernel/install.d/
install -m 0755 %{SOURCE10} %{buildroot}%{_prefix}/lib/kernel/install.d
install -m 0755 %{SOURCE7} %{buildroot}%{_prefix}/lib/kernel/install.d

install -d -m 0755 %{buildroot}%{_sysconfdir}/kernel/install.d/
install -m 0644 /dev/null %{buildroot}%{_sysconfdir}/kernel/install.d/20-grubby.install
install -m 0644 /dev/null %{buildroot}%{_sysconfdir}/kernel/install.d/90-loaderentry.install

install -d -m 0755 %{buildroot}%{_userunitdir}/timers.target.wants
install -m 0755 docs/grub-boot-success.timer %{buildroot}%{_userunitdir}
install -m 0755 docs/grub-boot-success.service %{buildroot}%{_userunitdir}
ln -s ../grub-boot-success.timer %{buildroot}%{_userunitdir}/timers.target.wants

install -d -m 0755 %{buildroot}%{_unitdir}/system-update.target.wants
install -m 0755 docs/grub-boot-indeterminate.service %{buildroot}%{_unitdir}
ln -s ../grub-boot-indeterminate.service %{buildroot}%{_unitdir}/system-update.target.wants

install -d -m 0755 %{buildroot}%{_libexecdir}/installkernel
cp -v %{SOURCE11} %{buildroot}%{_libexecdir}/installkernel
sed -e "s,@@LIBEXECDIR@@,%{_libexecdir}/installkernel,g" %{SOURCE12} > %{buildroot}%{_sbindir}/installkernel

%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post (                      \
    install -m 0755 -d %{finddebugroot}/usr             \
    mv %{buildroot}%{_bindir} %{finddebugroot}%{_bindir}        \
    mv %{buildroot}%{_sbindir} %{finddebugroot}%{_sbindir}      \
    %{dip}                              \
    install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/  \
    cp -al %{finddebugroot}/usr/lib/debug/              \\\
        %{buildroot}/usr/lib/debug/             \
    cp -al %{finddebugroot}/usr/src/debug/              \\\
        %{buildroot}/usr/src/debug/ )               \
    mv %{finddebugroot}%{_bindir} %{buildroot}%{_bindir}        \
    mv %{finddebugroot}%{_sbindir} %{buildroot}%{_sbindir}      \
    %{nil}

%undefine buildsubdir

%pre tools
if [ -f /boot/grub2/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' /boot/grub2/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' /boot/grub2/user.cfg
    fi
elif [ -f %{efi_esp_dir}/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' %{efi_esp_dir}/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' \
	    %{efi_esp_dir}/user.cfg
    fi
elif [ -f /etc/grub.d/01_users ] && \
	grep -q '^password_pbkdf2 root' /etc/grub.d/01_users ; then
    if [ -f %{efi_esp_dir}/grub.cfg ]; then
	# on EFI we don't get permissions on the file, but
	# the directory is protected.
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > %{efi_esp_dir}/user.cfg
    fi
    if [ -f /boot/grub2/grub.cfg ]; then
	install -m 0600 /dev/null /boot/grub2/user.cfg
	chmod 0600 /boot/grub2/user.cfg
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > /boot/grub2/user.cfg
    fi
fi

%posttrans tools

if [ -f /etc/default/grub ]; then
    if grep -q '^GRUB_ENABLE_BLSCFG=.*' /etc/default/grub; then
      sed -i '/GRUB_ENABLE_BLSCFG=/d' /etc/default/grub
    fi
fi

%triggerun -- grub2 < 1:1.99-4
mkdir -p /boot/grub2.tmp &&
mv -f /boot/grub2/*.mod \
      /boot/grub2/*.img \
      /boot/grub2/*.lst \
      /boot/grub2/device.map \
      /boot/grub2.tmp/ || :

%triggerpostun -- grub2 < 1:1.99-4
test ! -f /boot/grub2/device.map &&
test -d /boot/grub2.tmp &&
mv -f /boot/grub2.tmp/*.mod \
      /boot/grub2.tmp/*.img \
      /boot/grub2.tmp/*.lst \
      /boot/grub2.tmp/device.map \
      /boot/grub2/ &&
rm -r /boot/grub2.tmp/ || :

%files common -f grub.lang
%defattr(-,root,root)
%license COPYING
%dir /boot/grub2/themes/system
%attr(0755,root,root) %{_sbindir}/installkernel
%attr(0700,root,root) %dir /boot/grub2
%ghost %config(noreplace) /boot/grub2/grubenv
%exclude /boot/grub2/*
%dir %{_libdir}/grub/
%{_datarootdir}/grub/themes/
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%{_prefix}/lib/kernel/install.d/20-grub.install
%{_prefix}/lib/kernel/install.d/99-grub-mkconfig.install
%{_sysconfdir}/kernel/install.d/*.install
%{_libexecdir}/installkernel/installkernel-bls
%dir %attr(0700,root,root) %{efi_esp_dir}
%{_datadir}/locale/*

%files tools
%defattr(-,root,root)
%{_sbindir}/%{name}-mkconfig
%exclude %{_sbindir}/grub2-set-bootflag
%{_sbindir}/%{name}-switch-to-blscfg
%{_sbindir}/%{name}-rpm-sort
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-sparc64-setup
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-file
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-script-check

%config %{_sysconfdir}/grub.d/??_*
%exclude %{_sysconfdir}/grub.d/01_fallback_counting
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/grub.d/README
%{_sysconfdir}/prelink.conf.d/grub2.conf
%{_userunitdir}/*
%{_unitdir}/*
%{_datarootdir}/grub/*
%{_datarootdir}/bash-completion/completions/grub
%exclude %{_datarootdir}/grub/themes
%exclude %{_datarootdir}/grub/*.h
%{_infodir}/%{name}*

%if %{with_legacy_arch}
%{_sbindir}/grub2-install
%ifarch x86_64
%{_sbindir}/%{name}-bios-setup
%else
%exclude %{_sbindir}/%{name}-bios-setup
%endif
%ifarch %{sparc}
%{_sbindir}/grub2-sparc64-setup
%{_sbindir}/%{name}-ofpathname
%else
%exclude %{_sbindir}/grub2-sparc64-setup
%exclude %{_sbindir}/%{name}-ofpathname
%endif
%exclude %{_sbindir}/grub2-ofpathname
%endif

%files tools-minimal
%defattr(-,root,root)
%{_sysconfdir}/prelink.conf.d/grub2.conf
%attr(4755, root, root) %{_sbindir}/%{name}-set-bootflag
%{_sbindir}/%{name}-get-kernel-settings
%{_sbindir}/%{name}-set*password
%{_sbindir}/%{name}-set-default
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mount

%files tools-extra
%defattr(-,root,root)
%{_sysconfdir}/sysconfig/grub
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-syslinux2cfg
%ifnarch %{sparc}
%{_bindir}/grub2-mkrescue
%endif

%ifarch x86_64
%files tools-efi
%{_sbindir}/%{name}-macbless
%{_bindir}/%{name}-render-label
%endif


%if 0%{with_efi_arch}
%{expand:%define_efi_variant_files %%{package_arch} %%{grubefiname} %%{grubeficdname} %%{grubefiarch} %%{target_cpu_name} %%{grub_target_name}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%define_efi_variant_files %%{alt_package_arch} %%{grubaltefiname} %%{grubalteficdname} %%{grubaltefiarch} %%{alt_target_cpu_name} %%{alt_grub_target_name}}
%endif
%if 0%{with_legacy_arch}
%{expand:%define_legacy_variant_files %%{legacy_package_arch} %%{grublegacyarch}}
%endif

%if 0%{with_emu_arch}
%files emu
%{_bindir}/%{name}-emu*

%files emu-modules
%{_libdir}/grub/%{emuarch}-emu/*
%exclude %{_libdir}/grub/%{emuarch}-emu/*.module
%endif

%files           help
%defattr(-,root,root)
%doc INSTALL NEWS README THANKS TODO docs/grub.html docs/grub-dev.html docs/font_char_metrics.png
%{_datadir}/man/man*

%changelog
* Tue Nov 16 2021 fengtao <fengtao40@huawei.com> - 2.04-21
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix bad test on GRUB_DISABLE_SUBMENU

* Mon Sep 27 2021 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-20
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:verifiers: Fix calling uninitialized function pointer

* Mon Aug 02 2021 gaihuiying <gaihuiying1@huawei.com> - 2.04-19
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify git config parameters

* Tue May 25 2021 yanan <yanan@huawei.com> - 2.04-18
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:delete the Symbolic Link of grubenv in grub2-efi-x64 and grub-efi-aa64 packages

* Tue May 18 2021 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-17
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:delete the Symbolic Link of grubenv in grub2-efi-x64 and grub-efi-aa64 packages

* Tue Mar 30 2021 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-16
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:backport some patches from upstream community and fix incorrect
       author names in patches

* Mon Mar 29 2021 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-15
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:backport the patches that upstream community released on
       March 2, 2021

* Mon Mar 29 2021 renmingshuai <renmingshuai@huawei.com> - 2.04-14
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add efi_vendor for vendor

* Sun Mar 21 2021 orange-snn <songnannan2@huawei.com> - 2.04-13
- fix postun error in grub2-efi-x64

* Thu Mar 18 2021 yanglu <yanglu60@huawei.com> - 2.04-12
- Type:cves
- ID:CVE-2020-27779 CVE-2020-14372
- SUG:NA
- DESC:fix CVE-2020-27779 CVE-2020-14372

* Wed Mar 17 2021 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-11
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix the installation failure of grub2-efi-x64/grub-efi-aa64 packages on
       the /boot partition of VFAT file system.

* Fri Mar 12 2021 yanglu <yanglu60@huawei.com> - 2.04-10
- Type:cves
- ID:CVE-2020-25632 CVE-2020-25647 CVE-2020-27749 CVE-2021-20225 CVE-2021-20233
- SUG:NA
- DESC:fix CVE-2020-25632 CVE-2020-25647 CVE-2020-27749 CVE-2021-20225 CVE-2021-20233

* Sat Feb 27 2021 fengtao <fengtao40@huawei.com> - 2.04-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:tftp roll over block counter to prevent timeouts with
       data packets
       
* Mon Feb 22 2021 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix kernel not found because grub.cfg using BLS format

* Mon Nov 16 2020 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove duplicate rpm-devel in BuildRequires

* Sat Nov 14 2020 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove 08_fallback_counting.in apply grubby

* Thu Oct 29 2020 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove grub2-emu and grub2-emu-lite in grub2-tools

* Thu Oct 29 2020 zhangqiumiao <zhangqiumiao1@huawei.com> - 2.04-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:split tools-extra and tools-minimal from tools

* Fri Aug 7 2020 hanzhijun <hanzhijun1@huawei.com> - 2.04-3
- Type:cves
- Id:CVE-2020-10713 CVE-2020-14308 CVE-2020-14309 CVE-2020-14310 CVE-2020-14311 CVE-2020-15705 CVE-2020-15706 CVE-2020-15707
- SUG:NA
- DESC:fix CVE-2020-10713 CVE-2020-14308 CVE-2020-14309 CVE-2020-14310 CVE-2020-14311 CVE-2020-15705 CVE-2020-15706 CVE-2020-15707

* Mon Aug 3 2020 hanzhijun <hanzhijun1@huawei.com> - 2.04-2
- add CPPFLAGS

* Sat Aug 1 2020 hanzhijun <hanzhijun1@huawei.com> - 2.04-1
- update to 2.0.4 
 
* Fri Jul 17 2020 chenyaqiang <chenyaqiang@huawei.com> - 2.02-75
- remove repeated buildrequest packge “rpm-devel” in grub2.spec

* Fri Apr 24 2020 fengtao <fengtao40@huawei.com> - 2.02-74
- exclude two cmd in grub2-tools

* Wed Mar 3 2020 songnannan <songnannan2@huawei.com> - 2.02-73
- delete java-1.8.0-openjdk in buildrequires

* Thu Feb 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.02-72
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add make check function

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-71
- Type:cves
- Id:NA
- SUG:NA
- DESC:add cve patches

* Tue Dec 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-70
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the path for themes

* Tue Dec 3 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-69- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add config_for_secure file for gcc_secure

* Sat Sep 28 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-68
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:rename the 20-grub.install file to 20-grubby.install

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-67
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix grub2-setpassword error for openeuler

* Wed Sep 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-66
- Package init
