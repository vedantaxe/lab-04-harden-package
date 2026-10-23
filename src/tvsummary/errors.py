"""Custom exceptions for the tvsummary package."""


class TVSummaryError(Exception):
    """Base exception for expected tvsummary errors."""


class ConfigurationError(TVSummaryError):
    """Raised when application configuration is invalid."""


class DataSourceError(TVSummaryError):
    """Raised when show records cannot be retrieved or decoded."""


class DataValidationError(TVSummaryError):
    """Raised when downloaded show records contain invalid data."""


class ReportError(TVSummaryError):
    """Raised when a summary report cannot be written."""
