#!/usr/bin/env sh
exec uvicorn app:APP_OBJ\
    --workers $SNIPPET_WORKERS\
    --loop uvloop\
    --ws none\
    --interface asgi3
