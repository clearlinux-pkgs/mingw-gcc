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
# Suppress stripping binaries
%define __strip /bin/true
%define debug_package %{nil}

Name     : mingw-gcc
Version  : 9.2.1
Release  : 642
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
BuildRequires : mingw-crt mingw-crt-dev
BuildRequires : strace


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
export CFLAGS="-march=westmere -g1 -O3 -fno-stack-protector -mtune=skylake"
export CXXFLAGS="-march=westmere -g1 -O3   -mtune=skylake"
export CFLAGS_FOR_TARGET="$CFLAGS -I /usr/mingw/include -isystem /usr/mingw/include -isysroot=/usr/mingw/ "
export CXXFLAGS_FOR_TARGET="$CXXFLAGS -isystem /usr/mingw/include"
export FFLAGS_FOR_TARGET="$FFLAGS  -isystem /usr/mingw/include"
export LDFLAGS_FOR_TARGET="$LFDLAGS -L/usr/mingw/lib "
export AS="/usr/bin/x86_64-w64-mingw32-as"
export AR="/usr/bin/x86_64-w64-mingw32-ar"
export RANLIB="/usr/bin/x86_64-w64-mingw32-ranlib"
export DLLTOOL="/usr/bin/x86_64-w64-mingw32-dlltool" 
export LIBRARY_PATH=/usr/lib64:/usr/mingw/lib:/usr/lib64

../%{gccpath}/configure \
    --prefix=/usr \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/mingw/lib \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/mingw/lib \
    --with-system-zlib\
    --enable-shared\
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=win32 \
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
    --enable-languages="c,c++,fortran" \
    --build=%{gcc_target}\
    --target=x86_64-w64-mingw32 \
    --disable-bootstrap \
    --with-ppl=yes \
    --with-isl \
    --disable-libssp \
    --includedir=/usr/mingw/include \
    --exec-prefix=/usr \
    --disable-libunwind-exceptions \
    --with-gnu-ld \
    --with-tune=haswell \
    --with-arch=westmere \
    --disable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only 

make -j20 all

#    --enable-languages="c,c++,fortran" \

popd



%install
export LIBRARY_PATH=/usr/lib64
mkdir -p  %{buildroot}/usr/mingw
ln -s mingw %{buildroot}/usr/x86_64-w64-mingw32

pushd ../gcc-build
make DESTDIR=%{buildroot} install 
popd
ln -s /usr/bin/x86_64-w64-mingw32-as %{buildroot}/usr/mingw/lib/gcc/x86_64-w64-mingw32/9/as
ln -s /usr/bin/x86_64-w64-mingw32-ld %{buildroot}/usr/mingw/lib/gcc/x86_64-w64-mingw32/9/ld
ln -s /usr/bin/x86_64-w64-mingw32-ar %{buildroot}/usr/mingw/lib/gcc/x86_64-w64-mingw32/9/ar
ln -s /usr/bin/x86_64-w64-mingw32-ranlib %{buildroot}/usr/mingw/lib/gcc/x86_64-w64-mingw32/9/ranlib

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
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/cc1
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/as
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/ld
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/ar
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/ranlib
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/collect2
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include-fixed/README
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include-fixed/limits.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include-fixed/syslimits.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/adxintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/ammintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx2intrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx5124fmapsintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx5124vnniwintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512bitalgintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512bwintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512cdintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512dqintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512erintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512fintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512ifmaintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512ifmavlintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512pfintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vbmi2intrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vbmi2vlintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vbmiintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vbmivlintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vlbwintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vldqintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vlintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vnniintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vnnivlintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vpopcntdqintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avx512vpopcntdqvlintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/avxintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/bmi2intrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/bmiintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/bmmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/cet.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/cetintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/cldemoteintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/clflushoptintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/clwbintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/clzerointrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/cpuid.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/cross-stdarg.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/emmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/f16cintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/float.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/fma4intrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/fmaintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/fxsrintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/gfniintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/ia32intrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/immintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/iso646.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/lwpintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/lzcntintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/mm3dnow.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/mm_malloc.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/mmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/movdirintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/mwaitxintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/nmmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/pconfigintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/pkuintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/pmmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/popcntintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/prfchwintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/rdseedintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/rtmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/sgxintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/shaintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/smmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdalign.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdarg.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdatomic.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdbool.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stddef.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdfix.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdint-gcc.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdint.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/stdnoreturn.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/tbmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/tgmath.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/tmmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/vaesintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/varargs.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/vpclmulqdqintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/waitpkgintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/wbnoinvdintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/wmmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/x86intrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xmmintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xopintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xsavecintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xsaveintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xsaveoptintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xsavesintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/xtestintrin.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/fixinc.sh
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/fixinc_list
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/fixincl
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/gsyslimits.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/include/README
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/include/limits.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/macro_list
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/mkheaders
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/mkheaders.conf
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/install-tools/mkinstalldirs
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/lto-wrapper
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
 /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/crtbegin.o
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/crtend.o
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/crtfastmath.o
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/gcov.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/quadmath.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/quadmath_weak.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/unwind.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libgcc.a
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libgcc_eh.a
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libgcov.a
   /usr/share/info/libquadmath.info
   /usr/mingw/lib/libatomic-1.dll
   /usr/mingw/lib/libatomic.a
   /usr/mingw/lib/libatomic.dll.a
