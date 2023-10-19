from typing import Tuple

def factor_division(dividend, divisor):
    if dividend % divisor != 0:
        raise ValueError(f"Cannot cleanly divide {dividend} by non-factor {divisor}.")
    return dividend // divisor


class GuppiRawProperties:
    """
    GUPPI RAW properties
    """

    blocksize: int = property(
        fget=lambda self: self.__getitem__("BLOCSIZE"),
        fset=lambda self, value: self.__setitem__("BLOCSIZE", value),
        doc="""Number of bytes in the data of the block.
            Critical to reading from a file.
        """
    )

    blockshape: Tuple[int, int, int, int] = property(
        fget=lambda self: (
            self.nof_antennas,
            factor_division(self.observed_nof_channels, self.nof_antennas),
            factor_division(
                self.blocksize*8,
                (
                    self.observed_nof_channels
                    * self.nof_polarizations
                    * 2
                    * self.nof_bits
                )
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
        fget=lambda self: self.get("DIRECTIO", False),
        fset=lambda self, value: self.__setitem__("DIRECTIO", value),
        doc="""Whether or not the header is padded with bytes to align the
            start of the data of the block to a multiple of 512.
            Critical to reading from a file, but defaults to `False`.
            Used by rawspec when processing a file.
        """
    )

    observed_nof_channels: int = property(
        fget=lambda self: self.__getitem__("OBSNCHAN"),
        fset=lambda self, value: self.__setitem__("OBSNCHAN", value),
        doc="""Number of channels in the data of the block.
            Critical to rawspec processing a file.
        """
    )

    nof_polarizations: int = property(
        fget=lambda self: self.__getitem__("NPOL"),
        fset=lambda self, value: self.__setitem__("NPOL", value),
        doc="""Number of polarizations in the data of the block.
            Critical to rawspec processing a file.
        """
    )

    nof_bits: int = property(
        fget=lambda self: self.get("NBITS", 8),
        fset=lambda self, value: self.__setitem__("NBITS", value),
        doc="""Number of bits per sample in the data of the block.
            Critical to rawspec processing a file, but has a default.
        """
    )

    observed_frequency: float = property(
        fget=lambda self: self.__getitem__("OBSFREQ"),
        fset=lambda self, value: self.__setitem__("OBSFREQ", value),
        doc="""The center frequency of the data of the block.
            Critical to rawspec processing a file.
        """
    )

    observed_bandwidth: float = property(
        fget=lambda self: self.__getitem__("OBSBW"),
        fset=lambda self, value: self.__setitem__("OBSBW", value),
        doc="""The bandwidth covered by the data of the block.
            Critical to rawspec processing a file.
        """
    )

    channel_timespan: int = property(
        fget=lambda self: self.__getitem__("TBIN"),
        fset=lambda self, value: self.__setitem__("TBIN", value),
        doc="""Time span of each channel in the data of the block.
            Critical to rawspec processing a file.
        """
    )

    packet_index: int = property(
        fget=lambda self: self.__getitem__("PKTIDX"),
        fset=lambda self, value: self.__setitem__("PKTIDX", value),
        doc="""The first packet-index of the data of the block.
            Critical to rawspec processing a file.
        """
    )

    nof_antennas: int = property(
        fget=lambda self: self.get("NANTS", 1),
        fset=lambda self, value: self.__setitem__("NANTS", value),
        doc="""The factor of antenna in OBSNCHAN.
            Used by rawspec when processing a file.
        """
    )

    rightascension_string: str = property(
        fget=lambda self: self.get("RA_STR", "0.0"),
        fset=lambda self, value: self.__setitem__("RA_STR", value),
        doc="""The right-ascension coordinate the data of the block.
            Used by rawspec when processing a file.
        """
    )

    declination_string: str = property(
        fget=lambda self: self.get("DEC_STR", "0.0"),
        fset=lambda self, value: self.__setitem__("DEC_STR", value),
        doc="""The declination coordinate the data of the block.
            Used by rawspec when processing a file.
        """
    )

    stt_mjd_day: int = property(
        fget=lambda self: self.get("STT_IMJD", 51545),
        fset=lambda self, value: self.__setitem__("STT_IMJD", value),
        doc="""The MJD integer day of the first sample of the data of the block.
            Used by rawspec when processing a file.
        """
    )

    stt_mjd_seconds: float = property(
        fget=lambda self: self.get("STT_SMJD", 0),
        fset=lambda self, value: self.__setitem__("STT_SMJD", value),
        doc="""The day-seconds of the first sample of the data of the block.
            Used by rawspec when processing a file.
        """
    )

    source_name: str = property(
        fget=lambda self: self.get("SRC_NAME", "Unknown"),
        fset=lambda self, value: self.__setitem__("SRC_NAME", value),
        doc="""The observed target of the data of the block.
            Used by rawspec when processing a file.
        """
    )

    telescope: str = property(
        fget=lambda self={}: self.get("TELESCOP", "Unknown"),
        fset=lambda self, value: self.__setitem__("TELESCOP", value),
        doc="""The telescope name or code from which the block was produced.
            Used by rawspec when processing a file.
        """
    )