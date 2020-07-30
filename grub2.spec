%undefine _hardened_build

%global tarversion 2.02
%undefine _missing_build_ids_terminate_build
%global _configure_gnuconfig_hack 0

Name:		grub2
Epoch:		1
Version:	2.02
Release:	76
Summary:	Bootloader with support for Linux, Multiboot and more
License:	GPLv3+
URL:		http://www.gnu.org/software/grub/
Source0:	https://ftp.gnu.org/gnu/grub//grub-%{tarversion}.tar.xz
Source1:        grub.macros
Source2:	grub.patches
Source3:	release-to-master.patch
Source4:	http://unifoundry.com/unifont-5.1.20080820.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore
Source8:	strtoull_test.c
Source9:	20-grub.install
Source11:	installkernel-bls
Source12:	installkernel.in

%include %{SOURCE1}
%include %{SOURCE2}

BuildRequires:	gcc efi-srpm-macros flex bison binutils python3 ncurses-devel xz-devel
BuildRequires:	freetype-devel libusb-devel bzip2-devel rpm-devel rpm-devel rpm-libs
BuildRequires:	autoconf automake autogen device-mapper-devel freetype-devel git
BuildRequires:	texinfo gettext-devel dejavu-sans-fonts help2man systemd 

%ifarch %{golang_arches}
BuildRequires:	pesign >= 0.99-8
%endif
%if %{?_with_ccache: 1}%{?!_with_ccache: 0}
BuildRequires:	ccache
%endif

Obsoletes:	grub2 <= %{evr} grub < 1:0.98

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

%package        common
Summary:	common package for grub2
BuildArch:	noarch
Conflicts:	grubby < 8.40-18

%description common
Common package for grub2.

%package        tools
Summary:	tools package for grub2
Requires:	grub2-common = %{epoch}:%{version}-%{release}
Requires:	gettext os-prober which file
Requires(pre):	dracut
Requires(post):	dracut
Provides:       grub2-tools-minimal grub2-tools-extra
Obsoletes:      grub2-tools-minimal grub2-tools-extra

%description    tools
tools package for grub2.

%ifarch x86_64
%package        tools-efi
Summary:        efi packages for grub2-tools
Requires:	grub2-common = %{epoch}:%{version}-%{release}
Requires:	gettext os-prober which file
Obsoletes:	grub2-tools < %{evr}

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

rm -rf %{buildroot}%{_infodir}/dir
ln -s grub2-set-password %{buildroot}%{_sbindir}/grub2-setpassword
echo '.so man8/grub2-set-password.8' > %{buildroot}%{_datadir}/man/man8/%{name}-setpassword.8

%ifnarch x86_64
rm -vf %{buildroot}%{_bindir}/grub2-render-label
rm -vf %{buildroot}%{_sbindir}/grub2-bios-setup
rm -vf %{buildroot}%{_sbindir}/grub2-macbless
%endif

install -d %{buildroot}%{_sysconfdir}/prelink.conf.d/

pushd %{buildroot}%{_sysconfdir}/prelink.conf.d/
cat << EOF > grub2.conf
# these have execstack, and break under selinux
-b /usr/bin/grub2-script-check
-b /usr/bin/grub2-mkrelpath
-b /usr/bin/grub2-fstest
-b /usr/sbin/grub2-bios-setup
-b /usr/sbin/grub2-probe
-b /usr/sbin/grub2-sparc64-setup
EOF
popd


mkdir -p %{buildroot}%{_datadir}/grub/themes

install -d -m 0755 %{buildroot}%{_prefix}/lib/kernel/install.d
install -m 0755 %{SOURCE9} %{buildroot}%{_prefix}/lib/kernel/install.d

install -d -m 0755 %{buildroot}%{_sysconfdir}/kernel/install.d
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
sed -e "s,@@LIBEXECDIR@@,%{_libexecdir}/installkernel,g" %{SOURCE12} \
	> %{buildroot}%{_sbindir}/installkernel


%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post (						\
	install -m 0755 -d %{finddebugroot}/usr				\
	mv %{buildroot}%{_bindir} %{finddebugroot}%{_bindir}		\
	mv %{buildroot}%{_sbindir} %{finddebugroot}%{_sbindir}		\
	%{dip}								\
	install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/	\
	cp -al %{finddebugroot}/usr/lib/debug/				\\\
		%{buildroot}/usr/lib/debug/				\
	cp -al %{finddebugroot}/usr/src/debug/				\\\
		%{buildroot}/usr/src/debug/ )				\
	mv %{finddebugroot}%{_bindir} %{buildroot}%{_bindir}		\
	mv %{finddebugroot}%{_sbindir} %{buildroot}%{_sbindir}		\
	%{nil}

%undefine buildsubdir

%pre            tools
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

%post           tools
if [ "$1" = 1 ]; then
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || :
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info.gz || :
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

%preun tools
if [ "$1" = 0 ]; then
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || :
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info.gz || :
fi

%files          common
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
%{_sysconfdir}/kernel/install.d/*.install
%{_libexecdir}/installkernel/installkernel-bls
%dir %attr(0700,root,root) %{efi_esp_dir}
%{_datadir}/locale/*

%files          tools
%defattr(-,root,root)
%{_sbindir}/grub2-*
%exclude %{_sbindir}/grub2-set-bootflag
%attr(4755, root, root) %{_sbindir}/grub2-set-bootflag
%{_bindir}/grub2-*
%config %{_sysconfdir}/grub.d/??_*
%exclude %{_sysconfdir}/grub.d/01_fallback_counting
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/grub.d/README
%{_sysconfdir}/sysconfig/grub
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
%ifarch %{sparc}
%{_sbindir}/grub2-sparc64-setup
%else
%exclude %{_sbindir}/grub2-sparc64-setup
%endif
%exclude %{_sbindir}/grub2-ofpathname
%endif

%ifnarch %{sparc}
%{_bindir}/grub2-mkrescue
%endif

%ifarch x86_64
%files           tools-efi
%defattr(-,root,root)
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

%files           help
%defattr(-,root,root)
%doc INSTALL NEWS README THANKS TODO docs/grub.html docs/grub-dev.html docs/font_char_metrics.png
%{_datadir}/man/man*

%changelog
* Fri Jul 31 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.02-76
- Type:cves
- Id:CVE-2020-10713
- SUG:NA
- DESC:fix CVE-2020-10713

* Fri Jun 5 2020 fengtao <fengtao40@huawei.com> - 2.02-75
- remove sign for grub efi

* Mon May 25 2020 songnannan <songnannan2@huawei.com> - 2.02-74
- rebuild for the update packages

* Wed May 3 2020 songnannan <songnannan2@huawei.com> - 2.02-73
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

* Tue Dec 3 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.02-69
- Type:bugfix
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
