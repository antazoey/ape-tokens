from typing import Any

import click


def token_option(*param_decls: str, **kwargs: Any):
    """
    Click option that resolves a token symbol (or address) to a ``TokenInstance``.

    Defaults to ``--token`` when no parameter declarations are given. The default
    callback looks the value up via ``ape_tokens.tokens[value]``; pass ``callback=``
    to override. ``None`` values pass through unchanged so the option can be optional.

    Usage example::

        @click.command()
        @token_option("--asset-in")
        @token_option("--asset-out")
        def swap(asset_in, asset_out):
            ...
    """
    if not param_decls:
        param_decls = ("--token",)

    kwargs.setdefault("help", "A token symbol or address")
    kwargs.setdefault("metavar", "TOKEN")

    if "callback" not in kwargs:

        def _resolve_token(_ctx, param, value):
            if value is None:
                return None

            from ape.exceptions import ConversionError

            from ape_tokens import tokens

            try:
                return tokens[value]
            except (KeyError, ConversionError) as err:
                raise click.BadParameter(str(err), param=param) from err

        kwargs["callback"] = _resolve_token

    return click.option(*param_decls, **kwargs)
