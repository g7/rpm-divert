# -*- coding: utf-8 -*-
#
# rpm-divert
# Copyright (C) 2018 Eugenio "g7" Paolantonio
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
The rpm-divert database is a simple JSON file that contains the list of
every diversion, per-package.

Its structure is similar to the following:

[
	{
		"package" : "custom-hello",
		"diversions" : [
			{
				"source" : "/usr/bin/hello",
				"diversion" : "/usr/bin/hello-diverted",
				"applied" : true
			}
		]
	},
	[...]
]

This is optimized for legibility, not for performance.
"""

import json

import logging

import os

from rpm_divert.package import Package

__all__ = [
	"Database"
]

DEFAULT_DATABASE_PATH = "/var/lib/rpm-divert/diversions"

logger = logging.getLogger(__name__)

class Database:

	"""
	The actual database.
	"""

	def __init__(self, path=None):
		"""
		Initialises the class.

		:param: path: the database path. If None, defaults to
		/var/lib/rpm-divert/diversions
		"""

		self.path = path or DEFAULT_DATABASE_PATH

		self._packages = {}
		self._packages_iterator = None

		self.load()

	def __iter__(self):
		"""
		Returns the iterator (us)

		:returns: this Database() instance
		"""

		self._packages_iterator = iter(self._packages)

		return self

	def __next__(self):
		"""
		Returns the next object.

		:returns: the next object in the internal dictionary
		"""

		try:
			return next(self._packages_iterator)
		except StopIteration:
			self._pacakges_iterator = None
			raise

	def __getitem__(self, package):
		"""
		Returns the requested package, as a Package object.

		If the package doesn't exist in the database, it's
		created.

		:returns: a Package object
		"""

		return self._packages.setdefault(
			package,
			Package(package)
		)

	def __delitem__(self, package):
		"""
		Deletes a package from the internal dictionary.

		:param: package: the package object to remove
		"""

		del self._packages[package]

	def get_diversions(self, package=None):
		"""
		Returns every diversion in the database for the specified
		package, or of every package if not specified.

		:params: package: if not None, limits the search on the given
		package. Defaults to none.
		:returns: a dictionary containing the package as a key, and the
		diversions list as the value
		"""

		if package is not None:
			if package in self._packages:
				return {
					package : self._packages[package].diversions
				}

			return {}

		return {
			name : pkg.diversions
			for name, pkg in self._packages.items()
		}

	def dump(self):
		"""
		Dumps the database as a list of Packages.

		:returns: a list containing the database.
		"""

		return [
			pkg.dump()
			for pkg in self._packages.values()
		]

	def save(self):
		"""
		Saves the database to self.path.
		"""

		directory = os.path.dirname(self.path)

		if not os.path.exists(directory):
			os.makedirs(directory)

		with open(self.path, "w") as f:
			f.write(
				json.dumps(
					self.dump(),
					indent=4,
					sort_keys=True
				)
			)

	def load(self):
		"""
		Loads the database.
		"""

		if not os.path.exists(self.path):
			logger.warning("Diversion database doesn't exist")
			return

		with open(self.path, "r") as f:
			_diversions = json.loads(f.read())

		for pkg in _diversions:
			_pkg = Package.new_from_dict(pkg)
			self._packages[_pkg.name] = _pkg
