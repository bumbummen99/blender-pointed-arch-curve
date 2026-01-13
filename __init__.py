# Blender Pointed Arch Curve add-on
# Contributor(s): Patrick Henninger (privat@skyraptor.eu)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
bl_info = {
    "name": "Pointed Arch Curve",
    "description": "Adds a \"pointed arch\" (gothic style) curve with customizable parameters",
    "author": "Patrick Henninger",
    "version": (1, 0),
    "blender": (5, 0, 1),
    "location": "Add > Curve",
    "category": "Add Curve",
}

import bpy

#
# Add additional functions here
#

def register():
    from . import pointedarch
    properties.register()

def unregister():
    from . import pointedarch
    pointedarch.unregister()

if __name__ == '__main__':
    register()