%exclude    /usr/mingw/lib/libatomic.la
   /usr/mingw/lib/libgcc_s.a
   /usr/mingw/lib/libgcc_s_seh-1.dll
   /usr/mingw/lib/libquadmath-0.dll
   /usr/mingw/lib/libquadmath.a
   /usr/mingw/lib/libquadmath.dll.a
%exclude    /usr/mingw/lib/libquadmath.la
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/crtbegin.o
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/crtend.o
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/crtfastmath.o
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/gcov.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/quadmath.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/quadmath_weak.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/unwind.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libgcc.a
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libgcc_eh.a
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libgcov.a
   /usr/share/info/libquadmath.info
   /usr/mingw/lib/libatomic-1.dll
   /usr/mingw/lib/libatomic.a
   /usr/mingw/lib/libatomic.dll.a
%exclude    /usr/mingw/lib/libatomic.la
   /usr/mingw/lib/libgcc_s.a
   /usr/mingw/lib/libgcc_s_seh-1.dll
   /usr/mingw/lib/libquadmath-0.dll
   /usr/mingw/lib/libquadmath.a
   /usr/mingw/lib/libquadmath.dll.a
%exclude    /usr/mingw/lib/libquadmath.la
%exclude /usr/x86_64-w64-mingw32
   /usr/mingw/include/c++/9
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/cc1plus
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/f951
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/finclude/ieee_arithmetic.mod
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/finclude/ieee_exceptions.mod
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/finclude/ieee_features.mod
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/include/ISO_Fortran_binding.h
   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libcaf_single.a
%exclude   /usr/mingw/lib/gcc/x86_64-w64-mingw32/9/libcaf_single.la
   /usr/mingw/lib/libgfortran-5.dll
   /usr/mingw/lib/libgfortran.a
   /usr/mingw/lib/libgfortran.dll.a
%exclude   /usr/mingw/lib/libgfortran.la
   /usr/mingw/lib/libgfortran.spec
   /usr/mingw/lib/libstdc++-6.dll
   /usr/mingw/lib/libstdc++.a
   /usr/mingw/lib/libstdc++.dll.a
   /usr/mingw/lib/libstdc++.dll.a-gdb.py
%exclude   /usr/mingw/lib/libstdc++.la
   /usr/mingw/lib/libsupc++.a
%exclude   /usr/mingw/lib/libsupc++.la
   /usr/share/gcc-9/python/libstdcxx/__init__.py
   /usr/share/gcc-9/python/libstdcxx/v6/__init__.py
   /usr/share/gcc-9/python/libstdcxx/v6/printers.py
   /usr/share/gcc-9/python/libstdcxx/v6/xmethods.py
%exclude   /usr/share/info/gfortran.info
   /usr/share/man/man1/x86_64-w64-mingw32-g++.1
   /usr/share/man/man1/x86_64-w64-mingw32-gfortran.1
