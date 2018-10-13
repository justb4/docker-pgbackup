#!/bin/bash
echo "listing available backups"
echo "-------------------------"
find /backup -type f -name '*.sql.gz'
