#!/usr/bin/env python3
# Copyright 2021 lo
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import os
import logging
import subprocess

from charmhelpers.core import host

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class ConcourseCiCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        #self.framework.observe(self.on.httpbin_pebble_ready, self._on_httpbin_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.fortune_action, self._on_fortune_action)
        self.framework.observe(self.on.install, self._on_install)
        self._stored.set_default(things=[])


    def _on_install(self, event):
        #self.unit.status = MaintenanceStatus("Installing application packages")

        #config = hookenv.config()
        packages = ['curl', 'docker.io', 'docker-compose']

        for pkg in packages:
            os.environ["DEBIAN_FRONTEND"] = "noninteractive"
            cmd = ["apt-get", "install", "-y", pkg]
            subprocess.check_call(cmd, universal_newlines=True)

        file_to_units('files/concourse-ci.sh', '/usr/local/sbin/concourse-ci.sh')
        file_to_units('files/concourse-ci-systemd-config', '/lib/systemd/system/concourse-ci.service')
        host.service('enable', 'concourse-ci')

        self.unit.status = ActiveStatus()
    
    def _on_httpbin_pebble_ready(self, event):
        """Define and start a workload using the Pebble API.

        TEMPLATE-TODO: change this example to suit your needs.
        You'll need to specify the right entrypoint and environment
        configuration for your specific workload. Tip: you can see the
        standard entrypoint of an existing container using docker inspect

        Learn more about Pebble layers at https://github.com/canonical/pebble
        """
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        # Define an initial Pebble layer configuration
        pebble_layer = {
            "summary": "httpbin layer",
            "description": "pebble config layer for httpbin",
            "services": {
                "httpbin": {
                    "override": "replace",
                    "summary": "httpbin",
                    "command": "gunicorn -b 0.0.0.0:80 httpbin:app -k gevent",
                    "startup": "enabled",
                    "environment": {"thing": self.model.config["thing"]},
                }
            },
        }
        # Add intial Pebble config layer using the Pebble API
        container.add_layer("httpbin", pebble_layer, combine=True)
        # Autostart any services that were defined with startup: enabled
        container.autostart()
        # Learn more about statuses in the SDK docs:
        # https://juju.is/docs/sdk/constructs#heading--statuses

        self.unit.status = ActiveStatus()

    def _on_config_changed(self, _):
        """Just an example to show how to deal with changed configuration.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle config, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the config.py file.

        Learn more about config at https://juju.is/docs/sdk/config
        """
        current = self.config["thing"]
        if current not in self._stored.things:
            logger.debug("found a new thing: %r", current)
            self._stored.things.append(current)

        if host.service_running('concourse-ci'):
            host.service_restart('concourse-ci')
        else:
            host.service_start('concourse-ci')

    def _on_fortune_action(self, event):
        """Just an example to show how to receive actions.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle actions, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the actions.py file.

        Learn more about actions at https://juju.is/docs/sdk/actions
        """
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"fortune": "A bug in the code is worth two in the documentation."})

def file_to_units(local_path, unit_path, perms=None, owner='root', group='root'):
    """ copy a file from the charm onto our unit(s) """
    file_perms = perms
    if not perms:
        # Let's try manually work it out
        if local_path[-3:] == '.py' or local_path[-3:] == '.sh':
            file_perms = 0o755
        else:
            file_perms = 0o644

    with open(local_path, 'r') as fh:
        host.write_file(path=unit_path, content=fh.read().encode(), owner=owner, group=group, perms=file_perms)



if __name__ == "__main__":
    main(ConcourseCiCharm)
