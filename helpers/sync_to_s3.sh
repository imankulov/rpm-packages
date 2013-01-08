#!/bin/bash
bucket=${1:-$YUM_S3_BUCKET}
test "${bucket}" || { echo "Usage: '$0 s3-bucket-name' or 'YUM_S3_BUCKET='s3-bucket-name' $0'"; exit 1; }

cd  # chroot to home directory

set -x
mkdir -p repo/{SRPMS,x86_64}

mv /var/lib/mock/epel-6-x86_64/result/*.src.rpm repo/SRPMS
mv /var/lib/mock/epel-6-x86_64/result/*.x86_64.rpm repo/x86_64
mv /var/lib/mock/epel-6-x86_64/result/*.noarch.rpm repo/x86_64

s3cmd get --recursive --skip-existing s3://$bucket/repo
ls -d repo/* | xargs -i createrepo {}
s3cmd sync --delete-removed repo s3://$bucket/
