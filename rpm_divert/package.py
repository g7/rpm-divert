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
A Package representation.
"""

import logging

from rpm_divert.diversion import Diversion

logger = logging.getLogger(__name__)

__all__ = [
	"Package"
]

class Package:

	"""
		{
		"package" : "hello-custom",
		"diversions" : [
			{
				"source" : "/usr/bin/hello",
				"diversion" : "/usr/bin/hello-diverted",
				"action" : "symlink",
				"replacement" : "/usr/lib/hello-custom/hello",
				"applied" : true
			}
		]
	}
	"""

	def __init__(self, name):
		"""
		Initialises the class.

		:param: name: the package name.
		"""

		self.name = name
		self.diversions = set()

	@classmethod
	def new_from_dict(cls, package_dict):
		"""
		Creates a new package from a package dict.

		:param: block: the dictionary to parse
		:returns: a valid Package() object.
		"""

		pkg = cls(package_dict["package"])

		# Load diversions
		for diversion in package_dict.get("diversions", []):
			pkg.diversions.add(
				Diversion.new_from_dict(diversion)
			)

		return pkg

	def dump(self):
		"""
		Dumps the package as a dictionary.

		:returns: a dictionary containing the package
		"""

		return {
			"package" : self.name,
			"diversions" : [
				diversion.dump()
				for diversion in self.diversions
			]
		}

	def __repr__(self):
		"""
		:returns: a representation of the object.
		"""

		return "<Package: %s>" % self.name
