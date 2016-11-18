from django.db import models

ARTICLE_URL = 'http://wallstreetcn.com/node/{0}'


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500, null=True)
    author = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    tag = models.CharField(max_length=20, null=True)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField(auto_now=True)

    # class Meta(BaseModel.Meta):
    #     index_together = ['name']

    @property
    def url(self):
        return ARTICLE_URL.format(self.id)


class Process(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.IntegerField(default=0)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    STATUS = PENDING, SUCCEEDED, FAILED = range(3)

    @property
    def is_success(self):
        return self.status == 1

    def make_status(self, is_success):
        status = 1 if is_success else 2
        return Process.objects.filter(id=self.id).update(status=status)

    def make_succeed(self):
        return Process.objects.filter(id=self.id).update(status=1)

    def make_fail(self):
        return Process.objects.filter(id=self.id).update(status=2)
