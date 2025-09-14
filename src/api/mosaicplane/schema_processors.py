"""
Schema processing hooks for drf-spectacular.

This module contains preprocessing hooks that modify the OpenAPI schema
before it's served to exclude internal or sensitive endpoints.
"""


def exclude_feature_flags(result, generator, request, public):
    """
    Preprocessing hook to exclude feature flag endpoints from API documentation.

    Feature flags are internal-only configuration and should not be exposed
    in the public API documentation.

    Args:
        result: The OpenAPI schema result
        generator: The schema generator instance
        request: The HTTP request object (if available)
        public: Boolean indicating if this is for public documentation

    Returns:
        Modified OpenAPI schema with feature flag endpoints removed
    """
    if not result or 'paths' not in result:
        return result

    # List of path patterns to exclude from documentation
    feature_flag_patterns = [
        '/v1/feature-flags',
        '/v1/feature-flags/',
        '/v1/feature-flags/detailed',
        '/v1/feature-flags/detailed/',
    ]

    # Remove feature flag endpoints from paths
    paths_to_remove = []
    for path in result['paths']:
        # Check for exact matches and pattern matches
        if any(path.startswith(pattern) or path == pattern for pattern in feature_flag_patterns):
            paths_to_remove.append(path)
        # Also remove individual feature flag detail endpoints (dynamic routes)
        elif path.startswith('/v1/feature-flags/') and path != '/v1/feature-flags/' and not path.endswith('/detailed/'):
            paths_to_remove.append(path)

    # Remove the identified paths
    for path in paths_to_remove:
        result['paths'].pop(path, None)

    return result