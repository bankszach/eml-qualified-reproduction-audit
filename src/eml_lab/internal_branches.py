"""Diagnostic-only internal branch helpers.

These helpers model named principal branch behavior for staged reproduction
experiments. They are not replacements for derived EML witnesses and must not
be used as verified witness implementations.

The current use case is comparing named principal ``acosh`` behavior against
the derived EML ``arcosh`` witness inside the branch-sensitive ``arccos``
chain. Passing tests with these helpers explains staged branch behavior; it
does not prove pure EML closure or full dependency-chain substitution.
"""

from __future__ import annotations

import mpmath as mp


def principal_arcosh_internal(z: object):
    """Diagnostic principal acosh via the standard sqrt-factorized formula.

    This is diagnostic-only. It uses mpmath principal sqrt/log branches and is
    compared against ``mpmath.acosh`` in tests. It is not the derived EML
    ``arcosh`` witness and must not be counted as a verified replacement for
    that witness in dependency-chain or fully expanded EML reports.
    """

    z = mp.mpc(z)
    return mp.log(z + mp.sqrt(z - 1) * mp.sqrt(z + 1))
