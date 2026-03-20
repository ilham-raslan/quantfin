from quantfin.vol.vol_calibrator import VolCalibrator


class Swaption3MVolCalibrator:
    """VolCalibrator class for 3m Caplets"""

    def __init__(self, swaptions, ibor_curve, ois_curve):
        self.swaptions = swaptions
        self.ibor_curve = ibor_curve
        self.ois_curve = ois_curve

    def extract_vol_data(self):
        # Extract data from swaptions into a form we can pass into the base VolCalibrator
        expiries = []
        strikes = []
        market_vols = []
        forwards = []

        for swaption in self.swaptions:
            expiries.append(swaption.expiry)
            strikes.append(swaption.strike)
            market_vols.append(swaption.market_vol)
            forwards.append(swaption.forward_swap_rate(self.ois_curve, self.ibor_curve))

        return expiries, strikes, market_vols, forwards

    def calibrate(self, engine="scipy"):
        expiries, strikes, market_vols, forwards = self.extract_vol_data()

        base_calibrator = VolCalibrator(expiries, strikes, market_vols, forwards)

        return base_calibrator.calibrate(engine=engine)