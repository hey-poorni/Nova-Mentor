from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # Stubs for the linter: provide an entry for each module so the IDE sees them
    # without trying to resolve path-with-space absolute imports
    class _ModuleStub: ...
    
    bedrock_client: Any = _ModuleStub()
    analytics_service: Any = _ModuleStub()
    quiz_service: Any = _ModuleStub()
    socratic_service: Any = _ModuleStub()
    analyzer_service: Any = _ModuleStub()
    vector_store: Any = _ModuleStub()
    recommendation_service: Any = _ModuleStub()
else:
    # Real logic for runtime: use relative imports to avoid absolute path issues
    from . import (
        bedrock_client,
        analytics_service,
        quiz_service,
        socratic_service,
        analyzer_service,
        vector_store,
        recommendation_service
    )
