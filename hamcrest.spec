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

%define with()          %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%define without()       %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%define bcond_with()    %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}

# This option controls integration which requires easymock2 and jmock
%bcond_with integration

# This option controls jarjar on qdox
# Since bundling the qdox classes prevents upgrades, we disable it by default
%bcond_with jarjar

# This option controls tests which requires ant-junit and testng
%bcond_with tests

# If integration is disabled, then tests are disabled
%if %without integration
%bcond_with tests
%endif

Name:           hamcrest
Version:        1.1
Release:        10.7
Summary:        Library of matchers for building test expressions
License:        BSD
URL:            http://code.google.com/p/hamcrest/
Group:          Development/Java
Source0:        http://hamcrest.googlecode.com/files/hamcrest-1.1.tgz
Source1:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-parent/1.1/hamcrest-parent-1.1.pom
Source2:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-library/1.1/hamcrest-library-1.1.pom
Source3:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-integration/1.1/hamcrest-integration-1.1.pom
Source4:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-generator/1.1/hamcrest-generator-1.1.pom
Source5:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.1/hamcrest-core-1.1.pom
Source6:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-all/1.1/hamcrest-all-1.1.pom
Source7:        hamcrest-text-1.1.pom
Source8:        hamcrest-core-MANIFEST.MF
Patch0:         hamcrest-1.1-build.patch
Patch1:         hamcrest-1.1-no-jarjar.patch
Patch2:         hamcrest-1.1-no-integration.patch
Requires:       java-1.6.0
%if %with integration
Requires:       easymock2
Requires:       jmock
%endif
Requires:       qdox
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-1.6.0-devel
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  zip
%if %with integration
BuildRequires:  easymock2
%endif
%if %with jarjar
BuildRequires:  jarjar
%endif
%if %with integration
BuildRequires:  jmock
%endif
BuildRequires:  junit
BuildRequires:  junit4
BuildRequires:  qdox
%if %with tests
BuildRequires:  testng
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

Requires(post): jpackage-utils >= 0:1.7.4
Requires(postun): jpackage-utils >= 0:1.7.4

%description
Provides a library of matcher objects (also known as constraints or predicates)
allowing 'match' rules to be defined declaratively, to be used in other
frameworks. Typical scenarios include testing frameworks, mocking libraries and
UI validation rules.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
BuildArch:      noarch

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Java
Summary:        Demos for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       junit
Requires:       junit4
%if %with tests
Requires:       testng
%endif

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
find . -type f -name "*.jar" | xargs -t rm
# BUILD/hamcrest-%{version}/lib/generator/jarjar-1.0rc3.jar.no
%if %with jarjar
ln -sf $(build-classpath jarjar) lib/generator/
%endif
# BUILD/hamcrest-1.1/lib/generator/qdox-1.6.1.jar.no
ln -sf $(build-classpath qdox) lib/generator/
# BUILD/hamcrest-1.1/lib/integration/easymock-2.2.jar.no
%if %with integration
ln -sf $(build-classpath easymock2) lib/integration/
%endif
# BUILD/hamcrest-1.1/lib/integration/jmock-1.10RC1.jar.no
%if %with integration
ln -sf $(build-classpath jmock) lib/integration/
%endif
# BUILD/hamcrest-1.1/lib/integration/junit-3.8.1.jar.no
ln -sf $(build-classpath junit) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/junit-4.0.jar.no
ln -sf $(build-classpath junit4) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/testng-4.6-jdk15.jar.no
%if %with tests
ln -sf $(build-classpath testng-jdk15) lib/integration/
%endif
%patch0 -p0
%if %without jarjar
%patch1 -p1
%endif
%if %without integration
%patch2 -p1
%endif

perl -pi -e 's/\r$//g' LICENSE.txt

%build
export CLASSPATH=$(build-classpath qdox)
export OPT_JAR_LIST="junit ant/ant-junit"
%if %with integration
ant -Dant.build.javac.source=1.5 -Dversion=%{version} -Dbuild.sysclasspath=first all javadoc
%else
ant -Dant.build.javac.source=1.5 -Dversion=%{version} -Dbuild.sysclasspath=first clean core generator library text bigjar javadoc
%endif

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE8} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{name}-core-%{version}.jar META-INF/MANIFEST.MF

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-parent.pom
%add_to_maven_depmap org.hamcrest %{name}-parent %{version} JPP/%{name} parent

install -m 644 build/%{name}-all-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/all-%{version}.jar
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-all.pom
%add_to_maven_depmap org.hamcrest %{name}-all %{version} JPP/%{name} all

install -m 644 build/%{name}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/core-%{version}.jar
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-core.pom
%add_to_maven_depmap org.hamcrest %{name}-core %{version} JPP/%{name} core

install -m 644 build/%{name}-generator-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/generator-%{version}.jar
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-generator.pom
%add_to_maven_depmap org.hamcrest %{name}-generator %{version} JPP/%{name} generator

install -m 644 build/%{name}-library-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/library-%{version}.jar
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-library.pom
%add_to_maven_depmap org.hamcrest %{name}-library %{version} JPP/%{name} library

%if %with integration
install -m 644 build/%{name}-integration-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/integration-%{version}.jar
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-integration.pom
%add_to_maven_depmap org.hamcrest %{name}-integration %{version} JPP/%{name} integration
%endif

install -m 644 build/%{name}-text-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/text-%{version}.jar
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-text.pom
%add_to_maven_depmap org.hamcrest %{name}-text %{version} JPP/%{name} text

%if %with tests
install -m 644 build/%{name}-unit-test-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/unit-test-%{version}.jar
%endif

pushd $RPM_BUILD_ROOT%{_javadir}/%{name}
for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done
popd

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%if %with integration
install -m 644 build/%{name}-examples-%{version}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif
cp -pr %{name}-examples $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/all-%{version}.jar
%{_javadir}/%{name}/all.jar
%{_javadir}/%{name}/core-%{version}.jar
%{_javadir}/%{name}/core.jar
%{_javadir}/%{name}/generator-%{version}.jar
%{_javadir}/%{name}/generator.jar
%if %with integration
%{_javadir}/%{name}/integration-%{version}.jar
%{_javadir}/%{name}/integration.jar
%endif
%{_javadir}/%{name}/library-%{version}.jar
%{_javadir}/%{name}/library.jar
%{_javadir}/%{name}/text-%{version}.jar
%{_javadir}/%{name}/text.jar
%if %with tests
%{_javadir}/%{name}/unit-test-%{version}.jar
%{_javadir}/%{name}/unit-test.jar
%endif
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}-%{version}
%{_datadir}/%{name}

