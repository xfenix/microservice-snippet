#!/usr/bin/env sh
exec uvicorn snippet_service.__main__:APP_OBJ\
    --workers $SNIPPET_WORKERS\
    --loop uvloop\
    --ws none\
    --interface asgi3
