from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "products" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "price" INT,
    "description" TEXT,
    "brand" VARCHAR(255),
    "url" VARCHAR(512),
    "image" VARCHAR(512),
    "provider" VARCHAR(10) NOT NULL
);
COMMENT ON COLUMN "products"."provider" IS 'INTERSPORT: Intersport\nXXL: XXL\nUNKNOWN: Unknown';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "products";"""
