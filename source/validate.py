
class Validate:

    """ Validate by price """
    @staticmethod
    def by_price_and_old_price(price: float, old_price: float) -> bool:
        # Price must have risen 0.03%
        if price > (old_price * 1.03):
            return True
        return False
