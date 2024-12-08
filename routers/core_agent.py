from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from agents.core.CoreAgent import CoreAgent
from api_key.validation import verify_api_key

router = APIRouter(
    prefix="/core-agent",
    tags=["core-agent"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/trigger")
async def trigger_core_agent():
    """
    Manually trigger the CoreAgent to process all users.
    This endpoint is protected by API key authentication.
    """
    try:
        core_agent = CoreAgent()
        await core_agent.process_all_users()
        return JSONResponse(
            content={"message": "CoreAgent processing completed successfully"},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to process users: {str(e)}"},
            status_code=500
        ) 