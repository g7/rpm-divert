#!/usr/bin/env python3
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

import sys

import logging

import rpm_divert.commands as commands

from rpm_divert.commands.base import generate_arguments

from rpm_divert import Database, Diversion

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

if __name__ == "__main__":
	db = Database()
	db.load()

	# Generate argument parser
	parser = generate_arguments(
		[
			getattr(commands, command)
			for command in commands.COMMANDS
		]
	)

	args = parser.parse_args()

	command = args.command

	if command == None:
		# Show help
		parser.parse_args(["-h"])
		sys.exit(0) # Never called

	try:
		commands.route_from_namespace(args, context_dict={"database" : db})
	finally:
		# Save
		if command != "list":
			db.save()
