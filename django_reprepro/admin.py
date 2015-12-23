# -*- coding: utf-8 -*-
#
# This file is part of django-reprepro (https://github.com/mathiasertl/django-reprepro).
#
# django-reprepro is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# django-reprepro is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-reprepro.  If
# not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from django.contrib import admin

from .models import Component
from .models import Distribution
from .models import IncomingDirectory
from .models import Package
from .models import PackageUpload

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'last_seen', )
    list_filter = ('enabled', )
    ordering = ('name', )
    readonly_fields = ('last_seen', )


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'last_seen', )
    list_filter= ('vendor', )
    ordering = ('name', )
    readonly_fields = ('last_seen', )


class PackageUploadInline(admin.TabularInline):
    model = PackageUpload
    fields = ('timestamp', 'version', 'dist', 'arch', 'components')
    readonly_fields = ('timestamp', 'version', 'dist', 'arch', 'components')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj):
        return False


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [
        PackageUploadInline,
    ]
    list_display = ('name', 'components_list', 'last_seen', )
    list_filter = ('all_components', 'components', )
    ordering = ('name', )
    readonly_fields = ('last_seen', )
    search_fields = ('name', )

    def components_list(self, obj):
        return ', '.join(obj.components.all().order_by('name').values_list('name', flat=True))


@admin.register(IncomingDirectory)
class IncomingDirectoryAdmin(admin.ModelAdmin):
    list_display = ('location', 'enabled')