# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import uuid

from st2common import log as logging
from st2common.runners.base import ShellRunnerMixin
from st2common.runners.base import get_metadata as get_runner_metadata
from winrm_runner.winrm_base import WinRmBaseRunner

__all__ = [
    'WinRmPsScriptRunner',
    'get_runner',
    'get_metadata'
]

LOG = logging.getLogger(__name__)


class WinRmPsScriptRunner(WinRmBaseRunner, ShellRunnerMixin):

    def run(self, action_parameters):
        if not self.entry_point:
            raise ValueError('Missing entry_point action metadata attribute')

        # read in the script contents from the local file
        with open(self.entry_point, 'r') as script_file:
            ps_script = script_file.read()

        # extract script parameters specified in the action metadata file
        positional_args, named_args = self._get_script_args(action_parameters)
        named_args = self._transform_named_args(named_args)

        # build a string from all of the named and positional arguments
        # this will be our full parameter list when executing the script
        ps_params = self.create_ps_params_string(positional_args, named_args)

        # the following wraps the script (from the file) in a script block ( {} )
        # executes it, passing in the parameters built above
        # https://docs.microsoft.com/en-us/powershell/scripting/core-powershell/console/powershell.exe-command-line-help
        ps_script_and_params = "& {%s} %s" % (ps_script, ps_params)

        # execute
        return self.run_ps(ps_script_and_params)


def get_runner():
    return WinRmPsScriptRunner(str(uuid.uuid4()))


def get_metadata():
    return get_runner_metadata('winrm_ps_script_runner')
