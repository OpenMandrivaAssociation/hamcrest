# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Name:			hamcrest
Version:		1.1
Release:		2.0.7
Epoch:			0
Summary:		Hamcrest matcher object framework
License:		BSD
Url:			http://code.google.com/p/hamcrest/
Group:			Development/Java
Source0:		http://hamcrest.googlecode.com/files/hamcrest-1.1.tgz
Source1:		http://repo1.maven.org/maven2/org/hamcrest/hamcrest-parent/1.1/hamcrest-parent-1.1.pom
Source2:		http://repo1.maven.org/maven2/org/hamcrest/hamcrest-library/1.1/hamcrest-library-1.1.pom
Source3:		http://repo1.maven.org/maven2/org/hamcrest/hamcrest-integration/1.1/hamcrest-integration-1.1.pom
Source4:		http://repo1.maven.org/maven2/org/hamcrest/hamcrest-generator/1.1/hamcrest-generator-1.1.pom
Source5:		http://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.1/hamcrest-core-1.1.pom
Source6:		http://repo1.maven.org/maven2/org/hamcrest/hamcrest-all/1.1/hamcrest-all-1.1.pom
Source7:		hamcrest-text-1.1.pom
Patch0:			hamcrest-1.1-build.patch
BuildRequires:	jpackage-utils >= 0:1.7.4
BuildRequires:	java-rpmbuild
BuildRequires:	ant >= 0:1.6.5
BuildRequires:	ant-junit
BuildRequires:	easymock2
BuildRequires:	jarjar
BuildRequires:	jmock
BuildRequires:	junit
BuildRequires:	junit4
BuildRequires:	qdox
BuildRequires:	testng
Requires:	java >= 0:1.5.0
Requires:	easymock2
Requires:	jmock
Requires:	qdox
%if ! %{gcj_support}
Buildarch:		noarch
%endif

%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif

Requires(post):		jpackage-utils >= 0:1.7.4
Requires(postun):	jpackage-utils >= 0:1.7.4

%description
Provides a library of matcher objects (also known as 
constraints or predicates) allowing 'match' rules to 
be defined declaratively, to be used in other frameworks. 
Typical scenarios include testing frameworks, mocking 
libraries and UI validation rules.

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:		Development/Java
Summary:	Demos for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	junit
Requires:	junit4
Requires:	testng

%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q 
%remove_java_binaries
# BUILD/hamcrest-1.1/lib/generator/jarjar-1.0rc3.jar.no
ln -sf $(build-classpath jarjar) lib/generator/
# BUILD/hamcrest-1.1/lib/generator/qdox-1.6.1.jar.no
ln -sf $(build-classpath qdox) lib/generator/
# BUILD/hamcrest-1.1/lib/integration/easymock-2.2.jar.no
ln -sf $(build-classpath easymock2) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/jmock-1.10RC1.jar.no
ln -sf $(build-classpath jmock) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/junit-3.8.1.jar.no
ln -sf $(build-classpath junit) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/junit-4.0.jar.no
ln -sf $(build-classpath junit4) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/testng-4.6-jdk15.jar.no
ln -sf $(build-classpath testng) lib/integration/
%patch0 -b .sav0

%build
export OPT_JAR_LIST=$(build-classpath ant-launcher ant/ant-junit junit)
export CLASSPATH=$(build-classpath asm3 ant-launcher ant ant/ant-junit)
%{ant} -Dversion=1.1 -Dbuild.sysclasspath=first all javadoc

%install

# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-parent.pom
%add_to_maven_depmap org.hamcrest %{name}-parent %{version} JPP/%{name} parent

install -m 644 build/%{name}-all-%{version}.jar %{buildroot}%{_javadir}/%{name}/all-%{version}.jar
install -m 644 %{SOURCE6} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-all.pom
%add_to_maven_depmap org.hamcrest %{name}-all %{version} JPP/%{name} all

install -m 644 build/%{name}-core-%{version}.jar %{buildroot}%{_javadir}/%{name}/core-%{version}.jar
install -m 644 %{SOURCE5} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-core.pom
%add_to_maven_depmap org.hamcrest %{name}-core %{version} JPP/%{name} core

install -m 644 build/%{name}-generator-%{version}.jar %{buildroot}%{_javadir}/%{name}/generator-%{version}.jar
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-generator.pom
%add_to_maven_depmap org.hamcrest %{name}-generator %{version} JPP/%{name} generator

install -m 644 build/%{name}-library-%{version}.jar %{buildroot}%{_javadir}/%{name}/library-%{version}.jar
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-library.pom
%add_to_maven_depmap org.hamcrest %{name}-library %{version} JPP/%{name} library

install -m 644 build/%{name}-integration-%{version}.jar %{buildroot}%{_javadir}/%{name}/integration-%{version}.jar
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-integration.pom
%add_to_maven_depmap org.hamcrest %{name}-integration %{version} JPP/%{name} integration

install -m 644 build/%{name}-text-%{version}.jar %{buildroot}%{_javadir}/%{name}/text-%{version}.jar
install -m 644 %{SOURCE7} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-text.pom
%add_to_maven_depmap org.hamcrest %{name}-text %{version} JPP/%{name} text

install -m 644 build/%{name}-unit-test-%{version}.jar %{buildroot}%{_javadir}/%{name}/unit-test-%{version}.jar

pushd %{buildroot}%{_javadir}/%{name}
for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done
popd

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}
install -m 644 build/%{name}-examples-%{version}.jar %{buildroot}%{_datadir}/%{name}-%{version}
cp -pr %{name}-examples %{buildroot}%{_datadir}/%{name}-%{version}/

%{gcj_compile} 

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/%{name}
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-2.0.4mdv2011.0
+ Revision: 605850
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-2.0.3mdv2010.1
+ Revision: 522835
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.1-2.0.2mdv2010.0
+ Revision: 425139
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0:1.1-2.0.1mdv2009.0
+ Revision: 264653
- rebuild early 2009.0 package (before pixel changes)

* Wed Apr 16 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.1-1.0.1mdv2009.0
+ Revision: 194992
- BR java-rpmbuild
- add ant.jar to classpath also
- try again to fix ant-launcher
- really add ant-launcher
- add ant-launcher to the classpath
- import hamcrest


