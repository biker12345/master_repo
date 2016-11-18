'''
Union Find Algorithm in order to merge networks
@Author: #RAW
'''

import pdb
from datetime import datetime, timedelta
from utils import RedisHelper
from django.conf import settings

class UnionFind():
	def __init__(self, conn_type):
		self.redis_obj = RedisHelper(conn_type)

	def get_redis_ttl(self):
		return settings.REDIS_TTL
		# now = datetime.now()
		# midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
		# return (midnight - now).seconds

	def find_parent(self, group_id):
		group_dict = self.redis_obj.get_value(group_id + "_link")
		group_dict = eval(group_dict)
		if group_dict.get('parent') != group_id:
			group_dict['parent'] = self.find_parent(group_dict.get('parent'))
			ttl = self.get_redis_ttl()
			self.redis_obj.set_value(group_id + "_link", group_dict, ttl)
		return group_dict.get('parent')

	def merge(self, g1, g2):
		p1 = self.find_parent(g1)
		p2 = self.find_parent(g2)
		g1_dict = self.redis_obj.get_value(p1 + "_link")
		g2_dict = self.redis_obj.get_value(p2 + "_link")
		g1_dict, g2_dict = eval(g1_dict), eval(g2_dict)
		if g1_dict.get('rank') < g2_dict.get('rank'):
			g1_dict['parent'] = p2
		elif g2_dict.get('rank') < g1_dict.get('rank'):
			g2_dict['parent'] = p1
		else:
			g2_dict['parent'] = p1
			g2_dict['rank'] = g2_dict.get('rank') + 1
		ttl = self.get_redis_ttl()
		self.redis_obj.set_value(g1+"_link", g1_dict, ttl)
		self.redis_obj.set_value(g2+"_link", g2_dict, ttl)