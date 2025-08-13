from fastapi import APIRouter
from ..schemas import ChatRequest, ChatResponse
from ..dispatcher.ai_dispatcher import dispatcher

router = APIRouter(prefix="/api")


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    result = await dispatcher.handle_message(req.message)
    return ChatResponse(action=result.get("action", "unknown"), data=result.get("data", {}))