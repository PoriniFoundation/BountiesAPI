# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-09 11:06
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_user_wants_marketing_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='emails',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'activity': False, 'both': {'RatingReceived': True}, 'fulfiller': {'FulfillmentAcceptedFulfiller': True}, 'issuer': {'BountyCommentReceived': True, 'BountyCompleted': True, 'BountyExpired': True, 'ContributionReceived': True, 'FulfillmentSubmittedIssuer': True, 'FulfillmentUpdatedIssuer': True, 'TransferRecipient': True}}),
        ),
    ]
