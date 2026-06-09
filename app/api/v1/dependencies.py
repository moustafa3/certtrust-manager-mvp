from typing import Annotated

from fastapi import Depends

from app.core.security import verify_api_key

ApiKeyAuth = Annotated[None, Depends(verify_api_key)]