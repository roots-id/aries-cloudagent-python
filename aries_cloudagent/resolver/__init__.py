"""Interfaces and base classes for DID Resolution."""

import logging

from ..config.injection_context import InjectionContext
from ..config.provider import ClassProvider

from .did_resolver_registry import DIDResolverRegistry

LOGGER = logging.getLogger(__name__)


async def setup(context: InjectionContext):
    """Set up default resolvers."""
    registry = context.inject_or(DIDResolverRegistry)
    if not registry:
        LOGGER.warning("No DID Resolver Registry instance found in context")
        return

    key_resolver = ClassProvider(
        "aries_cloudagent.resolver.default.key.KeyDIDResolver"
    ).provide(context.settings, context.injector)
    await key_resolver.setup(context)
    registry.register(key_resolver)

    if not context.settings.get("ledger.disabled"):
        indy_resolver = ClassProvider(
            "aries_cloudagent.resolver.default.indy.IndyDIDResolver"
        ).provide(context.settings, context.injector)
        await indy_resolver.setup(context)
        registry.register(indy_resolver)
    else:
        LOGGER.warning("Ledger is not configured, not loading IndyDIDResolver")

    web_resolver = ClassProvider(
        "aries_cloudagent.resolver.default.web.WebDIDResolver"
    ).provide(context.settings, context.injector)
    await web_resolver.setup(context)
    registry.register(web_resolver)
    
    ada_resolver = ClassProvider(
        "aries_cloudagent.resolver.default.sidetree-cardano.AdaDIDResolver"
    ).provide(context.settings, context.injector)
    await ada_resolver.setup(context)
    registry.register(ada_resolver)

    prism_resolver = ClassProvider(
        "aries_cloudagent.resolver.default.prism.PrismDIDResolver"
    ).provide(context.settings, context.injector)
    await prism_resolver.setup(context)
    registry.register(prism_resolver)
