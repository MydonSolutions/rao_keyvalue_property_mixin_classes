from typing import Tuple


class GuppiRawProperties:
    """
    GUPPI RAW properties
    """

    @staticmethod
    def factor_division(dividend, divisor):
        if dividend % divisor != 0:
            raise ValueError(
                f"Cannot cleanly divide {dividend} by non-factor {divisor}."
            )
        return dividend // divisor

    @staticmethod
    def from_sexagesimal_str(value, str_delimiter=':', unit_base=60) -> float:
        if isinstance(value, str):
            units_factor = 1
            value_f = 0
            for part in value.split(str_delimiter):
                value_f += float(part)/units_factor
                if units_factor == 1:
                    units_factor *= -1 if value_f < 0 else 1
                units_factor *= unit_base

            return value_f
        return float(value)

    @staticmethod
    def to_sexagesimal_str(value, str_delimiter=':', unit_base=60) -> str:
        if isinstance(value, str):
            return value

        value_parts = [
            str(int(value)),
            str(abs(int((value-int(value))*unit_base))),
            f"{abs((value*60-int(value*60))*unit_base):0.16f}"
        ]

        return str_delimiter.join(value_parts)

    blocksize: int = property(
        fget=lambda self: self.__getitem__("BLOCSIZE"),
        fset=lambda self, value: self.__setitem__("BLOCSIZE", value),
        doc="""Number of bytes in the block-data.
        Critical to reading from a file.
        """
    )

    nof_spectra_per_block: int = property(
        fget=lambda self: GuppiRawProperties.factor_division(
            self.blocksize*8,
            (
                self.observed_nof_channels
                * self.nof_polarizations
                * 2
                * self.nof_bits
            )
        ),
        fset=None,
        doc="""The number of spectra in the block-data.
        """
    )

    blockshape: Tuple[int, int, int, int] = property(
        fget=lambda self: (
            self.nof_antennas,
            self.observed_nof_antenna_channels,
            self.nof_spectra_per_block,
            self.nof_polarizations
        ),
        fset=None,
        doc="""The 4 dimensional shape of the block-data.
        Assumes complex data, of order:
        [slowest=Aspects, Channels, Spectra, Polarization=fastest]
        """
    )

    directio: bool = property(
        fget=lambda self: self.get("DIRECTIO", False),
        fset=lambda self, value: self.__setitem__("DIRECTIO", value),
        doc="""Whether or not the header is padded with bytes to align the
        start of the block-data to a multiple of 512.
        Critical to reading from a file, but defaults to `False`.
        Used by rawspec when processing a file.
        """
    )

    observed_nof_channels: int = property(
        fget=lambda self: self.__getitem__("OBSNCHAN"),
        fset=lambda self, value: self.__setitem__("OBSNCHAN", value),
        doc="""Number of channels in the block-data.
        Critical to rawspec processing a file.
        """
    )

    observed_nof_antenna_channels: int = property(
        fget=lambda self: GuppiRawProperties.factor_division(
            self.observed_nof_channels,
            self.nof_antennas
        ),
        fset=None,
        doc="""Number of channels per antenna in the block-data.
        A shorthand proxy for `observed_nof_channels//nof_antennas`.
        """
    )

    nof_polarizations: int = property(
        fget=lambda self: self.__getitem__("NPOL"),
        fset=lambda self, value: self.__setitem__("NPOL", value),
        doc="""Number of polarizations in the block-data.
        Critical to rawspec processing a file.
        """
    )

    nof_bits: int = property(
        fget=lambda self: self.get("NBITS", 8),
        fset=lambda self, value: self.__setitem__("NBITS", value),
        doc="""Number of bits per sample in the block-data.
        Critical to rawspec processing a file, but has a default.
        """
    )

    observed_frequency: float = property(
        fget=lambda self: self.__getitem__("OBSFREQ"),
        fset=lambda self, value: self.__setitem__("OBSFREQ", value),
        doc="""The center frequency of the block-data.
        Critical to rawspec processing a file.
        """
    )

    observed_bandwidth: float = property(
        fget=lambda self: self.__getitem__("OBSBW"),
        fset=lambda self, value: self.__setitem__("OBSBW", value),
        doc="""The bandwidth covered by the block-data.
        Critical to rawspec processing a file.
        """
    )

    channel_bandwidth: float = property(
        fget=lambda self: (
            self.observed_bandwidth/self.observed_nof_antenna_channels
        ),
        fset=lambda self, value: self.__class__.observed_bandwidth.fset(
            self,
            self.observed_nof_antenna_channels*value
        ),
        doc="""The bandwidth covered by each channel in the block-data.
        """
    )

    spectra_timespan: int = property(
        fget=lambda self: self.__getitem__("TBIN"),
        fset=lambda self, value: self.__setitem__("TBIN", value),
        doc="""Timespan of each spectrum in the block-data.
        Critical to rawspec processing a file.
        """
    )

    packet_index: int = property(
        fget=lambda self: self.__getitem__("PKTIDX"),
        fset=lambda self, value: self.__setitem__("PKTIDX", value),
        doc="""The first packet-index of the block-data.
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
        doc="""The right-ascension coordinate (hours) of the telescope for the
        block-data.
        Used by rawspec when processing a file.
        """
    )

    rightascension_hours: float = property(
        fget=lambda self: GuppiRawProperties.from_sexagesimal_str(
            self.rightascension_string
        ),
        fset=lambda self, value: self.__class__.rightascension_string.fset(
            self,
            GuppiRawProperties.to_sexagesimal_str(value)
        ),
        doc="""The right-ascension coordinate of the telescope for the block-data.
        """
    )

    declination_string: str = property(
        fget=lambda self: self.get("DEC_STR", "0.0"),
        fset=lambda self, value: self.__setitem__("DEC_STR", value),
        doc="""The declination coordinate (degrees) of the telescope for the
        block-data.
        Used by rawspec when processing a file.
        """
    )

    declination_degrees: float = property(
        fget=lambda self: GuppiRawProperties.from_sexagesimal_str(
            self.declination_string
        ),
        fset=lambda self, value: self.__class__.declination_string.fset(
            self,
            GuppiRawProperties.to_sexagesimal_str(value)
        ),
        doc="""The declination coordinate of the telescope for the block-data.
        """
    )

    stt_mjd_day: int = property(
        fget=lambda self: self.get("STT_IMJD", 51545),
        fset=lambda self, value: self.__setitem__("STT_IMJD", value),
        doc="""The MJD integer day of the first sample of the block-data.
        Used by rawspec when processing a file.
        """
    )

    stt_mjd_seconds: float = property(
        fget=lambda self: self.get("STT_SMJD", 0),
        fset=lambda self, value: self.__setitem__("STT_SMJD", value),
        doc="""The day-seconds of the first sample of the block-data.
        Used by rawspec when processing a file.
        """
    )

    source_name: str = property(
        fget=lambda self: self.get("SRC_NAME", "Unknown"),
        fset=lambda self, value: self.__setitem__("SRC_NAME", value),
        doc="""The observed target of the block-data.
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

    observed_channels_offset: int = property(
        fget=lambda self: self.get("SCHAN", 0),
        fset=lambda self, value: self.__setitem__("SCHAN", value),
        doc="""The total-obvservation relative-offset of the first channel observed
        within the GUPPI data.
        Very common across radio-observatories.
        """
    )

    nof_packet_indices_per_block: int = property(
        fget=lambda self: self.get("PIPERBLK", self.nof_spectra_per_block),
        fset=lambda self, value: self.__setitem__("PIPERBLK", value),
        doc="""The number of packet-indices a block spans.
        Very common across radio-observatories. Used when calculating the
        unix-time of a packet index.
        """
    )

    time_unix_offset: int = property(
        fget=lambda self: self.get("SYNCTIME", 0),
        fset=lambda self, value: self.__setitem__("SYNCTIME", value),
        doc="""An integer-seconds offset to be used when calculating the unix-time
        of a packet index.
        Very common across radio-observatories.
        """
    )

    time_unix_epoch_seconds: float = property(
        fget=lambda self, packet_index_offset=0, spectra_index_offset=0: (
            self.time_unix_offset
            + (
                (
                    (self.packet_index + packet_index_offset)
                    / self.nof_packet_indices_per_block
                ) * self.self.nof_spectra_per_block
                + spectra_index_offset
            ) * self.spectra_timespan
        ),
        fset=None,
        doc="""The unix-epoch-seconds time of the first sample of the block."""
    )
