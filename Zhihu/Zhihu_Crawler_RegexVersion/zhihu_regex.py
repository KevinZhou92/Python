#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def pattern_getter(pattername):
	if (pattername == 'USER_NAME') :
		return re.compile('<span class="ProfileHeader-name">(.*?)</span>')

	if (pattername == 'PHOTO') :
		return re.compile('<img class="Avatar Avatar--large UserAvatar-inner" style="width:160px;height:160px;" src="(.*?)" srcset="(.*?)"/>')

	if (pattername == 'GENDER') :
		return re.compile('<div class="ProfileHeader-iconWrapper"><svg width="(.*?)" height="(.*?)" viewBox="(.*?)" class="(.*?)"')

	if (pattername == 'EDUCATION') :
		return re.compile('Icon Icon--education"(.*?)</svg></div>(.*?)<div class="ProfileHeader-divider"></div>(.*?)<div class="ProfileHeader-divider"></div>')	

	if (pattername == 'CAREER') :
		return re.compile('Icon Icon--company(.*?)</svg></div>(.*?)</div><div class="ProfileHeader-info')	

	if (pattername == 'CAREER_DETAIL') :
		return re.compile('(.*)<div class="ProfileHeader-divider"></div>(.*)?<div class="ProfileHeader-divider"></div>(.*)')

	if (pattername == 'CAREER_DETAIL_1') :
		return re.compile('(.*?)<div class="ProfileHeader-divider"></div>(.*)')