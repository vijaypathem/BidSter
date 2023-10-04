from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.


class Auction(models.Model):
    auction_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.auction_name

    def clean(self):
        now = timezone.now()

        if self.start_time >= self.end_time:
            raise ValidationError("the end time should be later than start time ")
        if now > self.start_time and now > self.end_time:
            raise ValidationError("action cannot be in the past")

    def save(self, *args, **kwargs):
        now = timezone.now()

        if self.start_time <= now <= self.end_time:
            self.status = "open"
        else:
            self.status = "closed"
            if not self.winner:
                highest_bid = self.bid_set.order_by("-bid_amount").first()
                if highest_bid:
                    self.winner = highest_bid.bidder
        super().save(*args, **kwargs)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Auction: {self.auction.auction_name}, Bidder: {self.bidder.username}"

    def save(self, *args, **kwargs):
        if self.bid_amount < self.auction.base_price:
            raise ValueError("Bid amount must be greater thab base price")
        super().save(*args, **kwargs)
