Mercurial (HG) hook
===================

Mercurial (HG) hook for detecting unwanted sequences in the current commit diff.

Usage
-----

Add to .hg/hgrc (or ~/.hgrc) the following lines:<br />
<br />
[hooks]<br />
pretxncommit.bxcommit = python:PATH_TO_THIS_REPO/src/bxcommit.py:bx_commit_check<br />
[bxcommit]<br />
forbidden = some:unwanted:sequences:separated:with:colon
