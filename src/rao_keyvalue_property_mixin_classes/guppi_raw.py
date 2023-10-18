from typing import Tuple

class GuppiRawProperties:
    """
    GUPPI RAW properties
    """

    blocksize: int = property(
        fget=lambda self: self.__get_item__("BLOCSIZE"),
        fset=lambda self, value: self.set("BLOCSIZE", value),
        doc="""Number of bytes in the data of the block.
            Critical to reading from a file.
        """
    )

    blockshape: Tuple[int, int, int, int] = property(
        fget=lambda self: (
            self.nof_antennas,
            self.observed_nof_channels//self.nof_antennas,
            self.blocksize//(
                self.observed_nof_channels
                * self.nof_polarizations
                * 2
                * self.nof_bits
            ),
            self.nof_polarizations
        ),
        fset=None,
        doc="""The 4 dimensional shape of the data within the block.
        Assumes complex data, of order:
        [slowest=Aspects, Channels, Spectra, Polarization=fastest]
        """
    )

    directio: bool = property(
        fget=lambda self: self.get("DIRECTIO", default=False),
        fset=lambda self, value: self.set("DIRECTIO", value),
        doc="""Whether or not the header is padded with bytes to align the
            start of the data of the block to a multiple of 512.
            Critical to reading from a file, but defaults to `False`.
            Used by rawspec when processing a file.
        """
    )

    observed_nof_channels: int = property(
        fget=lambda self: self.__get_item__("OBSNCHAN"),
        fset=lambda self, value: self.set("OBSNCHAN", value),
        doc="""Number of channels in the data of the block.
            Critical to rawspec processing a file.
        """
    )

    nof_polarizations: int = property(
        fget=lambda self: self.__get_item__("NPOL"),
        fset=lambda self, value: self.set("NPOL", value),
        doc="""Number of polarizations in the data of the block.
            Critical to rawspec processing a file.
        """
    )

    nof_bits: int = property(
        fget=lambda self: self.get("NBITS", 8),
        fset=lambda self, value: self.set("NBITS", value),
        doc="""Number of bits per sample in the data of the block.
            Critical to rawspec processing a file, but has a default.
        """
    )

    observed_frequency: float = property(
        fget=lambda self: self.__get_item__("OBSFREQ"),
        fset=lambda self, value: self.set("OBSFREQ", value),
        doc="""The center frequency of the data of the block.
            Critical to rawspec processing a file.
        """
    )

    observed_bandwidth: float = property(
        fget=lambda self: self.__get_item__("OBSBW"),
        fset=lambda self, value: self.set("OBSBW", value),
        doc="""The bandwidth covered by the data of the block.
            Critical to rawspec processing a file.
        """
    )

    channel_timespan: int = property(
        fget=lambda self: self.__get_item__("TBIN"),
        fset=lambda self, value: self.set("TBIN", value),
        doc="""Time span of each channel in the data of the block.
            Critical to rawspec processing a file.
        """
    )

    packet_index: int = property(
        fget=lambda self: self.__get_item__("PKTIDX"),
        fset=lambda self, value: self.set("PKTIDX", value),
        doc="""The first packet-index of the data of the block.
            Critical to rawspec processing a file.
        """
    )

    nof_antennas: int = property(
        fget=lambda self: self.get("NANTS", default=1),
        fset=lambda self, value: self.set("NANTS", value),
        doc="""The factor of antenna in OBSNCHAN.
            Used by rawspec when processing a file.
        """
    )

    rightascension_string: str = property(
        fget=lambda self: self.get("RA_STR", default="0.0"),
        fset=lambda self, value: self.set("RA_STR", value),
        doc="""The right-ascension coordinate the data of the block.
            Used by rawspec when processing a file.
        """
    )

    declination_string: str = property(
        fget=lambda self: self.get("DEC_STR", default="0.0"),
        fset=lambda self, value: self.set("DEC_STR", value),
        doc="""The declination coordinate the data of the block.
            Used by rawspec when processing a file.
        """
    )

    stt_mjd_day: int = property(
        fget=lambda self: self.get("STT_IMJD", default=51545),
        fset=lambda self, value: self.set("STT_IMJD", value),
        doc="""The MJD integer day of the first sample of the data of the block.
            Used by rawspec when processing a file.
        """
    )

    stt_mjd_seconds: float = property(
        fget=lambda self: self.get("STT_SMJD", default=0),
        fset=lambda self, value: self.set("STT_SMJD", value),
        doc="""The day-seconds of the first sample of the data of the block.
            Used by rawspec when processing a file.
        """
    )

    source_name: str = property(
        fget=lambda self: self.get("SRC_NAME", default="Unknown"),
        fset=lambda self, value: self.set("SRC_NAME", value),
        doc="""The observed target of the data of the block.
            Used by rawspec when processing a file.
        """
    )

    telescope: str = property(
        fget=lambda self: self.get("TELESCOP", default="Unknown"),
        fset=lambda self, value: self.set("TELESCOP", value),
        doc="""The telescope name or code from which the block was produced.
            Used by rawspec when processing a file.
        """
    )