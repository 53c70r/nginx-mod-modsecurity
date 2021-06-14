%global _hardened_build 1
%global nginx_user nginx
%global debug_package %{nil}
%global with_aio 1
%global fedora_min_nginx_version 1.18.0
%global fedora_max_nginx_version 1.20.1
%global fedora_min_version 33
%global fedora_max_version 34


%if 0%{?fedora} > 22
%global with_mailcap_mimetypes 1
%endif

%ifnarch s390 s390x ppc64 ppc64le
%global with_gperftools 1
%endif

%undefine _strict_symbol_defs_build
%bcond_with geoip

Name:           nginx-mod-modsecurity
Version:        1.0.2
Release:        10%{?dist}
Summary:        ModSecurity v3 Nginx Connector
License:        ASL 2.0
BuildArch:      x86_64
URL:            https://www.modsecurity.org/

Source0:        https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{version}/modsecurity-nginx-v%{version}.tar.gz
Source1:        https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{version}/modsecurity-nginx-v%{version}.tar.gz.asc
Source2:        https://nginx.org/download/nginx-%{fedora_min_nginx_version}.tar.gz
Source3:        https://nginx.org/download/nginx-%{fedora_min_nginx_version}.tar.gz.asc
Source4:        mod-modsecurity.conf
Source5:        LICENSE
Source6:        https://nginx.org/download/nginx-%{fedora_max_nginx_version}.tar.gz
Source7:        https://nginx.org/download/nginx-%{fedora_max_nginx_version}.tar.gz.asc
Source101:      https://nginx.org/keys/is.key
Source102:      https://nginx.org/keys/maxim.key
Source103:      https://nginx.org/keys/mdounin.key
Source104:      https://nginx.org/keys/sb.key
Source105:      modsecurity.gpg

Patch0:         nginx-auto-cc-gcc.patch

%if 0%{?with_gperftools}
BuildRequires:  gperftools-devel
%endif

BuildRequires:  gcc
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
BuildRequires:  nginx-libmodsecurity
BuildRequires:  gnupg2

%if 0%{?fedora} == %{fedora_min_version}
Requires:       nginx >= %{fedora_min_nginx_version}
%endif

%if 0%{?fedora} == %{fedora_max_version}
Requires:       nginx >= %{fedora_max_nginx_version}
%endif

Requires:       GeoIP
Requires:       nginx-libmodsecurity

%description
The ModSecurity-nginx connector is the connection point between nginx and libmodsecurity (ModSecurity v3). Said another way, this project provides a communication channel between nginx and libmodsecurity. This connector is required to use LibModSecurity with nginx.

%prep
cat %{S:101} %{S:102} %{S:103} %{S:104} > %{_builddir}/nginx.gpg
cat %{SOURCE105} > %{_builddir}/modsecurity.gpg
%{gpgverify} --keyring='%{_builddir}/modsecurity.gpg' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%if 0%{?fedora} == %{fedora_min_version}
%{gpgverify} --keyring='%{_builddir}/nginx.gpg' --signature='%{SOURCE3}' --data='%{SOURCE2}'
%endif

%if 0%{?fedora} == %{fedora_max_version}
%{gpgverify} --keyring='%{_builddir}/nginx.gpg' --signature='%{SOURCE7}' --data='%{SOURCE6}'
%endif

%if 0%{?fedora} == %{fedora_min_version}
%setup -c -q -a 2
%endif

%if 0%{?fedora} == %{fedora_max_version}
%setup -c -q -a 6
%endif

%setup -T -D -a 0 -q

%if 0%{?fedora} == %{fedora_min_version}
cd nginx-%{fedora_min_nginx_version}
%endif

%if 0%{?fedora} == %{fedora_max_version}
cd nginx-%{fedora_max_nginx_version}
%endif

%patch0 -p0

%build

%if 0%{?fedora} == %{fedora_min_version}
cd nginx-%{fedora_min_nginx_version}
%endif

%if 0%{?fedora} == %{fedora_max_version}
cd nginx-%{fedora_max_nginx_version}
%endif

