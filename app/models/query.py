from tortoise import fields, models


class Query(models.Model):
    id = fields.IntField(pk=True)
    query = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "queries"
