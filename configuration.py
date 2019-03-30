#!/usr/bin/env python3
# ~/S/g/g/Pfingstrose
# Copyright(C) 2019 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Configuration of ~/S/g/g/Pfingstrose."""

import os


class Configuration:
    """Configuration of ~/S/g/g/Pfingstrose."""

    CONSUMER_KEY = os.getenv("PFINGSTROSE_CONSUMER_KEY", "")
    CONSUMER_SECRET = os.getenv("PFINGSTROSE_CONSUMER_SECRET", "")
    ACCESS_TOKEN = os.getenv("PFINGSTROSE_ACCESS_TOKEN", "")
    ACCESS_TOKEN_SECRET = os.getenv("PFINGSTROSE_ACCESS_TOKEN_SECRET", "")
