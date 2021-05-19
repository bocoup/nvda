# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides custom asserts for system tests.
"""
from NvdaSpeechMappings import NvdaSpeechMappings
from robot.libraries.BuiltIn import BuiltIn
builtIn: BuiltIn = BuiltIn()


# In Robot libraries, class name must match the name of the module. Use caps for both.
class AssertsLib:
	@staticmethod
	def strings_match(actual, expected, ignore_case=False):
		try:
			builtIn.should_be_equal_as_strings(
				actual,
				expected,
				msg="Actual speech != Expected speech",
				ignore_case=ignore_case
			)
		except AssertionError:
			builtIn.log(
				"repr of actual vs expected (ignore_case={}):\n{}\nvs\n{}".format(
					ignore_case,
					repr(actual),
					repr(expected)
				)
			)
			raise

	@staticmethod
	def not_doc_boundary(command, actual, args, ignore_case=False):
		try:
			for unexpected in ('no previous ', 'no next '):
				builtIn.should_not_contain(
					actual,
					unexpected,
					msg='{}: {}\nUnexpected document boudary'.format(command, ', '.join(args)),
					ignore_case=ignore_case
				)
		except AssertionError:
			builtIn.log(
				"Actual (ignore_case={}):\n{}".format(
					ignore_case,
					repr(actual)
				)
			)
			raise

	@staticmethod
	def aria_at(command, actual, args, ignore_case=False):
		try:
			expected = args[0]
			# Normalize whitespace in actual.
			actual = " ".join(actual.strip().split())
			msg = '{}: {}\nActual output: {}'.format(command, expected, actual)
			if command == 'assert_contains':
				x = None
				if len(args) > 1:
					x = args[1]
				if x is None:
					builtIn.should_contain(
						actual,
						expected,
						msg=msg
					)
				else:
					builtIn.should_contain_x_times(
						actual,
						expected,
						x,
						msg=msg
					)
			elif command == 'assert_role':
				# Normalize ARIA role to NVDA's spoken output for the role.
				expected = NvdaSpeechMappings.role(expected)
				builtIn.should_contain_x_times(
					actual,
					expected,
					1,
					msg=msg
				)
			elif command == 'assert_state_or_property':
				state_or_property = args[0]
				expected = args[1]
				if state_or_property == 'aria-checked':
					possible_checked = NvdaSpeechMappings.state('aria-checked')
					actual_checked_true = possible_checked['true'] in actual
					actual_checked_mixed = possible_checked['mixed'] in actual
					actual_checked_false = possible_checked['false'] in actual
					result = False
					if expected == 'true':
						result = actual_checked_true and not actual_checked_mixed and not actual_checked_false
					elif expected == 'mixed':
						result = actual_checked_mixed and not actual_checked_false
					else:
						result = actual_checked_false and not actual_checked_mixed
				else:
					result = False
					msg = 'Unknown state or property in assert_state_or_property: {}'.format(command)
				builtIn.should_be_true(
					result,
					msg=msg
				)
			elif command == 'assert_equals':
				builtIn.should_be_equal_as_strings(
					actual,
					expected,
					msg=msg
				)
			else:
				builtIn.should_be_true(
					False,
					msg='Unknown aria_at assertion: {}'.format(command)
				)
		except AssertionError:
			builtIn.log(
				"repr of actual vs expected (ignore_case={}):\n{}\nvs\n{}".format(
					ignore_case,
					repr(actual),
					repr(expected)
				)
			)
			raise
