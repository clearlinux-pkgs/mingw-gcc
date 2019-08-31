%define keepstatic 1
%define gcc_target x86_64-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.26
%define isl_version 0.16.1
%define gccver 9
%define gccpath gcc-9.1.0
# Highest optimisation ABI we target
%define mtune haswell

# Lowest compatible ABI (must be lowest of current targets & OBS builders)
# avoton (silvermont target) && ivybridge (OBS builders) = westmere
%define march westmere
%define abi_package %{nil}

Name     : mingw-gcc
Version  : 9.2.1
Release  : 638
URL      : http://www.gnu.org/software/gcc/
Source0  : https://gcc.gnu.org/pub/gcc/releases/gcc-9.1.0/gcc-9.1.0.tar.xz
Source1  : https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.16.1.tar.bz2
Source2  : DATESTAMP
Source3  : REVISION
Summary  : GNU cc and gcc C compilers
Group    : Development/Tools
License  : BSD-3-Clause BSL-1.0 GFDL-1.2 GFDL-1.3 GPL-2.0 GPL-3.0 LGPL-2.1 LGPL-3.0 MIT


Patch0   : gcc-stable-branch.patch
Patch1   : 0001-Fix-stack-protection-issues.patch
Patch2   : openmp-vectorize-v2.patch
Patch3   : fortran-vector-v2.patch
Patch5   : optimize.patch
Patch6   : ipa-cp.patch
Patch8	 : optimize-at-least-some.patch
Patch9   : gomp-relax.patch
Patch11  : memcpy-avx2.patch
Patch12	 : avx512-when-we-ask-for-it.patch
Patch14  : arch-native-override.patch
Patch15  : 0001-Ignore-Werror-if-GCC_IGNORE_WERROR-environment-varia.patch
Patch16  : 0001-Always-use-z-now-when-linking-with-pie.patch

# zero registers on ret to make ROP harder
Patch21  : zero-regs-gcc8.patch

Patch99  : fixup-9-branch.patch

# cves: 1xx


BuildRequires : bison
BuildRequires : flex
BuildRequires : gmp-dev
BuildRequires : libstdc++
BuildRequires : libunwind-dev
BuildRequires : mpc-dev
BuildRequires : mpfr-dev
BuildRequires : pkgconfig(zlib)
BuildRequires : sed
BuildRequires : texinfo
BuildRequires : dejagnu
BuildRequires : expect
BuildRequires : autogen
BuildRequires : guile
BuildRequires : tcl
BuildRequires : valgrind-dev
BuildRequires : libxml2-dev
BuildRequires : libxslt
BuildRequires : graphviz
BuildRequires : gdb-dev
BuildRequires : procps-ng
BuildRequires : glibc-libc32
BuildRequires : glibc-dev32
BuildRequires : docbook-xml docbook-utils doxygen
BuildRequires : mingw-binutils 
# mingw-crt mingw-crt-dev


Requires: gcc-libubsan
Requires: gcc-doc

Provides:       gcc-symlinks
Provides:       cpp
Provides:       cpp-symlinks
Provides:       gcov
Provides:       gfortran-symlinks
Provides:       g77
Provides:       g77-symlinks
Provides:       g++-symlinks
Provides:       g++
Provides:       gfortran

%description
GNU cc and gcc C compilers.

%package dev
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libgcov-dev
Provides:       libssp-dev
Provides:       libssp-staticdev
Provides:       libgomp-dev
Provides:       libgomp-staticdev
Provides:       libgcc-s-dev
Provides:       gcc-plugin-dev
Provides:       libstdc++-dev
Requires:       gcc-libs-math
Requires:       libstdc++

%description dev
GNU cc and gcc C compilers dev files



%package dev32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description dev32
GNU cc and gcc C compilers dev files




%package -n libgcc1
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Requires:       filesystem
Provides:       libssp0
Provides:       libgomp1

%description -n libgcc1
GNU cc and gcc C compilers.

%package libgcc32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libgcc32
GNU cc and gcc C compilers.

%package libubsan
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libubsan
Address sanitizer runtime libs

%package -n libstdc++
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description -n libstdc++
GNU cc and gcc C compilers.

%package libstdc++32
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libstdc++32
GNU cc and gcc C compilers.

%package doc
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          doc

%package go
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU Compile Collection GO compiler
Group:          devel

%description go
GNU Compile Collection GO compiler

%package go-lib
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU Compile Collection GO runtime
Group:          devel

%description go-lib
GNU Compile Collection GO runtime

%description doc
GNU cc and gcc C compilers.

%package locale
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          libs

%description locale
GNU cc and gcc C compilers.

%package libs-math
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          libs

%description libs-math
GNU cc and gcc C compilers.


%prep
%setup -q -n %{gccpath}
%patch99 -p1
%patch0 -p1

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
#%patch11 -p1

%patch12 -p1

%patch14 -p1

%patch15 -p1
%patch16 -p1

#%patch18 -p1
#%patch20 -p1

%patch21 -p1


%build

# Live in the gcc source tree
tar xf %{SOURCE1} && ln -sf isl-%{isl_version} isl

# Update the DATESTAMP and add a revision
tee `find -name DATESTAMP` > /dev/null < %{SOURCE2}
cp %{SOURCE3} gcc/

rm -rf ../gcc-build
mkdir ../gcc-build
pushd ../gcc-build
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=westmere -g1 -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000 -mtune=skylake"
export CXXFLAGS="-march=westmere -g1 -O3  -Wl,-z,max-page-size=0x1000 -mtune=skylake"
export CFLAGS_FOR_TARGET="$CFLAGS"
export CXXFLAGS_FOR_TARGET="$CXXFLAGS"
export FFLAGS_FOR_TARGET="$FFLAGS"

