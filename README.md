rpm-divert
==========

`rpm-divert` is a replacement for dpkg-divert for non-Debian based systems.

It's terribly hacky, and you shouldn't use it if your package manager
supports some sort of diversions mechanisms (like `dpkg` does).

`rpm-divert` *doesn't* support local diversions. Every diversion must be
linked to a package (which is not actually checked in the package manager
database, so it can be bogus).

Diversions aren't applied right away, but should be executed via the apply/unapply
commands. This allows usage from RPM triggers to keep a consistent system
while upgrading the packages touched by the diversions.

Usage
-----

	usage: rpm-divert.py [-h] {add,remove,apply,unapply,list} ...

	positional arguments:
	  {add,remove,apply,unapply,list}
		add                 adds a diversion
		remove              removes a diversion
		apply               applies the diversions
		unapply             unapplies the diversions
		list                lists applied diversions

	optional arguments:
	  -h, --help            show this help message and exit

### add

	usage: rpm-divert.py add [-h] [--action ACTION] [--replacement REPLACEMENT]
							 package source diversion

	positional arguments:
	  package               the package where to link the diversion
	  source                the file to divert
	  diversion             the diversion (i.e. the file source is renamed to)

	optional arguments:
	  -h, --help            show this help message and exit
	  --action ACTION, -a ACTION
							The action, currently 'symlink' or 'nothing'. Defaults
							to 'nothing'
	  --replacement REPLACEMENT, -r REPLACEMENT
							The replacement file to symlink to source. Used only
							if --action=symlink

### remove

	usage: rpm-divert.py remove [-h] package source

	positional arguments:
	  package     the package where to link the diversion
	  source      the file to divert

	optional arguments:
	  -h, --help  show this help message and exit

### apply

	usage: rpm-divert.py apply [-h] [--package PACKAGE]

	optional arguments:
	  -h, --help            show this help message and exit
	  --package PACKAGE, -p PACKAGE
							the package to process. If omitted, every diversion is
							applied.

### unapply

	usage: rpm-divert.py unapply [-h] [--package PACKAGE]

	optional arguments:
	  -h, --help            show this help message and exit
	  --package PACKAGE, -p PACKAGE
							the package to process. If omitted, every diversion is
							unapplied.

### list

	usage: rpm-divert.py list [-h] [--package PACKAGE]

	optional arguments:
	  -h, --help            show this help message and exit
	  --package PACKAGE, -p PACKAGE
							the package to process. If omitted, every diversion is
							listed.

