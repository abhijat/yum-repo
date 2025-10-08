# Package repositories for rpm and debian packages

This repository contains scripts and definitions for setting up YUM and apt repositories for Linux users to install
dragonfly packages.

The repositories are served as static websites. The generate-site workflow is used to set up and deploy the sites using
scripts and definitions included here.

The workflow does the following tasks:

* Download the latest 5 releases from dragonfly releases page, specifically deb and rpm assets
* Set up a directory structure separating deb and rpm files into version specific paths
* Sign the packages (see note on GPG)
* Deploy the assets prepared, along with the public GPG key and repo definitions for apt and rpm tooling

### Signing packages

The packages are signed using the GPG key imported from the secret GPG_PRIVATE_KEY in this repository.

The corresponding public key is served with site assets, so the apt/yum/dnf based tooling can consume the public key to
verify package integrity.

### TODO

- [ ] debian packages signing
- [ ] debian repo metadata setup
- [ ] tests asserting that packages are installable?
