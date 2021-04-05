from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Wallet, Transaction
from .permissions import IsOwner, IsAuthenticated
from .serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Переопределяем метод get_queryset, чтобы доступ был только к кошелькам пользователя
        :return: queryset кошельков пользователя
        """
        return self.request.user.wallets

    @action(methods=['get'], detail=True,
            permission_classes=[IsAuthenticated, IsOwner])
    def transactions(self, request, pk):
        """
        Дополнительный url-метод для получения
        траназакций одного кошелька

        Доступна фильтрация по тегу type
        ?type=topup - пополнение счёта
        ?type=withdrawal - снятие со счёта

        :param request: запрос
        :param pk: id кошелька, транзакции которого требуется получить
        :return: список JSON словарей с транзакциями данного кошелька
        """
        wallet = get_object_or_404(Wallet, owner=request.user, pk=pk)
        param = request.query_params.get('type')
        if param == 'topup':
            transactions = wallet.topups
        elif param == 'withdrawal':
            transactions = wallet.withdrawals
        else:
            query = Q(sender=wallet) | Q(recipient=wallet)
            transactions = Transaction.objects.filter(query)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Переопределяем метод get_queryset, чтобы доступ был только
        к транзакциям, связанным с кошельками пользователя

        Доступна фильтрация по тегу type
        ?type=topup - пополнение счёта
        ?type=withdrawal - снятие со счёта

        :return: список JSON словарей с транзакциями кошельков пользователя
        """
        param = self.request.query_params.get('type')
        if param == 'topup':
            query = Q(recipient__owner=self.request.user)
        elif param == 'withdrawal':
            query = Q(sender__owner=self.request.user)
        else:
            query = Q(sender__owner=self.request.user) | \
                    Q(recipient__owner=self.request.user)
        transactions = Transaction.objects.filter(query)
        return transactions

    def create(self, request, *args, **kwargs):
        """
        переопределяем метод create для проверки владения кошельком,
        достаточного баланса и ловушки на перевод в тот же кошелёк

        :return: ошибка или сохранённая транзакция
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = get_object_or_404(Wallet,
                                   pk=self.request.data['sender'],
                                   owner=self.request.user)
        recipient = serializer.validated_data['recipient']
        amount = serializer.validated_data['amount']

        if sender == recipient:
            return Response(
                {
                    'detail':
                        'You can\'t transfer money to the same wallet.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if sender.can_send(amount):
            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()
            return super(TransactionViewSet, self)\
                .create(request, *args, **kwargs)
        return Response(
            {
                'detail':
                    'You don\'t have enough money in your wallet.'
            },
            status=status.HTTP_403_FORBIDDEN
        )
