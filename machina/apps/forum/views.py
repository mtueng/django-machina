# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.db.models import get_model
from django.db.models import Q
from django.views.generic import ListView

# Local application / specific library imports
from machina.core.loading import get_class

Forum = get_model('forum', 'Forum')

PermissionHandler = get_class('permission.handler', 'PermissionHandler')
perm_handler = PermissionHandler()


class IndexView(ListView):
    template_name = 'forum/index.html'
    context_object_name = 'forums'

    def get_queryset(self):
        return perm_handler.forum_list_filter(
            Forum.objects.filter(
                # Category, top-level forums and links
                Q(parent__isnull=True, display_on_index=True) |
                # Sub-level categories, forums and links
                Q(parent__parent__isnull=True, display_on_index=True) |
                # Children of forums that have a category as parent
                Q(parent__parent__parent__isnull=True,
                    parent__parent__type=Forum.TYPE_CHOICES.forum_cat,
                    parent__type=Forum.TYPE_CHOICES.forum_post,
                    display_on_index=True)),
            self.request.user
        )
