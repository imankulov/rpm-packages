rpm-packages
============

Fresh specs for RHEL-based and RHEL-derived distributions (CentOS, Amazon Linux AMI)

Brush up
--------

Put in your `/etc/mock/site-defaults.cfg`


    config_opts['scm_opts']['method'] = 'git'
    config_opts['scm_opts']['git_get'] = "bash -c 'git clone SCM_BRN git://github.com/imankulov/rpm-packages.git SCM_PKG && mv SCM_PKG/sources/* SCM_PKG/'"
    config_opts['scm_opts']['spec'] = 'specs/SCM_PKG.spec'
    config_opts['scm_opts']['git_timestamps'] = False
    config_opts['scm_opts']['ext_src_dir'] = '/tmp/sources'

Then download sources from specs. You may pick one or more specfiles.

    ./helpers/download_sources.py specs/*.spec 

Then build a package of your dream.

    mock --scm-enable  --scm-option package=python-pip -v
