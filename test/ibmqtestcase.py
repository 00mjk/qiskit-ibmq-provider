# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Custom TestCase for IBMQProvider."""

import os
import logging
import inspect

from qiskit.test.base import BaseQiskitTestCase

from qiskit.providers.ibmq import IBMQ_PROVIDER_LOGGER_NAME
from qiskit.providers.ibmq.exceptions import IBMQAccountCredentialsNotFound

from .utils import setup_test_logging


class IBMQTestCase(BaseQiskitTestCase):
    """Custom TestCase for use with the IBMQProvider."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.log = logging.getLogger(cls.__name__)
        filename = '%s.log' % os.path.splitext(inspect.getfile(cls))[0]
        setup_test_logging(cls.log, filename)
        cls._set_logging_level(logging.getLogger(IBMQ_PROVIDER_LOGGER_NAME))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        from qiskit.providers.ibmq import IBMQ
        try:
            IBMQ.disable_account()
        except IBMQAccountCredentialsNotFound:
            pass

    @classmethod
    def simple_job_callback(cls, job_id, job_status, job, **kwargs):
        """A callback function that logs current job status."""
        # pylint: disable=unused-argument
        queue_info = kwargs.get('queue_info', 'unknown')
        cls.log.info("Job %s status is %s, queue_info is %s", job_id, job_status, queue_info)

    @classmethod
    def _set_logging_level(cls, logger: logging.Logger) -> None:
        """Set logging level for the input logger.

        Args:
            logger: Logger whose level is to be set.
        """
        if logger.level is logging.NOTSET:
            try:
                logger.setLevel(cls.log.level)
            except Exception as ex:  # pylint: disable=broad-except
                logger.warning(
                    'Error while trying to set the level for the "%s" logger to %s. %s.',
                    logger, os.getenv('LOG_LEVEL'), str(ex))
        if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
            logger.addHandler(logging.StreamHandler())
            logger.propagate = False
