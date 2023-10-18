import os
from datetime import datetime, timedelta

from .guppi_raw import GuppiRawProperties


class HpdaqProperties(GuppiRawProperties):
    """
    The hashpipe implementations known informally as hpguppi_daq
    pass header-block data chunks between pipelined threads which
    conform to the FITS header style of GUPPI RAW (probably because
    that is a primary data product). The implemented pipelines output
    more than just GUPPI RAW files, but the critical keyed-values have
    been cemented in the common vocabulary of hpdaq properties.
    """

    data_directory: str = property(
        fget=lambda self: self.__get_item__("DATADIR"),
        fset=None,
        doc="""Initial directory in the output path of the hashpipe recorded product.
        """
    )

    project_id: str = property(
        fget=lambda self: self.get("PROJID", ".")[0:23],
        fset=lambda self, value: self.set("PROJID", value),
        doc="""Subdirectory in the output path of the hashpipe recorded product.
        The value is truncated to 24 characters when used.
        """
    )

    backend: str = property(
        fget=lambda self: self.get("BACKEND", ".")[0:23],
        fset=lambda self, value: self.set("BACKEND", value),
        doc="""Subdirectory in the output path of the hashpipe recorded product.
        The value is truncated to 24 characters when used.
        """
    )
    observation_output_directorypath: str = property(
        getter=lambda self: os.path.join(
            self.data_directory,
            self.project_id,
            self.backend
        ),
        fset=None
    )

    start_packet_index: int = property(
        fget=lambda self: self.__get_item__("PKTSTART"),
        fset=lambda self, value: self.set("PKTSTART", value),
        doc="""The first packet-index from which to pass through the pipeline.
        """
    )

    stop_packet_index: int = property(
        fget=lambda self: self.__get_item__("PKTSTOP"),
        fset=lambda self, value: self.set("PKTSTOP", value),
        doc="""The last packet-index from which to pass through the pipeline.
        """
    )

    packet_index_per_block: int = property(
        fget=lambda self: self.__get_item__("PIPERBLK"),
        fset=lambda self, value: self.set("PIPERBLK", value),
        doc="""The packet-index span of a block.
        """
    )

    pulse: datetime = property(
        fget=lambda self: datetime.strptime(
            self.get("DAQPULSE", "Thu Jan 01 00:00:00 1970"),
            "%a %b %d %H:%M:%S %Y"
        ),
        fset=None
    )

    is_alive: bool = property(
        fget=lambda self: abs(datetime.now() - self.pulse) < timedelta(seconds=2),
        fset=None
    )