export DESTDIR=%{buildroot}
nginx_ldopts="$RPM_LD_FLAGS -Wl,-E"

%if 0%{?fedora} == %{fedora_min_version}
if ! ./configure \
    --prefix=%{_datadir}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --modules-path=%{_libdir}/nginx/modules \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf \
    --error-log-path=%{_localstatedir}/log/nginx/error.log \
    --http-log-path=%{_localstatedir}/log/nginx/access.log \
    --http-client-body-temp-path=%{_localstatedir}/lib/nginx/tmp/client_body \
    --http-proxy-temp-path=%{_localstatedir}/lib/nginx/tmp/proxy \
    --http-fastcgi-temp-path=%{_localstatedir}/lib/nginx/tmp/fastcgi \
    --http-uwsgi-temp-path=%{_localstatedir}/lib/nginx/tmp/uwsgi \
    --http-scgi-temp-path=%{_localstatedir}/lib/nginx/tmp/scgi \
    --pid-path=/run/nginx.pid \
    --lock-path=/run/lock/subsys/nginx \
    --user=%{nginx_user} \
    --group=%{nginx_user} \
%if 0%{?with_aio}
    --with-file-aio \
%endif
    --with-ipv6 \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --with-stream_ssl_preread_module \
    --with-http_addition_module \
    --with-http_xslt_module=dynamic \
    --with-http_image_filter_module=dynamic \
%if %{with geoip}
    --with-http_geoip_module=dynamic \
%endif
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_slice_module \
    --with-http_stub_status_module \
    --with-http_perl_module=dynamic \
    --with-http_auth_request_module \
    --with-mail=dynamic \
    --with-mail_ssl_module \
    --with-pcre \
    --with-pcre-jit \
    --with-stream=dynamic \
    --with-stream_ssl_module \
%if 0%{?with_gperftools}
    --with-google_perftools_module \
%endif
    --with-debug \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
    --with-ld-opt="$nginx_ldopts" \
    --add-dynamic-module="../modsecurity-nginx-v%{version}"; then
    : configure failed
    cat objs/autoconf.err
    exit 1
fi
%endif

%if 0%{?fedora} == %{fedora_max_version}
    ./configure \
    --prefix=/usr/share/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib64/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --http-client-body-temp-path=/var/lib/nginx/tmp/client_body \
    --http-proxy-temp-path=/var/lib/nginx/tmp/proxy \
    --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi \
    --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi \
    --http-scgi-temp-path=/var/lib/nginx/tmp/scgi \
    --pid-path=/run/nginx.pid \
    --lock-path=/run/lock/subsys/nginx \
    --user=nginx \
    --group=nginx \
    --with-compat \
    --with-debug \
    --with-file-aio \
    --with-google_perftools_module \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_degradation_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_image_filter_module=dynamic \
    --with-http_mp4_module \
    --with-http_perl_module=dynamic \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-http_xslt_module=dynamic \
    --with-mail=dynamic \
    --with-mail_ssl_module \
    --with-pcre \
    --with-pcre-jit \
    --with-stream=dynamic \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-threads \
    --add-dynamic-module="../modsecurity-nginx-v%{version}"
%endif

make modules %{?_smp_mflags}

%install

%if 0%{?fedora} == %{fedora_min_version}
%{__install} -p -D -m 0755 ./nginx-%{fedora_min_nginx_version}/objs/ngx_http_modsecurity_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so
%endif

%if 0%{?fedora} == %{fedora_max_version}
%{__install} -p -D -m 0755 ./nginx-%{fedora_max_nginx_version}/objs/ngx_http_modsecurity_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so
%endif

%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/nginx/modules/mod-modsecurity.conf
%{__install} -p -D -m 0644 %{SOURCE5} %{buildroot}%{_datarootdir}/licenses/%{NAME}/LICENSE

%files
%defattr (-,root,root)
%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so
%{_datadir}/nginx/modules/mod-modsecurity.conf
%{_datarootdir}/licenses/%{NAME}/LICENSE
