# Copyright (c) 2010-2011 Robin Jarry
# 
# This file is part of EVE Corporation Management.
# 
# EVE Corporation Management is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at your 
# option) any later version.
# 
# EVE Corporation Management is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along with 
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.
from django.db.models.aggregates import Count

__date__ = "2011 4 17"
__author__ = "diabeteman"

import json

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from ecm.core import utils
from ecm.view.decorators import check_user_access
from ecm.data.roles.models import Member, CharacterOwnership
from ecm.data.common.models import ColorThreshold
from ecm.view import extract_datatable_params, get_members

#------------------------------------------------------------------------------
@check_user_access()
def player_list(request):
    data = { 
        'colorThresholds' : ColorThreshold.as_json(),
    }
    return render_to_response("auth/player_list.html", data, RequestContext(request))

#------------------------------------------------------------------------------
USER_COLUMNS = ["username", "char_count", "group_count", "date_joined"]
@check_user_access()
def player_list_data(request):
    try:
        params = extract_datatable_params(request)
    except KeyError:
        return HttpResponseBadRequest()
    
    query = User.objects.filter(is_active=True)
    query = query.annotate(char_count=Count("characters"))
    query = query.filter(char_count__gt=0)
    query = query.exclude(username__in=[settings.CRON_USERNAME, settings.ADMIN_USERNAME])
    
    sort_by = USER_COLUMNS[params.column]
    # SQL hack for making a case insensitive sort
    if sort_by == "username":
        sort_col = "%s_nocase" % sort_by
        query = query.extra(select={sort_col : 'LOWER("%s")' % sort_by})
    else:
        sort_col = sort_by
        
    if not params.asc: sort_col = "-" + sort_col
    query = query.extra(order_by=[sort_col])
    
    if params.search:
        total_count = query.count()
        query = query.filter(username__icontains=params.search)
        filtered_count = query.count()
    else:
        total_count = filtered_count = query.count()
    
    query = query[params.first_id:params.last_id]
    player_list = []
    for player in query:
        player_list.append([
            '<a href="/players/%d" class="player">%s</a>' % (player.id, player.username),
            player.char_count,
            player.groups.count(),
            utils.print_time_min(player.date_joined)
        ])
    
    json_data = {
        "sEcho" : params.sEcho,
        "iTotalRecords" : total_count,
        "iTotalDisplayRecords" : filtered_count,
        "aaData" : player_list
    }
    
    return HttpResponse(json.dumps(json_data))

#------------------------------------------------------------------------------
@check_user_access()
def player_details(request, player_id):
    player = get_object_or_404(User, id=int(player_id))
    
    data = {
        'player': player,
        'colorThresholds' : ColorThreshold.as_json(),
        'directorAccessLvl' : Member.DIRECTOR_ACCESS_LVL
    }
    
    return render_to_response('auth/player_details.html', data, RequestContext(request))

#------------------------------------------------------------------------------
@check_user_access()
def player_details_data(request, player_id):
    try:
        params = extract_datatable_params(request)
    except KeyError:
        return HttpResponseBadRequest()

    player = get_object_or_404(User, id=int(player_id))
    owned = CharacterOwnership.objects.filter(owner=player)
    
    total_members,\
    filtered_members,\
    members = get_members(query=Member.objects.filter(ownership__in=owned),
                          first_id=params.first_id, 
                          last_id=params.last_id,
                          search_str=params.search,
                          sort_by=params.column, 
                          asc=params.asc)
    json_data = {
        "sEcho" : params.sEcho,
        "iTotalRecords" : total_members,
        "iTotalDisplayRecords" : filtered_members,
        "aaData" : members
    }
    
    return HttpResponse(json.dumps(json_data))
    