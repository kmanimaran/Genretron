import numpy
from two_dimensional_feature import TwoDimensionalFeature

__authors__ = "Carmine Paolino"
__copyright__ = "Copyright 2015, Vrije Universiteit Amsterdam"
__credits__ = ["Carmine Paolino"]
__license__ = "3-clause BSD"
__email__ = "carmine@paolino.me"


class Spectrogram(TwoDimensionalFeature):
    default_fft_resolution = 1024

    @staticmethod
    def bins(fft_resolution=None):
        fft_resolution = fft_resolution or Spectrogram.default_fft_resolution
        return (fft_resolution / 2) + 1

    def __init__(self, spectrogram, window_size, step_size, window_type,
                 fft_resolution, wins, bins, nframes):
        super(Spectrogram, self).__init__(
            spectrogram,
            window_size,
            step_size,
            window_type,
            wins,
            bins
        )
        self.fft_resolution = fft_resolution
        self.nframes = nframes

    def to_signal(self):
        import scipy
        signal = numpy.zeros(self.nframes)
        for i, n in enumerate(self.wins):
            print(i,n,self.data.T.shape)
            signal[i*self.bins:(i+1)*self.bins] = scipy.real(scipy.ifft(self.data[i]))

        # for n, i in enumerate(range(0, int(self.nframes - len(self.wins)), int(self.step_size))):
        #     data = scipy.real(scipy.ifft(self.data[n]))
        #     signal[i:i+len(self.wins)] += data
        return signal

    @classmethod
    def from_waveform(cls, frames,
                      window_size=TwoDimensionalFeature.default_window_size,
                      step_size=None,
                      window_type=TwoDimensionalFeature.default_window_type,
                      fft_resolution=default_fft_resolution):
        step_size = window_size / 2 if step_size is None else step_size
        window = cls.window_types[window_type](window_size)

        wins = cls.wins(len(frames), window_size, step_size)
        bins = cls.bins(fft_resolution)

        spectrogram = numpy.zeros(cls.shape(wins, bins))

        for i, n in enumerate(wins):
            xseg = frames[n - window_size:n]
            z = numpy.fft.fft(window * xseg, fft_resolution)
            # adding a small quantity fixes log(0) problem
            spectrogram[i, :] = numpy.log(numpy.abs(z[:bins] + 1e-8))

        return cls(spectrogram, window_size, step_size, window_type,
                   fft_resolution, wins, bins, len(frames))
