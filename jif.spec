Summary:	Jif: Java + information flow
Summary(pl.UTF-8):   Jif (Java + information flow) - Java z przepĹywem informacji
Name:		jif
Version:	3.0.0
Release:	0.1
License:	Apache v1.1
Group:		Development/Languages/Java
Source0:	http://www.cs.cornell.edu/jif/releases/%{name}-%{version}.zip
# Source0-md5:	e657b80f3e19d6d0909a16af3a8b6b88
Patch0:		%{name}-classpath.patch
URL:		http://www.cs.cornell.edu/jif/
BuildRequires:	ant >= 1.6.5-4
BuildRequires:	gcc-c++
BuildRequires:	jdk >= 1.3
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jre >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jif is a security-typed programming language that extends Java with
support for static information flow control.

Static information flow control can protect the confidentiality and
integrity of information manipulated by computing systems. The
compiler tracks the correspondence between information the policies
that restrict its use, enforcing security properties end-to-end within
the system. After checking information flow within Jif programs, the
Jif compiler translates them to Java programs and uses an ordinary
Java compiler to produce secure executable programs.

%description -l pl.UTF-8
Jif to jÄzyk programowania z bezpiecznymi typami rozszerzajÄcy JavÄ
o obsĹugÄ statycznej kontroli przepĹywu informacji.

Statyczna kontrola przepĹywu informacji moĹźe chroniÄ poufnoĹÄ i
spĂłjnoĹÄ informacji przetwarzanych przez systemy obliczeniowe.
Kompilator Ĺledzi zgodnoĹÄ miÄdzy informacjami a politykÄ
ograniczajÄcÄ ich uĹźycie, wymuszajÄc w systemie poĹźÄdane wĹaĹciwoĹci
bezpieczeĹstwa. Po sprawdzeniu przepĹywu informacji w programach w
Jifie kompilator tĹumaczy je na programy w Javie i uĹźywa zwykĹego
kompilatora Javy do stworzenia bezpiecznych programĂłw wykonywalnych.

%prep
%setup -q

%build
required_jars='ant'
CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
export CLASSPATH="$CLASSPATH:`/usr/bin/build-classpath $required_jars`"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

%{ant} 
%{ant} javadoc

# Java software sucks
patch -p1 <%{PATCH0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},{%{_javadir},%{_libdir}}/%{name}}

sed -e "s|TOP=.*|TOP='%{_javadir}'|" \
    -e "s|RT_LIB_PATH='.*:'|RT_LIB_PATH='%{_libdir}/%{name}:'|" bin/jif \
	> $RPM_BUILD_ROOT%{_bindir}/jif
sed -e "s|TOP=.*|TOP='%{_javadir}'|" \
    -e "s|RT_LIB_PATH='.*:'|RT_LIB_PATH='%{_libdir}/%{name}:'|" bin/jifc \
	> $RPM_BUILD_ROOT%{_bindir}/jifc
sed -e "s|TOP=.*|TOP='%{_javadir}'|" \
    -e "s|RT_LIB_PATH='.*:'|RT_LIB_PATH='%{_libdir}/%{name}:'|" bin/splitc \
	> $RPM_BUILD_ROOT%{_bindir}/splitc

install lib/{JFlex,java_cup,jif,jiflib,jifrt,jifsig,polyglot}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/

install lib/libjifrt.so $RPM_BUILD_ROOT%{_libdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%{_javadir}/%{name}
