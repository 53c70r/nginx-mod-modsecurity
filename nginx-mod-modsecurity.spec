%global _hardened_build 1
%global nginx_user nginx
%global debug_package %{nil}
%global with_aio 1

%if 0%{?fedora} > 22
%global with_mailcap_mimetypes 1
%endif

%if 0%{?fedora} < 37
%global nginx_version 1.20.2
%endif

%if 0%{?fedora} >= 37
%global nginx_version 1.22.1
%endif

%ifnarch s390 s390x ppc64 ppc64le
%global with_gperftools 1
%endif

%undefine _strict_symbol_defs_build
%bcond_with geoip

Name:           modsecurity-nginx
Version:        1.0.3
Release:        10%{?dist}
Summary:        ModSecurity v3 Nginx Connector
License:        ASL 2.0
URL:            https://www.modsecurity.org/

Source0:        https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{version}/modsecurity-nginx-v%{version}.tar.gz
Source1:        https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{version}/modsecurity-nginx-v%{version}.tar.gz.asc
Source2:        https://nginx.org/download/nginx-%{nginx_version}.tar.gz
Source3:        https://nginx.org/download/nginx-%{nginx_version}.tar.gz.asc
Source4:        mod-modsecurity.conf
Source101:      https://nginx.org/keys/thresh.key
Source102:      https://nginx.org/keys/maxim.key
Source103:      https://nginx.org/keys/mdounin.key
Source104:      https://nginx.org/keys/sb.key
Source105:      modsecurity.gpg

Patch0:         nginx-auto-cc-gcc.patch

%if 0%{?with_gperftools}
BuildRequires:  gperftools-devel
%endif

BuildRequires:  gcc
BuildRequires:  sed
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  libxslt-devel
BuildRequires:  gd-devel
BuildRequires:  GeoIP-devel
BuildRequires:  libcurl-devel
BuildRequires:  yajl-devel
BuildRequires:  lmdb-devel
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  perl-ExtUtils-Embed
BuildRequires:  libmodsecurity-nginx-devel
BuildRequires:  gnupg
BuildRequires:  nginx

Requires:       nginx >= %{nginx_version}
Requires:       libmodsecurity-nginx

%description
The ModSecurity-nginx connector is the connection point between nginx and libmodsecurity (ModSecurity v3).
Said another way, this project provides a communication channel between nginx and libmodsecurity.
This connector is required to use LibModSecurity with nginx.

%prep
cat %{S:101} %{S:102} %{S:103} %{S:104} > %{_builddir}/nginx.gpg
cat %{SOURCE105} > %{_builddir}/modsecurity.gpg
%{gpgverify} --keyring='%{_builddir}/modsecurity.gpg' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%{gpgverify} --keyring='%{_builddir}/nginx.gpg' --signature='%{SOURCE3}' --data='%{SOURCE2}'
sed -i "s/MODULE_PATH/\%{_prefix}\%{_lib}\/nginx\/modules\/ngx_http_modsecurity_module.so/g" mod-modsecurity.conf

# extract modsecurity-nginx
%setup -n modsecurity-nginx-v%{version}
# extract nginx next to modsecurity-nginx
%setup -T -b 2 -n nginx-%{nginx_version}
%patch0 -p 0

%build

export DESTDIR=%{buildroot}
	
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --add-dynamic-module="../modsecurity-nginx-v%{version}"

$configure
make modules %{?_smp_mflags}

%install
%{__install} -p -D -m 0755 objs/ngx_http_modsecurity_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/nginx/modules/mod-modsecurity.conf

%files
%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so
%{_datadir}/nginx/modules/mod-modsecurity.conf
%license ../modsecurity-nginx-v%{version}/LICENSE

%changelog
* Sun Mar 5 2023 Silvan Nagl <mail@53c70r.de> 1.0.3-10
- Use a more generic build
