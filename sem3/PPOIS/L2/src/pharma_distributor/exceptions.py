class PharmaDistributorError(Exception):
    """Base class for all errors in  PharmaDistributor."""

    pass


class FinanceError(PharmaDistributorError):
    pass


class CatalogError(PharmaDistributorError):
    pass


class ConversionError(PharmaDistributorError):
    pass


class CategoryError(CatalogError):
    pass

