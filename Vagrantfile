# -*- mode: ruby -*-
# vi: set ft=ruby :

# This Vagrantfile will build an RPM of the current version of the RPM spec
# Just run vagrant up, and wait for the rpm and srpm to be written to the cwd.

$buildrpm = <<BUILDRPM
echo "Running the HAProxy build script"

VERSION=`grep "^%define version" /vagrant/spec/haproxy.spec | cut -d ' ' -f 3`
echo Building HAProxy ${VERSION}

echo "Installing yum dependencies"
sudo yum install -y rpmdevtools pcre-devel openssl-devel
sudo yum groupinstall -y 'Development Tools'
echo "Yum depenencies installed."

echo "Setting up RPM build env"
rpmdev-setuptree

echo "Downloading HAProxy"
curl -o ~/rpmbuild/SOURCES/haproxy-${VERSION}.tar.gz http://www.haproxy.org/download/1.5/src/haproxy-${VERSION}.tar.gz

echo "Copying configs from git."
cp /vagrant/conf/* ~/rpmbuild/SOURCES/
cp /vagrant/spec/* ~/rpmbuild/SPECS/

echo "Building..."
cd ~/rpmbuild/
rpmbuild -ba SPECS/haproxy.spec

echo "Copying output to the vagrant share."
cp ~/rpmbuild/RPMS/x86_64/* /vagrant
cp ~/rpmbuild/SRPMS/* /vagrant

echo "Done building HAProxy " ${VERSION}
BUILDRPM

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Bare bones CentOS 6.5 box from a trustworthy community member.
  config.vm.box = "centos-65-x64-virtualbox-nocm.box"
  config.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/centos-65-x64-virtualbox-nocm.box"

  # This optional plugin caches RPMs for faster rebuilds.
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :machine
  end

  config.vm.provision "shell", privileged: false, inline: $buildrpm
end
