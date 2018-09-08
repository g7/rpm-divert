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
A Diversion representation.
"""

import logging

import shutil

import os

logger = logging.getLogger(__name__)

__all__ = [
	"DiversionAction",
	"Diversion"
]

class DiversionAction:

	NOTHING = "nothing"

	SYMLINK = "symlink"

	COPY = "copy"

class ApplyActionException(Exception):
	pass

class UnapplyActionException(Exception):
	pass

class Diversion:

	"""
			{
				"source" : "/usr/bin/hello",
				"diversion" : "/usr/bin/hello-diverted",
				"action" : "symlink",
				"replacement" : "/usr/lib/hello-custom/hello",
				"applied" : true
			}
	"""

	def __init__(self, source, diversion, action=DiversionAction.NOTHING, replacement=None, applied=False):
		"""
		Initialises the class.

		:param: source: the source file
		:param: diversion: the path of the diverted source
		:param: action: the action to take
		:param: replacement: the replacement file
		:param: applied: the diversion status
		"""

		self.source = source
		self.diversion = diversion
		self.action = action
		self.replacement = replacement
		self.applied = applied

	@classmethod
	def new_from_dict(cls, diversion_dict):
		"""
		Creates a new package from a diversion dict.

		:param: block: the dictionary to parse
		:returns: a valid Diversion() object.
		"""

		return cls(
			diversion_dict.pop("source"),
			diversion_dict.pop("diversion"),
			**diversion_dict
		)

	def apply(self, create_directory=False):
		"""
		Applies the diversion.

		:params: create_directory: if True, creates the directory tree
		of the diversion if it doesn't exist. Defaults to False.
		"""

		if self.applied:
			return

		diversion_dir = os.path.dirname(self.diversion)

		logger.info("diverting \"%s\" to \"%s\"" % (self.source, self.diversion))

		# Create directory tree if we should
		if create_directory and not os.path.exists(diversion_dir):
			os.makedirs(diversion_dir)

		# Safety checks
		if False in (
			os.path.exists(self.source),
			not os.path.exists(self.diversion),
			os.path.isdir(diversion_dir)
		):
			raise ApplyActionException("Unable to apply diversion, safety checks failed")

		try:
			os.rename(self.source, self.diversion)

			if self.action == DiversionAction.SYMLINK:
				# Handle symlink action
				# TODO: check replacement's existence
				logger.info("symlinking \"%s\" to \"%s\"" % (self.replacement, self.source))
				os.symlink(self.replacement, self.source)

				# Copy permission bits
				shutil.copymode(self.diversion, self.source)
			elif self.action == DiversionAction.COPY:
				# Handle copy action
				# TODO: check replacement's existence
				logger.info("copying \"%s\" to \"%s\"" % (self.replacement, self.source))
				shutil.copy2(self.replacement, self.source)
		except:
			raise ApplyActionException("Unable to apply diversion")

		self.applied = True

	def unapply(self):
		"""
		Unapplies the diversion.
		"""

		if not self.applied:
			return

		logger.info("restoring diversion \"%s\" to \"%s\"" % (self.source, self.diversion))

		# Special case for DiversionAction.NOTHING:
		#
		# RPM's twisted package upgrade flow installs first the new
		# files, and only then it starts processing triggers.
		#
		# When there is no replacement diversion, RPM will install the
		# new version of the diverted file first and so rpm-divert's safety
		# checks will fail as the source file exists
		# (as is the new, updated, one) while it shouldn't.
		#
		# Handle this special case by removing the previously diverted
		# files while not touching the new ones.
		if self.action == DiversionAction.NOTHING and not False in (
			os.path.exists(self.source),
			os.path.exists(self.diversion)
		):
			logger.warning("Diversion source already exists, removing old diversion and marking as unapplied")

			try:
				os.remove(self.diversion)
			except:
				raise UnapplyActionException("Unable to unapply diversion")
			else:
				self.applied = False

			return

		# Safety checks
		if False in (
			(not os.path.exists(self.source) if self.action == DiversionAction.NOTHING else os.path.exists(self.source)),
			os.path.exists(self.diversion),
		):
			raise UnapplyActionException("Unable to unapply diversion, safety checks failed")

		try:
			if self.action in (DiversionAction.SYMLINK, DiversionAction.COPY):
				# Handle symlink and copy actions
				logger.info("removing replacement \"%s\"" % self.source)
				os.remove(self.source)

			os.rename(self.diversion, self.source)

		except:
			raise UnapplyActionException("Unable to unapply diversion")

		self.applied = False

	def dump(self):
		"""
		Dumps the diversion as a dictionary.

		:returns: a dictionary containing the diversion.
		"""

		return {
			"source" : self.source,
			"diversion" : self.diversion,
			"action" : self.action,
			"replacement" : self.replacement,
			"applied" : self.applied
		}

	def __hash__(self):
		"""
		:returns: the hash of the object.
		"""

		return hash(self.source)

	def __eq__(self, other):
		"""
		:returns: True if the Diversion is equal to the supplied one.
		"""

		return (self.source == other.source)

	def __repr__(self):
		"""
		:returns: a representation of the object.
		"""

		return "<Diversion: \"%s\" -> \"%s\">" % (self.source, self.diversion)
