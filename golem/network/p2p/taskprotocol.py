from devp2p.protocol import BaseProtocol
from rlp import sedes

from golem.core.simpleserializer import CBORSedes


class TaskProtocol(BaseProtocol):

    protocol_id = 18318  # == GolemProtocol.protocol_id + 1
    name = b'task_proto'

    def __init__(self, peer, service):
        # required by P2PProtocol
        self.config = peer.config
        self.eth_account_info = None
        BaseProtocol.__init__(self, peer, service)

    class reject(BaseProtocol.command):
        """
        Generic reject message,
        sent by both requestors and providers
        """
        cmd_id = 0

        structure = [
            ('cmd_id', sedes.big_endian_int),
            ('reason', CBORSedes),
            ('payload', CBORSedes)
        ]

    class task_request(BaseProtocol.command):
        """
        ComputeTaskDef request,
        sent by providers
        """
        cmd_id = 1

        structure = [
            ('task_id', sedes.binary),
            ('performance', CBORSedes),
            ('price', sedes.big_endian_int),
            ('max_disk', sedes.big_endian_int),
            ('max_memory', sedes.big_endian_int),
            ('max_cpus', sedes.big_endian_int)
        ]

    class task(BaseProtocol.command):
        """
        ComputeTaskDef and resources,
        sent by requestors
        """
        cmd_id = 2

        structure = [
            ('definition', CBORSedes),
            ('resources', CBORSedes),
            ('resource_options', CBORSedes)
        ]

    class failure(BaseProtocol.command):
        """
        Computation failure,
        sent by providers
        """
        cmd_id = 3
        structure = [
            ('subtask_id', sedes.binary),
            ('reason', sedes.binary)
        ]

    class result(BaseProtocol.command):
        """
        Task computation result,
        sent by providers
        """
        cmd_id = 4

        structure = [
            ('subtask_id', sedes.binary),
            ('computation_time', sedes.big_endian_int),
            ('resource_hash', sedes.binary),
            ('resource_secret', sedes.binary),
            ('resource_options', CBORSedes),
            ('eth_account', sedes.binary)
        ]

    class accept_result(BaseProtocol.command):
        """
        Accept task computation result,
        sent by requestors
        """
        cmd_id = 5

        structure = [
            ('subtask_id', sedes.binary),
            ('remuneration', sedes.big_endian_int)
        ]

    class payment_request(BaseProtocol.command):
        """
        Payment information request,
        sent by providers
        """
        cmd_id = 6

        structure = [
            ('subtask_id', sedes.binary),
        ]

    class payment(BaseProtocol.command):
        """
        Payment information,
        sent by requestors
        """
        cmd_id = 7

        structure = [
            ('subtask_id', sedes.binary),
            ('transaction_id', sedes.binary),
            ('remuneration', sedes.big_endian_int),
            ('block_number', sedes.binary)
        ]