from datetime import datetime, date
import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from analytics.filters import BountiesTimelineFilter
from .serializers import BountiesTimelineSerializer, TimelineCategorySerializer
from .models import BountiesTimeline
from std_bounties.models import Category, RankedCategory


class TimelineBounties(APIView):
    def get(self, request):
        queryset = request.query_params.copy()
        since = queryset.get('since', '')
        until = queryset.get('until', datetime.now().date())
        schema = queryset.get('schema', 'all')

        try:
            since_date = datetime.strptime(since, "%Y-%m-%d").date()

            if type(until) is not date:
                until_date = datetime.strptime(until, "%Y-%m-%d").date()
            else:
                until_date = until

            if type(since_date) is date and type(until_date) is date:
                queryset['until'] = until_date
                queryset['since'] = since_date

                bounties_timeline = BountiesTimelineFilter(queryset,
                                                           BountiesTimeline.objects.all().order_by('date'),
                                                           request=request)


                serialized = BountiesTimelineSerializer(bounties_timeline.qs, many=True, context={'request': request})

                if schema == 'all':
                    ranked_category_list = RankedCategory.objects.distinct().values('normalized_name', 'name')
                    ranked_categories = dict(map(lambda x: (x['normalized_name'], x['name']), ranked_category_list))

                    gitcoinQuery = Category.objects.select_related('bounty').filter(
                        bounty__bounty_created__gte=since_date,
                        bounty__bounty_created__lte=until_date,
                        bounty__schemaName__exact='gitcoinBounty'
                    ).distinct().values('normalized_name').annotate(total=Count('bounty'))

                    standardQuery = Category.objects.select_related('bounty').filter(
                        bounty__bounty_created__gte=since_date,
                        bounty__bounty_created__lte=until_date,
                        bounty__schemaName__exact='standardSchema'
                    ).distinct().values('normalized_name').annotate(total=Count('bounty'))

                    queryset = gitcoinQuery | standardQuery
                    categories = TimelineCategorySerializer(queryset, many=True, context={'ranked_categories': ranked_categories})

                else:
                    ranked_category_list = RankedCategory.objects.distinct().values('normalized_name', 'name')
                    ranked_categories = dict(map(lambda x: (x['normalized_name'], x['name']), ranked_category_list))
                    queryset = Category.objects.select_related('bounty').filter(
                        bounty__bounty_created__gte=since_date,
                        bounty__bounty_created__lte=until_date,
                        bounty__schemaName__exact=schema
                    ).distinct().values('normalized_name').annotate(total=Count('bounty'))
                    categories = TimelineCategorySerializer(queryset, many=True, context={'ranked_categories': ranked_categories})

                data = {
                    'timeline': serialized.data,
                    'categories': categories.data
                }

                return Response(data)

        except ValueError:
            pass

        res = {"error": 400, "message": "The fields since & until needs being formated as YYYY-MM-DD"}
        return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)
