from django.contrib import admin
from django.conf import settings
from studlan.lottery.models import Lottery, LotteryTranslation

class LotteryTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    model = LotteryTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1

class LotteryAdmin(admin.ModelAdmin):
    inlines = [LotteryTranslationInlineAdmin,]

admin.site.register(Lottery, LotteryAdmin)
