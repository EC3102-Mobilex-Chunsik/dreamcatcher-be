from fastapi import APIRouter

# Configure API router
router = APIRouter(
    tags=['health'],
)


@router.get('/_health')
async def get_health():
    return {
        'status': 'Ok',
    }
