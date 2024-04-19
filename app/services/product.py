



from uuid import UUID

from fastapi import HTTPException
from config.db_dependency import DBSessionDep
from repositories.product_repo import ProductRepository


class ProductService:

    def __init__(self,product_repository:ProductRepository) -> None:
        self.product_repository = product_repository


    async def get_product_by_id(self,product_id:UUID):
        """GET product by id"""
        product = await self.product_repository.get_product_by_id(product_id)
        return product
    
    

async def get_product_service(db:DBSessionDep)->ProductService:
    try:
        product_repository = ProductRepository(db)
        return ProductService(product_repository)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create UserService: {str(e)}")