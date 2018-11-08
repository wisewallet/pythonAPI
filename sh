#!/bin/sh
set -e
#
# This script is meant for quick & easy install via:
#   'curl -sSL https://do-agent.sh | sh'
# or:
#   'wget -qO- https://do-agent.sh | sh'

dist=""
dist_version=""
dist_version_family=""
dist_pretty=""
droplet_id=""

check_distro() {
    # Detect the distribution attributes
    # We use /etc/os-release since its standard
    if [  -f /etc/os-release  ]; then
        dist=$(awk -F= '$1 == "ID" {gsub("\"", ""); print$2}' /etc/os-release)
        dist_version=$(awk -F= '$1 == "VERSION_ID" {gsub("\"", ""); print$2}' /etc/os-release)
        dist_pretty=$(awk -F= '$1 == "PRETTY_NAME" {gsub("\"", ""); print$2}' /etc/os-release)
    elif [ -f /etc/redhat-release ]; then
        dist=$(awk '{print tolower($1)}' /etc/redhat-release)
        dist_version=$(awk '{print tolower($3)}' /etc/redhat-release)
        dist_pretty=$(awk '{print$1" "$3}' /etc/redhat-release)
    else
        cat <<-EOF

  Automated installation is not supported on distributions
  with out /etc/os-release or /etc/redhat-release.

EOF
        exit 1
    fi

    dist=${dist?unable to determine the distribution}
    dist_version=${dist_version?unable to determine distribution version}
    dist_version_family=$(echo ${dist_version} | awk -F. '{print$1}')
    dist_version_family=${dist_version_family?failed to determine the distribution major number}
}

command_exists() {
  command -v "$@" > /dev/null 2>&1
}

write_rhel_repo() {
  $sh_c '
cat > /etc/yum.repos.d/digitalocean-agent.repo <<"EOM"
[digitalocean-agent]
name=DigitalOcean agent
baseurl=https://repos.sonar.digitalocean.com/yum/$basearch
failovermethod=priority
enabled=1
gpgcheck=1
gpgkey=https://repos.sonar.digitalocean.com/sonar-agent.asc
EOM

rpm --import https://repos.sonar.digitalocean.com/sonar-agent.asc
'
}

install_yum() {
  write_rhel_repo
  $sh_c 'yum install do-agent -y'
}

install_dnf() {
  write_rhel_repo
  $sh_c 'dnf install do-agent -y'
}

install_apt() {
  $sh_c '
export DEBIAN_FRONTEND=noninteractive

apt-get -qqy update
apt-get -y install apt-transport-https curl
curl https://repos.sonar.digitalocean.com/sonar-agent.asc | apt-key add -

cat > /etc/apt/sources.list.d/digitalocean-agent.list <<EOF
deb https://repos.sonar.digitalocean.com/apt main main
EOF

apt-get -qqy update
apt-get -y install do-agent
'
}

check_do() {
  # DigitalOcean embedded platform information in the DMI data.
  $sh_c '
  read droplet_id < /sys/devices/virtual/dmi/id/product_serial
  read sys_vendor < /sys/devices/virtual/dmi/id/bios_vendor
  if ! [ "$sys_vendor" = "DigitalOcean" ]; then
    cat <<-EOF

    The DigitalOcean Agent is only supported on DigitalOcean right now.
    It may be supported on other platforms in the future.

    If you are seeing this message on an older droplet, you may need to power-off
    and then power-on at http://cloud.digitalocean.com. After power-cycling,
    please re-run this script.

EOF
    exit 1
  fi
'
}

not_supported() {
  cat <<-EOF

 ${dist_pretty} is not supported at this time.

 Scripted installation of the DigitalOcean Agent only supported on:
    CentOS 6 and later
    Debian 8.0 and later
    Fedora 23 and later
    Ubuntu 14.04 and later

EOF
  exit 1
}

do_install() {
  user="$(id -un 2>/dev/null || true)"

  sh_c='sh -c'
  if [ "$user" != 'root' ]; then
    if command_exists sudo; then
      sh_c='sudo -E sh -c'
    elif command_exists su; then
      sh_c='su -c'
    else
      cat >&2 <<-'EOF'
      Error: this installer needs the ability to run commands as root.
      We are unable to find either "sudo" or "su" available to make this happen.
EOF
      exit 1
    fi
  fi

  # Check to make sure we're on DigitalOcean
  check_do

  # Get the distro info
  check_distro

  echo "Detected ${dist_pretty}...installing the DigitalOcean Agent"

  # Run setup for each distro accordingly
  case "$dist" in
    debian)
      if [ "$dist_version_family" -ge 8 ]; then
        install_apt
        exit 0
      fi
      not_supported
      ;;

    ubuntu)
      if [ "$dist_version_family" -gt 12 ]; then
        install_apt
        exit 0
      fi
      not_supported
      ;;

    centos)
      if [ "$dist_version_family" -ge 6 ]; then
        install_yum
        exit 0
      fi
      not_supported
      ;;

    fedora)
      if [ "${dist_version_family:-23}" -ge 24 ]; then
        install_dnf
        exit 0
      fi
      not_supported
      ;;

    *)
      not_supported
      ;;
  esac

}

# wrapped up in a function so that we have some protection against only getting
# half the file during "curl do-agent.sh | sh"
do_install
