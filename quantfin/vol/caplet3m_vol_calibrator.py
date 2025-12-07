from quantfin.vol.vol_calibrator import VolCalibrator


class Caplet3MVolCalibrator:
    """VolCalibrator class for 3m Caplets"""

    def __init__(self, caplets, ibor_curve):
        self.caplets = caplets
        self.ibor_curve = ibor_curve

    def extract_vol_data(self):
        # Extract data from caplets into a form we can pass into the base VolCalibrator
        expiries = []
        strikes = []
        market_vols = []
        forwards = []

        for cap in self.caplets:
            expiries.append(cap.expiry)
            strikes.append(cap.strike)
            market_vols.append(cap.market_vol)
            forwards.append(cap.forward_rate(self.ibor_curve))

        return expiries, strikes, market_vols, forwards

    def calibrate(self, engine="scipy"):
        expiries, strikes, market_vols, forwards = self.extract_vol_data()

        base_calibrator = VolCalibrator(expiries, strikes, market_vols, forwards)

        return base_calibrator.calibrate(engine=engine)