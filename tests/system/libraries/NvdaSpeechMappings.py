# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides mappings from ARIA roles and states to NVDA's expected speech output,
for ARIA-AT tests.
"""


class NvdaSpeechMappings:
    @staticmethod
    def role(role):
        return {
            "checkbox": "check box"
        }[role]

    @staticmethod
    def state(state):
        return {
            "aria-checked": {
                "false": "not checked",
                "mixed": "half checked",
                "true": "checked"
            }
        }[state]
