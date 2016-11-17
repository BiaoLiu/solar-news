from django.db import models

ARTICLE_URL = 'http://wallstreetcn.com/node/{0}'


# Create your models here.

# class BaseModel(models.Model):
#     id = models.IntegerField(primary_key=True)
#     createtime = models.DateTimeField()
#     updatetime = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500, null=True)
    content = models.TextField(null=True)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)

    # songs = db.ListField(db.ReferenceField('Song'))

    # class Meta(BaseModel.Meta):
    #     index_together = ['name']

    @property
    def url(self):
        return ARTICLE_URL.format(self.id)


class Process(models.Model):
    id = models.IntegerField(primary_key=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    @property
    def is_success(self):
        return self.status == 1

    def make_succeed(self):
        return self.objects.update(status=1)

    def make_fail(self):
        return self.objects.update(status=2)