export CPATH=/usr/include
export LIBRARY_PATH=/usr/lib64

../%{gccpath}/configure \
    --prefix=/usr \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/lib64 \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/lib64 \
    --with-system-zlib\
    --enable-shared\
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --disable-plugin\
    --with-gnu-as \
    --with-gnu-ld \
    --disable-nls  \
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --disable-multilib\
    --disable-lto\
    --disable-win32-registry \
    --disable-werror \
    --enable-linker-build-id \
    --enable-languages="c" \
    --build=%{gcc_target}\
    --target=x86_64-w64-mingw32 \
    --disable-bootstrap \
    --with-ppl=yes \
    --with-isl \
    --disable-libssp \
    --includedir=/usr/include/mingw \
    --exec-prefix=/usr \
    --disable-libunwind-exceptions \
    --with-gnu-ld \
    --with-tune=haswell \
    --with-arch=westmere \
    --disable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only 

make -j20 all-gcc

#    --enable-languages="c,c++,fortran" \

popd


%install
export CPATH=/usr/include
export LIBRARY_PATH=/usr/lib64
pushd ../gcc-build


make DESTDIR=%{buildroot} install-gcc 
ln -s /usr/bin/x86_64-w64-mingw32-as %{buildroot}/usr/lib64/gcc/x86_64-w64-mingw32/9/as
ln -s /usr/bin/x86_64-w64-mingw32-ld %{buildroot}/usr/lib64/gcc/x86_64-w64-mingw32/9/ld
ln -s /usr/bin/x86_64-w64-mingw32-ar %{buildroot}/usr/lib64/gcc/x86_64-w64-mingw32/9/ar
ln -s /usr/bin/x86_64-w64-mingw32-ranlib %{buildroot}/usr/lib64/gcc/x86_64-w64-mingw32/9/ranlib

%files
   /usr/bin/x86_64-w64-mingw32-cpp
   /usr/bin/x86_64-w64-mingw32-gcc
   /usr/bin/x86_64-w64-mingw32-gcc-9
   /usr/bin/x86_64-w64-mingw32-gcc-ar
   /usr/bin/x86_64-w64-mingw32-gcc-nm
   /usr/bin/x86_64-w64-mingw32-gcc-ranlib
   /usr/bin/x86_64-w64-mingw32-gcov
   /usr/bin/x86_64-w64-mingw32-gcov-dump
   /usr/bin/x86_64-w64-mingw32-gcov-tool
   /usr/lib64/gcc/x86_64-w64-mingw32/9/cc1
   /usr/lib64/gcc/x86_64-w64-mingw32/9/as
   /usr/lib64/gcc/x86_64-w64-mingw32/9/ld
   /usr/lib64/gcc/x86_64-w64-mingw32/9/ar
   /usr/lib64/gcc/x86_64-w64-mingw32/9/ranlibg
   /usr/lib64/gcc/x86_64-w64-mingw32/9/collect2
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include-fixed/README
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include-fixed/limits.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include-fixed/syslimits.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/adxintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/ammintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx2intrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx5124fmapsintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx5124vnniwintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512bitalgintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512bwintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512cdintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512dqintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512erintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512fintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512ifmaintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512ifmavlintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512pfintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vbmi2intrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vbmi2vlintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vbmiintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vbmivlintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vlbwintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vldqintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vlintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vnniintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vnnivlintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vpopcntdqintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avx512vpopcntdqvlintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/avxintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/bmi2intrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/bmiintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/bmmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/cet.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/cetintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/cldemoteintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/clflushoptintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/clwbintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/clzerointrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/cpuid.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/cross-stdarg.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/emmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/f16cintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/float.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/fma4intrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/fmaintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/fxsrintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/gfniintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/ia32intrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/immintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/iso646.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/lwpintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/lzcntintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/mm3dnow.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/mm_malloc.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/mmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/movdirintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/mwaitxintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/nmmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/pconfigintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/pkuintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/pmmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/popcntintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/prfchwintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/rdseedintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/rtmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/sgxintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/shaintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/smmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdalign.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdarg.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdatomic.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdbool.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stddef.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdfix.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdint-gcc.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdint.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/stdnoreturn.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/tbmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/tgmath.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/tmmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/vaesintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/varargs.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/vpclmulqdqintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/waitpkgintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/wbnoinvdintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/wmmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/x86intrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xmmintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xopintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xsavecintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xsaveintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xsaveoptintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xsavesintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/include/xtestintrin.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/fixinc.sh
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/fixinc_list
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/fixincl
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/gsyslimits.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/include/README
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/include/limits.h
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/macro_list
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/mkheaders
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/mkheaders.conf
   /usr/lib64/gcc/x86_64-w64-mingw32/9/install-tools/mkinstalldirs
   /usr/lib64/gcc/x86_64-w64-mingw32/9/lto-wrapper
%exclude    /usr/share/info/cpp.info
%exclude    /usr/share/info/cppinternals.info
%exclude    /usr/share/info/gcc.info
%exclude    /usr/share/info/gccinstall.info
%exclude    /usr/share/info/gccint.info
   /usr/share/man/man1/x86_64-w64-mingw32-cpp.1
   /usr/share/man/man1/x86_64-w64-mingw32-gcc.1
   /usr/share/man/man1/x86_64-w64-mingw32-gcov-dump.1
   /usr/share/man/man1/x86_64-w64-mingw32-gcov-tool.1
   /usr/share/man/man1/x86_64-w64-mingw32-gcov.1
%exclude    /usr/share/man/man7/fsf-funding.7
%exclude   /usr/share/man/man7/gfdl.7
%exclude   /usr/share/man/man7/gpl.7
