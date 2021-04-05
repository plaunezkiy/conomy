from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models


class Wallet(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='wallets',
                              on_delete=models.CASCADE,
                              verbose_name='Владелец')
    name = models.CharField('Название', max_length=150)
    balance = models.FloatField('Баланс',
                                validators=[MinValueValidator(limit_value=0)])

    class Meta:
        verbose_name = 'Кошелёк'
        verbose_name_plural = 'Кошельки'

    def __str__(self):
        return f'{self.name}/{self.owner}'

    def can_send(self, amount):
        """
        Метод определяет, достаточно ли денег для перевода
        :param amount: сумма перевода
        :return: bool - достаточно ли средств для перевода
        """
        return (self.balance - amount) >= 0


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE,
                               verbose_name='От кого',
                               related_name='withdrawals')
    recipient = models.ForeignKey(Wallet, on_delete=models.CASCADE,
                                  verbose_name='Кому',
                                  related_name='topups')
    amount = models.FloatField('Сумма перевода', blank=True, null=True)
    comment = models.CharField('Комментарий', max_length=50)
    date = models.DateTimeField('Дата перевода', auto_now_add=True)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date']

    def __str__(self):
        return f'{self.amount} руб. ОТ {self.sender}' \
               f' ДЛЯ {self.recipient}'
