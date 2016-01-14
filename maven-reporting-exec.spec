%global pkg_name maven-reporting-exec
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.1
Release:        4.12%{?dist}
BuildArch:      noarch
Summary:        Classes to manage report plugin executions with Maven 3

License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-reporting-exec/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/reporting/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-invoker-plugin
BuildRequires:  %{?scl_prefix}maven-shared
BuildRequires:  %{?scl_prefix}maven-surefire-plugin
BuildRequires:  %{?scl_prefix}maven-surefire-provider-junit
BuildRequires:  %{?scl_prefix}plexus-containers-component-metadata


%description
Classes to manage report plugin executions with Maven 3. Contains classes for
managing and configuring reports and their execution.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
The API documentation of %{pkg_name}.



%prep
%setup -qn %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# convert CR+LF to LF
sed -i 's/\r//g' pom.xml src/main/java/org/apache/maven/reporting/exec/*

# We have different sonatype groupId and java package name
find -iname '*.java' -exec sed -i 's/org.eclipse.aether/org.sonatype.aether/g' '{}' ';'

%pom_xpath_set "pom:groupId[text()='org.eclipse.aether']" org.sonatype.aether
%pom_remove_plugin org.apache.maven.plugins:maven-enforcer-plugin
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Test are skipped because there are errors with PlexusLogger
# More info possibly here:
# https://docs.sonatype.org/display/AETHER/Using+Aether+in+Maven+Plugins?focusedCommentId=10485782#comment-10485782
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.12
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.1-4.11
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.1-4.10
- Mass rebuild 2015-01-06

* Thu Jul 31 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.9
- Fix javadoc subpackage generation
- Resolves: rhbz#1125205

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.8
- Mass rebuild 2014-05-26

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.7
- Fix directory ownership

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.5
- Mass rebuild 2014-02-18
- Add missing BR: maven-shared

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1-4
- Mass rebuild 2013-12-27

* Mon Jun 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-3
- Remove unused source

* Mon May 06 2013 Tomas Radej <tradej@redhat.com> - 1.1-2
- Removed aether BR

* Mon Apr 22 2013 Tomas Radej <tradej@redhat.com> - 1.1-1
- Updated to latest upstream version
- Building with maven-local

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.2-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Tomas Radej <tradej@redhat.com> - 1.0.2-1
- Updated to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 tradej <tradej@redhat.com> 1.0.1-3
- Added dist macro to release

* Thu Aug 11 2011 tradej <tradej@redhat.com> 1.0.1-2
- Changed BuildArch to noarch

* Wed Aug 10 2011 tradej <tradej@redhat.com> 1.0.1-1
- Initial release (thanks to akurtakov, jcapik and the GULaG team for help)

