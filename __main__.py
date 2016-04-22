#!/usr/bin/python

import os, shutil, sys
from subprocess import call, check_call

homedir = os.path.expanduser('~') 

appdir = os.path.join(homedir, '.bkup')

tmpdir = os.path.join(appdir, 'tmp')
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)

### clear the destination directory prior to each run (caveat emptor)
cleardestdir=True

## file name (no path) of gunzipped tarball
backupfile='home.tgz'
## backup directory
backupdir=homedir
## where to move tgz file
destdir=os.path.join(homedir, 'tmp')

def write_list_to_file(ls, fl):
	with open(fl, 'w') as out_file:
	    out_file.write('\n'.join(ls))

## include patterns
# includefile=os.path.join(homedir, '.backup-include')
includes = ['./.git-completion.bash','./.gitconfig','./test/a','./test/one.txt','./test/b/c.txt','./Code/provision/']
includefile=os.path.join(tmpdir, '.include')
write_list_to_file(includes, includefile)

## exclude patterns
excludefile=os.path.join(homedir, '.backup-exclude')

## tar commands based on tar implemntation (gnu or bsd)
# tar_gnu="tar -czvf $backupfile --files-from=$includefile --exclude-from=$excludefile"
tar_gnu=['tar', '-czvf', backupfile, '--files-from='+includefile,  '--exclude-from='+excludefile]

tar_bsd="tar -czvf $backupfile --include-from=$includefile --exclude-from=$excludefile"


if cleardestdir:
	# rm -rf $destdir/*
	shutil.rmtree(destdir)
	os.mkdir(destdir)

# ## go to back up direcroty
# cd $backupdir
os.chdir(backupdir)

# ## wrap it up (create g-zipped tarball)
# $tar_gnu || $tar_bsd
call(tar_gnu)

# ## move archive to destination
# mv $backupfile $destdir/
shutil.move(backupfile, destdir)

# #### this part is for debugging, you could impement backup rotations, etc. here

# cd $destdir
os.chdir(destdir)

# ## extract the archive
# tar xzvf $backupfile
call(["tar", "xzvf", backupfile])

# remove tmp dir
shutil.rmtree(tmpdir)