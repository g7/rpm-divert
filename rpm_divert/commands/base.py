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

import argparse

from collections import namedtuple

CommandDetail = namedtuple("CommandDetail", ["help", "args"])

def command(
	help=None,
	args=[]
):
	"""
	Decorator that stores details on a command.
	"""

	subparser_details = CommandDetail(help=help, args=args)

	def decorator(function):
		"""
		The actual decorator.
		"""

		function.__subparser_details = subparser_details

		return function

	return decorator

def generate_arguments(commands):
	"""
	Generates the arguments.

	:param: commands: a list of callables decorated with @command
	:returns: an ArgumentParser instance
	"""

	parser = argparse.ArgumentParser()

	command_subparsers = parser.add_subparsers(dest="command")

	for command in commands:
		if not hasattr(command, "__subparser_details"):
			continue

		details = getattr(command, "__subparser_details")

		subparser = command_subparsers.add_parser(
			command.__name__,
			help=details.help
		)

		for argument_arg, argument_details in details.args:
			subparser.add_argument(
				*argument_details.pop("arguments"),
				**argument_details
			)

	return parser
